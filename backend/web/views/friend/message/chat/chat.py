import asyncio
import base64
import json
import os
import threading
import uuid
import websockets

from django.http import StreamingHttpResponse
from langchain_core.messages import HumanMessage, BaseMessageChunk, SystemMessage, AIMessage
from rest_framework.renderers import BaseRenderer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from web.models.friend import Friend, Message, SystemPrompt
from web.views.friend.message.chat.graph import ChatGraph
from web.views.friend.message.memory.update import update_memory
from queue import Queue


class SSERenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


def add_system_prompt(state, friend):
    msgs = state['messages']
    system_prompts = SystemPrompt.objects.filter(title='回复').order_by('order_number')
    prompt = ''
    for sp in system_prompts:
        prompt += sp.prompt
    prompt += f'\n【角色性格】\n{friend.character.profile}\n'
    prompt += f'【长期记忆】\n{friend.memory}\n'
    return {'messages': [SystemMessage(prompt)] + msgs}


def add_recent_messages(state, friend):
    msgs = state['messages']
    message_raw = list(Message.objects.filter(friend=friend).order_by('-id')[:10])
    message_raw.reverse()
    messages = []
    for m in message_raw:
        messages.append(HumanMessage(m.user_message))
        messages.append(AIMessage(m.output))
    return {'messages': msgs[:1] + messages + msgs[-1:]}

class MessageChatView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [SSERenderer]

    def post(self, request):
        friend_id = request.data.get('friend_id')
        message = request.data.get("message", "").strip()

        if not message:
            return Response({'result': '消息不能为空'}, status=400)

        friend = Friend.objects.filter(pk=friend_id, me__user=request.user).first()
        if not friend:
            return Response({'result': '好友不存在'}, status=404)

        app = ChatGraph.create_app()
        inputs = {'messages': [HumanMessage(message)]}
        inputs = add_system_prompt(inputs, friend)
        inputs = add_recent_messages(inputs, friend)

        response = StreamingHttpResponse(
            self.event_stream(app, inputs, friend, message),
            content_type="text/event-stream",
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

    async def tts_sender(self, app, inputs, mq, ws, task_id):

        async for msg_data in app.astream(inputs, stream_mode="messages"):
            msg = msg_data[0] if isinstance(msg_data, tuple) else msg_data

            if isinstance(msg, BaseMessageChunk):
                if msg.content:

                    await ws.send(json.dumps({
                        "header": {"action": "continue-task", "task_id": task_id, "streaming": "duplex"},
                        "payload": {"input": {"text": msg.content}}
                    }))

                    mq.put_nowait({'content': msg.content})

                if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                    mq.put_nowait({'usage': msg.usage_metadata})

        await ws.send(json.dumps({
            "header": {"action": "finish-task", "task_id": task_id, "streaming": "duplex"},
            "payload": {"input": {}}
        }))

    async def tts_receiver(self, mq, ws):
        async for msg in ws:
            if isinstance(msg, bytes):
                audio = base64.b64encode(msg).decode('utf-8')
                mq.put_nowait({'audio': audio})
            else:
                data = json.loads(msg)
                event = data['header']['event']
                if event in ['task-finished', 'task-failed']:
                    break

    async def run_tts_tasks(self, app, inputs, mq):
        task_id = uuid.uuid4().hex
        api_key = os.getenv('API_KEY')
        wss_url = os.getenv('WSS_URL')
        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            async with websockets.connect(wss_url, additional_headers=headers) as ws:

                await ws.send(json.dumps({
                    "header": {"action": "run-task", "task_id": task_id, "streaming": "duplex"},
                    "payload": {
                        "task_group": "audio", "task": "tts", "function": "SpeechSynthesizer",
                        "model": "cosyvoice-v3-flash",
                        "parameters": {
                            "text_type": "PlainText", "voice": "longanyang",
                            "format": "mp3", "sample_rate": 22050, "rate": 1.25
                        },
                        "input": {}
                    }
                }))

                async for msg in ws:
                    if json.loads(msg)['header']['event'] == 'task-started':
                        break

                await asyncio.gather(
                    self.tts_sender(app, inputs, mq, ws, task_id),
                    self.tts_receiver(mq, ws),
                )
        except Exception as e:
            mq.put_nowait({'error': str(e)})

    def work(self, app, inputs, mq):
        try:
            asyncio.run(self.run_tts_tasks(app, inputs, mq))
        finally:
            mq.put_nowait(None)

    def event_stream(self, app, inputs, friend, message):
        mq = Queue()

        thread = threading.Thread(target=self.work, args=(app, inputs, mq))
        thread.daemon = True
        thread.start()

        full_output = ''
        full_usage = {}
        is_aborted = False

        try:
            while True:

                msg = mq.get()
                if msg is None:
                    break

                if 'error' in msg:
                    yield f"data: {json.dumps({'error': msg['error']}, ensure_ascii=False)}\n\n"
                    break

                if msg.get('content'):
                    full_output += msg['content']
                    yield f"data: {json.dumps({'content': msg['content']}, ensure_ascii=False)}\n\n"

                if msg.get('audio'):
                    yield f"data: {json.dumps({'audio': msg['audio']}, ensure_ascii=False)}\n\n"

                if msg.get('usage'):
                    full_usage = msg['usage']

            yield "data: [DONE]\n\n"

        except GeneratorExit:

            is_aborted = True
            raise
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
        finally:

            if full_output:
                try:
                    Message.objects.create(
                        friend=friend,
                        user_message=message[:500],
                        input=json.dumps([m.model_dump() for m in inputs['messages']], ensure_ascii=False)[:10000],
                        output=full_output,
                        input_tokens=full_usage.get('input_tokens', 0),
                        output_tokens=full_usage.get('output_tokens', 0),
                        total_tokens=full_usage.get('total_tokens', 0),
                    )

                    if not is_aborted and Message.objects.filter(friend=friend).count() % 10 == 0:
                        update_memory(friend)
                except Exception as e:
                    print(f"Database save error: {e}")
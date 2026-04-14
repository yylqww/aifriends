import json
from django.http import StreamingHttpResponse
from langchain_core.messages import HumanMessage, BaseMessageChunk
from rest_framework.renderers import BaseRenderer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from web.models.friend import Friend, Message
from web.views.friend.message.chat.graph import ChatGraph


class SSERenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


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

        def event_stream():
            full_output = ''
            full_usage = {}

            try:
                for msg, metadata in app.stream(inputs, stream_mode="messages"):
                    if isinstance(msg, BaseMessageChunk):
                        if msg.content:
                            full_output += msg.content
                            yield f"data: {json.dumps({'content': msg.content}, ensure_ascii=False)}\n\n"

                        if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                            full_usage = msg.usage_metadata

                yield "data: [DONE]\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

            finally:
                if full_output:
                    try:
                        input_tokens = full_usage.get('input_tokens', 0)
                        output_tokens = full_usage.get('output_tokens', 0)
                        total_tokens = full_usage.get('total_tokens', 0)

                        Message.objects.create(
                            friend=friend,
                            user_message=message,
                            input=json.dumps([{"role": "user", "content": message}], ensure_ascii=False),
                            output=full_output,
                            input_tokens=input_tokens,
                            output_tokens=output_tokens,
                            total_tokens=total_tokens,
                        )
                    except Exception as db_err:

                        print(f"数据库存入失败: {db_err}")

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'  
        return response
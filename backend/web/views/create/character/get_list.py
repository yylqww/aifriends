from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response

from web.models.character import Character
from web.models.user import UserProfile


class GetListCharacter(APIView):
    def get(self, request):
        try:
            items_count = int(request.query_params.get('items_count') )
            user_id = request.query_params.get('user_id')
            user_profile = UserProfile.objects.select_related('user').get(user_id=user_id)
            user = user_profile.user

            #预加载作者和用户
            characters_raw = Character.objects.select_related('author__user').filter(
                author=user_profile
            ).order_by('-id')[items_count: items_count + 20]
            characters = []
            for character in characters_raw:
                author = character.author
                characters.append({
                    'id': character.id,
                    'name': character.name,
                    'profile': character.profile,
                    'photo': character.photo.url,
                    'background_image': character.background_image.url,
                    'author': {
                        'user_id': author.user_id,
                        'username': author.user.username,
                        'photo': author.photo.url,
                    }
                })
            return Response({
                'result': 'success',
                'user_profile': {
                    'id': user.id,
                    'username': user.username,
                    'photo': user_profile.photo.url,
                    'profile': user_profile.profile,
                },
                'characters': characters
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试'
            })
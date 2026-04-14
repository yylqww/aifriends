from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

from web.models.character import Character


class HomepageView(APIView):
    def get(self, request):
        try:
            items_count = int(request.query_params.get('items_count', 0))
            search_query = request.query_params.get('search_query', '').strip()
            queryset = Character.objects.select_related('author__user').all()
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) | Q(profile__icontains=search_query)
                )
            characters_raw = queryset.order_by('-id')[items_count: items_count + 20]

            characters = []
            for character in characters_raw:
                characters.append({
                    'id': character.id,
                    'name': character.name,
                    'profile': character.profile,
                    'photo': character.photo.url,
                    'background_image': character.background_image.url,
                    'author': {
                        'user_id': character.author.id,
                        'username': character.author.user.username,
                        'photo': character.author.photo.url,
                    }
                })

            return Response({
                'result': 'success',
                'characters': characters
            })

        except Exception:
            return Response({'result': '系统异常'})
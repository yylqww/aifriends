from django.urls import path, re_path

from web.views.create.character.create import CreateCharacter
from web.views.create.character.get_single import GetSingleCharacter
from web.views.create.character.remove import RemoveCharacter
from web.views.index import index
from web.views.user.account.get_user_info import GetUserInfo
from web.views.user.account.login import LoginView
from web.views.user.account.logout import LogoutView
from web.views.user.account.refresh_token import RefreshToken
from web.views.user.account.register import RegisterView
from web.views.user.profile.update import UpdateProfile

urlpatterns = [
    path('api/user/account/login/', LoginView.as_view()),
    path('api/user/account/logout/', LogoutView.as_view()),
    path('api/user/account/register/', RegisterView.as_view()),
    path('api/user/account/refresh_token/', RefreshToken.as_view()),
    path('api/user/account/get_user_info/', GetUserInfo.as_view()),
    path('api/user/profile/update/', UpdateProfile.as_view()),
    path('api/create/character/create/', CreateCharacter.as_view()),
    path('api/create/character/update/', UpdateProfile.as_view()),
    path('api/create/character/remove/', RemoveCharacter.as_view()),
    path('api/create/character/get_single/', GetSingleCharacter.as_view()),
    path('', index),
    re_path(r'^(?!media/|static/|assets/).*$', index)
]




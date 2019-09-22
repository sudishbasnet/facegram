from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('',views.home),
    path('chat', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
    path('api/users/<int:pk>', views.user_list, name='user-detail'),
    path('api/users', views.user_list, name='user-list'),
    path('addProfile',views.addProfile),
    path('follow',views.follow),
    path('upost',views.UploadPost),
    path('comment',views.comment,name="comment"),
    path('delComment', views.delComment, name="delComment"),
    path('deleteimg', views.deleteimg, name="deleteimg"),
    path('delPost',views.delPost, name="delPost"),
    path('like',views.like,name='like'),
    path('facegrammer',views.facegrammer,name="facegrammer"),
    path('gallery', views.gallery),
    path('user/<str:id>',views.user),
    path('pswd',auth_views.PasswordChangeView.as_view(template_name='signup.html')),
    path('signup/<str:action>',views.signup,name='signup'),
    path('friends/<str:action>',views.followers),
    
    
]

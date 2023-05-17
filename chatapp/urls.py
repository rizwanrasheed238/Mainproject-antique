
from django.urls import path, include
from chatapp import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView
 
 
urlpatterns = [
    path("chatview", chat_views.chatPage, name="chat-page"),
 
    # login-section
    path("auth/login/", LoginView.as_view
         (template_name="chatapp/LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]
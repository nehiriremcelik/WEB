from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from goldenqa import views  # Import views from your goldenqa app

urlpatterns = [
    path('', lambda request: redirect('login/')),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='cores/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('like-answer/<int:answer_id>/', views.like_answer, name='like_answer'),
    path('home/', views.home, name='home'),
]


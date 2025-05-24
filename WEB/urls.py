"""
URL configuration for DjangoProject9 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from goldenqa import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),  
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('vote-answer/<int:answer_id>/', views.vote_answer, name='vote_answer'),
]


from django.urls import path
from . import views
urlpatterns = [

    path('', views.home, name="homepage"),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('new_article/', views.article_create_form, name='article_form'),
    path('article_list/', views.article_list, name='articlelist'),
    path('search', views.search, name='search')

]

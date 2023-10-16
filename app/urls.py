from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home_page'),
    path('blog/<int:id>/details/', details, name='blog_details'),
    path('blog/create/', create, name='blog_create'),
    path('blog/<int:id>/edit/', edit, name='blog_edit'),
    path('blog/<int:id>/delete/', delete, name='blog_delete'),

    path('blog/new_create/', article_create, name='create'),

    path('comment/<int:id>/delete/', comment_delete, name='comment_delete'),
    path('comment/<int:id>/edit/', comment_edit, name='comment_edit'),
]

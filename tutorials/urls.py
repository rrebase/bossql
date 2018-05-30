from django.urls import path

from tutorials import views

app_name = 'tutorials'
urlpatterns = [
    path('', views.index, name='index'),
    path('introduction', views.introduction, name='introduction'),
    path('select', views.select, name='select'),
    path('insert', views.insert, name='insert'),
    path('update', views.update, name='update'),
    path('create', views.create, name='create'),
    path('constraints', views.constraints, name='constraints')
]

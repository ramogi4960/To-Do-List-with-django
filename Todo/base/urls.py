from django.urls import path
from .views import List, Detail, Create, Update, Delete, Login, LogoutView, Register

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('register', Register.as_view(), name='register'),
    path('', List.as_view(), name='list'),
    path('task/<int:pk>', Detail.as_view(), name='detail'),
    path('create', Create.as_view(), name='create'),
    path('update/<int:pk>', Update.as_view(), name='update'),
    path('delete/<int:pk>', Delete.as_view(), name='delete'),
]
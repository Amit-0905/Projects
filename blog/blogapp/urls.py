from django.urls import path
from . import views

urlpatterns =[
    path('',views.home,name='home'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('post/<int:post_id>',views.post_detail,name='post_detail'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('register',views.register,name='register'),
    path('new_post',views.new_post,name='new_post'),
    path('contact_submit',views.contact_submit,name='contact_submit'),
]
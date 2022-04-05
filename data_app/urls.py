from .import views
from django.http import HttpResponse
from django.urls import path

urlpatterns = [


    path('',views.home,name='home'),
    path('index',views.index, name='index'),
    path('login_view', views.login_view, name='login_view'),
    path('receiver',views.receiver,name="receiver"),
    path('owner',views.owner, name="owner"),
    path("receiver_reg",views.data_receiver_register,name="receiver_reg"),
    path("owner_reg",views.data_owner_register,name="owner_reg"),
    path("model_form_upload",views.model_form_upload,name="model_form_upload"),
    path('doc_views',views.doc_views,name='doc_views'),
    path('logout_view/', views.logout_view, name='logout_view'),


]



from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [

    path("", homepage,name='homepage'),
    path("register/", register,name='register'),
    path("login/", userlogin,name='login'),
    path("logout/", userlogout,name='logout'),
    path("adminpage/",adminpagedates,name = "adminpage"),
    path("adminpage/deletedate/<int:pk>/",adminpagedates_delete_full,name="adminpage_delete_date"),
    path("adminpage/<int:year>/<int:month>/<int:typeid>/" , adminpage ,name = "adminpaging"),
    path("adminpage/createdate/",adminpagedates_add_date,name = "adminpagedates_add_date"),
    path("adminpage/addworker/",admin_add_work,name="admin_add_worker"),
    path("adminpage/createtype/",admin_createtype,name = "admincreatetype"),
    path("adminpage/create_worker/",admin_create_worker,name="adminpage_create_worker"),
    path("update-progress-item/", progressitemadd, name="update-progress-item"),
    path("showworkers/",showworkers,name="showworkers"),
    path("showworkers/delete/<int:pk>/" , delete_worker , name = "delete_worker"),
    path("history/",history , name = "history"),
    path("history/<int:pk>/" , delete_history ),
    path("history/change/<int:pk>/",change_history),
    
    
]

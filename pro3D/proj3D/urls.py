"""proj3D URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from app import views as app_v
from app import views_database as app_d
from app import views_upload as app_u
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('index/',app_v.gotoIndex),#test
    path('upload/',app_d.upload),#获取用户上传的内容-test
    #path('upload/',app_u.import_directory),#获取用户上传的内容-test
    path('convert/',app_v.convertTostl),
    path('register/',app_d.register),
    path('login/',app_d.login),
    path('register/',app_d.register),
    path('build_project/',app_d.projectBuild),
    path('get_projects/',app_d.projectGet),
    path('update_project/',app_d.projectUpdate),
    path('delete_project/',app_d.projectDelete),
    path('build_set/',app_d.setBuild),
    path('get_sets/',app_d.setGet),
    path('join_sets/',app_d.setJoin),
    path('update_set/',app_d.setUpdate),
    path('delete_set/',app_d.setDelete),
    path('export_label/',app_d.export_label),#修改
    path('download/<path:file_path>',app_v.send_nii),
    path('seg_predict/',app_d.predict),
    path('build_3D/',app_d.build_3D),
    path('get_label/',app_d.labelGet),
    path('update_label/',app_d.labelUpdate),
    path('logout/',app_d.logout)
    
]
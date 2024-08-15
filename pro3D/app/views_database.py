import json
from django.http import JsonResponse
from app.models import User,Project,Label,CTSet
from django.http import HttpResponse
from . import nii2stl
from . import views_upload
from django.http import HttpResponseRedirect
from django.shortcuts import render
import os
import glob
import nibabel as nib
import SimpleITK as sitk
import numpy as np
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
import datetime
LABEL_NAMES = {
    1: "spleen",
    2: "right kidney",
    3: "left kidney",
    4: "gall bladder",
    5: "esophagus",
    6: "liver",
    7: "stomach",
    8: "aorta",
    9: "postcava",
    10: "pancreas",
    11: "right adrenal gland",
    12: "left adrenal gland",
    13: "duodenum",
    14: "bladder",
    15: "prostate/uterus"
}

LABEL_COLORS = {
    1: (255, 87, 51),   # orange
    2: (199, 0, 57),    # red
    3: (144, 12, 63),   # deep pink
    4: (88, 24, 69),    # dark purple
    5: (218, 247, 166), # pale green
    6: (18, 135, 165),  # blue-green
    7: (11, 83, 69),    # dark green
    8: (25, 111, 61),   # forest green
    9: (125, 102, 8),   # olive
    10: (241, 196, 15), # yellow
    11: (230, 126, 34), # carrot orange
    12: (108, 52, 131), # royal purple
    13: (46, 64, 83),   # navy blue
    14: (241, 169, 160),# salmon pink
    15: (133, 193, 233) # light blue
}
# base_file = "D:/TEMP/"
base_file = "C:/Users/92090/Desktop/TEMP/"

#注册
def register(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        user_account = input_data['user_account']
        user_password = input_data['user_password']
        if User.objects.filter(user_account=user_account).exists():
            return HttpResponse(json.dumps({'status':'fail','reason':'该用户名已被注册'}))
        else:
            new_user = User.objects.create(user_account=user_account, user_password=user_password)
            return HttpResponse(json.dumps({'status':'OK'}))

#登录，主要判断用户名和密码是否符合
def login(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        try:
            user = User.objects.get(user_account=input_data["account"])
            password = user.user_password
        except User.DoesNotExist:
            # 没有找到对应的用户
            password = None
            return HttpResponse(json.dumps({'status':'fail','reason':'invalid account'}))
        if(password==input_data["password"]):#登录成功
            response=HttpResponse(json.dumps({'status':'OK'}))
            #设置cookie
            # response.set_signed_cookie('account', user.user_id, salt='salt', max_age=30*24*60*60)
            response.set_cookie('account', user.user_id, max_age=30*24*60*60)
            return response
        else:
            return HttpResponse(json.dumps({'status':'fail','reason':'invalid password'}))
    # return render(request, 'login.html')
def projectBuild(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        #根据cookie获得accountid
        userID = request.COOKIES.get('account')
        user = User.objects.get(user_id=userID)
        project=Project.objects.create(project_id = input_data["project_id"],project_name=input_data["project_name"],user=user,remark=input_data["remark"])
        return HttpResponse(json.dumps({'status':'OK','project_id':project.project_id}))
    # return render(request, 'buildproject.html')
def projectGet(request):
    if request.method == 'POST':
        user_id = request.COOKIES.get('account')
        # 通过用户id获取用户对象
        user = User.objects.get(user_id=user_id)
        # 通过用户对象获取该用户的所有项目
        projects = Project.objects.filter(user=user)
        # 遍历所有项目，将项目id和项目名字存储在字典中
        result = []
        for project in projects:
            set_ids = list(project.ctset_set.values_list('set_id', flat=True))
            result.append({
                'project_id':project.project_id,
                'project_name': project.project_name,
                'project_build_time': project.build_time.strftime('%Y-%m-%d %H:%I:%S'),
                'remark': project.remark,
                'sets_id': set_ids,
            })
        #如果没有对象，存空值
        if not result:
            result={}
        response_data = {"status": "OK","projects": result}    
        return HttpResponse(json.dumps(response_data))
    # return render(request, 'getproject.html')
def projectUpdate(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        project_data = input_data.get('project')
        project_id = project_data.get('project_id')
        # 检查是否存在该项目
        updateproject = Project.objects.get(project_id=project_id)
        # 更新项目信息
        updateproject.project_name = project_data.get('project_name', updateproject.project_name)
        updateproject.user = project_data.get('user', updateproject.user)
        updateproject.remark = project_data.get('remark', updateproject.remark)
        updateproject.save()
        return JsonResponse({'status': 'OK'})
def projectDelete(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        project_id=input_data['project_id']
        project = Project.objects.get(project_id=project_id)
        project.delete()
        return HttpResponse(json.dumps({'status':'OK'}))
def setBuild(request):
    if request.method == 'POST':
        user_id = request.COOKIES.get('account')
        input_data = json.loads(request.body)
        CT_set=CTSet.objects.create(set_name=input_data['set_name'],set_id=input_data['set_id'],remark=input_data['remark'],user_id=user_id)
        if input_data['project_id'] != '':
            project = Project.objects.get(project_id=input_data['project_id'])
            #ctset_set 是 Django 自动生成的 ManyToManyField 的默认属性名称,ctset_set 是 Django 自动生成的 ManyToManyField 的默认属性名称
            project.ctset_set.add(CT_set)
        return HttpResponse(json.dumps({'status':'OK','set_id':CT_set.set_id}))
    return render(request, 'buildset.html')
def setGet(request):
    if request.method == 'POST':
        user_id = request.COOKIES.get('account')
        # 通过用户id获取用户对象
        user = User.objects.get(user_id=user_id)
        # 通过用户对象获取该用户的所有项目
        #__实现跨表查询
        sets = CTSet.objects.filter(user_id=user_id)
        # 遍历所有项目，将项目id和项目名字存储在字典中
        result = []
        for CT_set in sets:
            result.append ( {
                'set_id':CT_set.set_id,
                'set_name': CT_set.set_name,
                'directory': CT_set.directory,
                'original_path': CT_set.original_path,
                'nii_path': CT_set.nii_path,
                'label_path': CT_set.label_path,
                'nii_after_path': CT_set.nii_after_path,
                'stl_directory': CT_set.stl_directory,

                'build_time': CT_set.build_time.strftime('%Y-%m-%d %H:%I:%S'),
                'remark': CT_set.remark,
            })
        #如果没有对象，存空值
        if not result:
            result=[]
        response_data = {"status": "OK","sets": result}    
        return HttpResponse(json.dumps(response_data))
    # return render(request, 'getset.html')
def setJoin(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        project_id = input_data['project_id']
        sets_id_list = input_data['sets_id_list']
        try:
            project = Project.objects.get(project_id=project_id)
        except Project.DoesNotExist:
            return HttpResponse(json.dumps({'status':'fail','reason':'there is no such project'}))
        set_ids = list(project.ctset_set.values_list('set_id', flat=True))
        # 没有的增加
        for CT_set_id in sets_id_list:
            if (CT_set_id not in set_ids):
                ct_set = CTSet.objects.get(set_id=CT_set_id)
                project.ctset_set.add(ct_set)
        # 确认哪些需要减少
        for CT_set_id in set_ids:
            if (CT_set_id not in sets_id_list):
                ct_set = CTSet.objects.get(set_id=CT_set_id)
                project.ctset_set.remove(ct_set)
        return HttpResponse(json.dumps({'status':'OK'}))
def setDelete(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        set_id=input_data['set_id']
        Set = CTSet.objects.get(set_id=set_id)
        Set.delete()
        return HttpResponse(json.dumps({'status':'OK'}))    
#7.
def export_label(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        CT_set_id = input_data['set_id']
        try:
            ct_set = CTSet.objects.get(set_id=CT_set_id)
            file_path = ct_set.label_path
            file=open(file_path, 'rb')
            response = FileResponse(file)
            #是一个下载文件请求（attachment），下载文件取名为label.nii.gz
            response['Content-Disposition'] = 'attachment; filename=label.nii.gz'
            #响应是一个二进制流‘application/octet-steam'
            response['Content-Type'] = 'application/octet-stream'
            return response
        except CTSet.DoesNotExist:
                return HttpResponse(json.dumps({'status':'fail'}))

def labelDelete(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        label=input_data['label']
        label_ = Label.objects.get(label=label)
        label_.delete()
        return HttpResponse(json.dumps({'status':'OK'}))   

        
def setUpdate(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        set_data = input_data.get('set')
        set_id = set_data.get('set_id')
        # 检查是否存在该项目
        updateset = CTSet.objects.get(set_id=set_id)
        # 更新项目信息
        updateset.set_name = set_data.get('set_name', updateset.set_name)
        updateset.remark = set_data.get('remark', updateset.remark)
        # #更新多对多关系
        # #获取与set有关的projects
        # project_ids = set_data.get('projects')
        # if project_ids:
        #     updateset.projects.clear()  # 清空之前的关系
        #     for project_id in project_ids:
        #         project = Project.objects.get(project_id=project_id)
        #         updateset.projects.add(project)
        updateset.save()
        return JsonResponse({'status': 'OK'})
# 8 文件上传 可以支持上传单个文件或者压缩包
def upload(request):
    if request.method == 'POST':
        up_file = request.FILES.get('file')
        input_data = request.POST
        set_id=input_data['set_id']
        re_upload=input_data['re_upload']
        CT_set=CTSet.objects.get(set_id=set_id)#得到对应的set
        if up_file and not CT_set.nii_path:#原文件为空
            destination_path=None

            #上传的是单个文件
            if up_file.name.endswith('.nii')or up_file.name.endswith('.nii.gz') or up_file.name.endswith('.mhd') or up_file.name.endswith('.dcm') or up_file.name.endswith('.raw'):
                destination_path=views_upload.import_file(request)#转为nii后的地址
                CT_set.nii_path = destination_path#新地址保存
                CT_set.save()
                return HttpResponse(json.dumps({'status':'OK','file_path':destination_path}))
            #上传的是压缩包
            elif up_file.name.endswith('.rar') or up_file.name.endswith('.zip') :
                destination_path=views_upload.import_directory(request)
                CT_set.nii_path = destination_path
                CT_set.save()
                return HttpResponse(json.dumps({'status':'OK','file_path':destination_path}))
            else:
                return HttpResponse(json.dumps({'status':'fail','reason':'invalid file'}))
        elif up_file and re_upload:
            
            #上传的是单个文件
            if up_file.name.endswith('.nii')or up_file.name.endswith('.nii.gz') or up_file.name.endswith('.mhd') or up_file.name.endswith('.dcm') or up_file.name.endswith('.raw'):
                destination_path=views_upload.import_file(request)
                CT_set.nii_path = destination_path
                CT_set.save()
                return HttpResponse(json.dumps({'status':'OK','file_path':destination_path}))
            #上传的是压缩包
            elif up_file.name.endswith('.rar') or up_file.name.endswith('.zip'):
                destination_path=views_upload.import_directory(request)
                CT_set.nii_path = destination_path
                CT_set.save()
                return HttpResponse(json.dumps({'status':'OK','file_path':destination_path}))
            else:
                return HttpResponse(json.dumps({'status':'fail','reason':'invalid file'}))
        else:#无法上传
            return HttpResponse(json.dumps({'status':'fail'}))
    




# #10.预测模型
def predict(request):
    input_data = json.loads(request.body)
    # 以下仅模拟已经得到的过程
    set_id=input_data['set_id']
    CT_set=CTSet.objects.get(set_id=set_id)
    label_nii_path = "C:/Users/92090/Desktop/3D_medical/base_train/labelsTr/test_label.nii"
    CT_set.label_path = label_nii_path
    CT_set.nii_after_path = label_nii_path
    CT_set.save()
    labelInit(set_id,label_nii_path)
    ##导入模型训练
    return HttpResponse(json.dumps({'status':'OK','label_nii_path':label_nii_path}))
    return HttpResponse(json.dumps({'status':'fail','reason':'没有导入成功'}))
#11.三维重建   
def build_3D(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        set_id=input_data['set_id']
        CT_set=CTSet.objects.get(set_id=set_id)
        label_nii=CT_set.nii_after_path
        folder,file_dict,volume_dict=nii2stl.Tostl(label_nii)
        CT_set.stl_directory=folder#TEMP/stl/xxxx
        CT_set.save()
        # 更新标签路径
        labels = Label.objects.filter(ct_set=CT_set)
        for label_ in labels:
            Label.objects.filter(label=label_.label,ct_set_id=set_id).update(stl_path=file_dict[label_.label],volume=volume_dict[label_.label])
        return HttpResponse(json.dumps({'status':'OK'}))


# #12.标签初始化【已经变为非前后端交互函数】
def labelInit(set_id,label_nii_path):
        # 创建一个新标签
        CT_set=CTSet.objects.get(set_id=set_id)
        multi_label_image=sitk.ReadImage(label_nii_path)
        img_npy = sitk.GetArrayFromImage(multi_label_image)
        labels = np.unique(img_npy)
        for label in labels:
            if (label != 0):
                organ=LABEL_NAMES[label]
                color_r, color_g, color_b = LABEL_COLORS[label]
                newlabel = Label.objects.create(label=label,organ_name=organ,r=color_r,g=color_g,b=color_b,transparency=0.9,visible=True,stl_path="",ct_set=CT_set) 
#13.获取标签
def labelGet(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        CT_set_id = input_data['set_id']
        try:
            index=1
            CT_set = CTSet.objects.get(set_id=CT_set_id)
            # labels=Label.objects.get(ct_set=CT_set)
            labels = Label.objects.filter(ct_set=CT_set)
            result = {}
            for label_ in labels:
                result[label_.label]={
                    'stl_path': label_.stl_path,
                    'name': label_.organ_name,
                    'r': label_.r,
                    'g':label_.g,
                    'b':label_.b,
                    'volume':round(label_.volume,3),
                    'opacity': label_.transparency,
                    'visible': label_.visible
                }
            return HttpResponse(json.dumps({'status':'OK','label_list':result}))
        except CTSet.DoesNotExist:#没有这个CTSet
            return HttpResponse(json.dumps({'status':'fail','reaso':'未初始化标签'}))
#14.更新标签：
def labelUpdate(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
        set_id=input_data['set_id']
        labels=input_data['labels']
        for label in labels:
            label_id=label#作为查找
            try:
                label_modify=Label.objects.filter(label=label_id).update(
                    stl_path=label['stl_path'],
                    organ_name=label['organ_name'],
                    # r=label['color'][0],
                    # g=label['color'][1],
                    # b=label['color'][2],
                    r=label['r'],
                    g=label['g'],
                    b=label['b'],
                    transparency=label['opacity'],
                    visible=label['visible'])
                return HttpResponse(json.dumps({'status':'OK'}))
            except Label.DoesNotExist:
                return HttpResponse(json.dumps({'status':'fail'}))
        
# 15. 退出，清除cookie
def logout(request):
    response = HttpResponse(json.dumps({'status': 'OK'}))
    response.delete_cookie('account')
    return response
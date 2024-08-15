from django.shortcuts import render
from django.http import FileResponse
from app.models import User,CTSet
from django.http import HttpResponse
import SimpleITK as sitk
# Create your views here.
from django.shortcuts import redirect, render 
import os
from django.shortcuts import render
from django.http import HttpResponseRedirect
import vtk
import SimpleITK as sitk
import numpy as np
import pyvista as pv
import vtk
import json
import os
import shutil
import SimpleITK as sitk
import os
import gzip
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import nibabel as nib
import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

import shutil
import zipfile
import glob
import os
import zipfile
import rarfile
from django.http import HttpResponseBadRequest
# base_file = "D:/TEMP/"
base_file = "C:/Users/92090/Desktop/TEMP/"
def import_directory(request):
    up_dir = request.FILES.get('file')
    # Store the uploaded directory in a temporary directory
    temp_dir = base_file+"temp/"

    delete_dir=temp_dir
    userID = request.COOKIES.get('account')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    if up_dir.name.endswith('.zip'):
        archive = zipfile.ZipFile(up_dir)
        extract_dir = base_file+"temp/"#用于存放解压后的文件
        os.makedirs(extract_dir, exist_ok=True)
        archive.extractall(extract_dir)#解压到相应文件
        archive.close()
        for root, dirs, files in os.walk(extract_dir):
            if not(root.endswith('temp')):
                temp_dir=root

    elif up_dir.name.endswith('.rar'):
        archive = rarfile.RarFile(up_dir)
        extract_dir = base_file+"temp/"
        # os.makedirs(extract_dir, exist_ok=True)
        archive.extractall(extract_dir)
        archive.close()
        
        for root, dirs, files in os.walk(extract_dir):
            if not(root.endswith('temp')):
                temp_dir=root

    else:#上传的是文件夹
        print(request.FILES.getlist('file'))
        for uploaded_file in request.FILES.getlist('file'):
            print("uploaded_file:",uploaded_file.name)
            with open(base_file+"temp/" + uploaded_file.name, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
    destination_path=None
    # 将文件夹中文件转为nii
    #当上传的是多个文件时，以用户id命名文件夹，这个文件夹为files_dir
    files_dir = os.path.normpath(os.path.join(base_file, 'get',userID))
    print('files_dir',files_dir)
    print('temp_dir',temp_dir)
    #当上传的是多个文件时，以用户id命名文件夹（该文件夹中全为nii）
    if os.path.exists(files_dir):
        shutil.rmtree(files_dir)
    os.makedirs(files_dir)
    #遍历,将文件转换为nii
    for file_name in os.listdir(temp_dir):
        basename, ext = os.path.splitext(file_name)
        if ext not in ['.nii', '.nii.gz','.mhd', '.dcm']:#暂时没有添加raw
            continue
        #raw和mhd要凑一起
        file_path = os.path.join(temp_dir, file_name)
        reader = sitk.ImageFileReader()
        reader.SetFileName(file_path)
        image = reader.Execute()
        nii_bytes = sitk.GetArrayFromImage(image).tobytes()
        destination_path = os.path.normpath(os.path.join(files_dir,f'{basename}.nii'))
        with open(destination_path, 'wb') as f:
            f.write(nii_bytes)
    
    # Remove the temporary directory
    shutil.rmtree(delete_dir)
    #查询文件夹中文件数量
    # 获取所有nii文件
    nii_files = glob.glob(os.path.join(files_dir, "*.nii"))
# 计算nii文件数量
    file_count = len(nii_files)
    
    if(file_count>1):#合并为一个
        
        destination_path =os.path.normpath(os.path.join(base_file, 'get',f'{basename}.nii'))#最后输入合并后的nii地址,basename是某一个nii的名字
        # Load all the Nifti files in the input directory
        nii_files = []
        for nii_file in glob.glob(os.path.join(files_dir, "*.nii")):
            nii_files.append(nib.load(nii_file))

        # 合并nii文件
        merged_img = nib.concat_images(nii_files, check_affines=True)

        # 保存到指定位置
        nib.save(merged_img, destination_path, compress=False)
        shutil.rmtree(files_dir)
        return destination_path
    elif(file_count==1):#如果只有一个文件，移到指定地点
        source_file =os.path.normpath(os.path.join(files_dir,f'{basename}.nii'))
        destination_path = os.path.normpath(os.path.join(base_file, 'get',f'{basename}.nii'))
        shutil.copy(source_file, destination_path)
        shutil.rmtree(files_dir)
        return destination_path
    else:
        print("没有上传成功")
    return HttpResponseRedirect('/success/')#跳转地址

#如果显示tool有问题，可以https://blog.csdn.net/im_hwp/article/details/108724749
#这里默认一次上传一个压缩包

def import_file(request):
    up_file = request.FILES.get('file')
    ''''----------------------------------先将文件存下来----------------------------------'''
    uploaded_file = request.FILES['file']
    with open(base_file+"test/" + uploaded_file.name, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    file_path = destination.name
    # 将上传的文件保存到指定目录下
    # ext = os.path.splitext(up_file.name)[1].lower() #判断文件后缀
    '''------------------------------------再转为nii格式，并保存nii格式---------------------'''
    basename = os.path.basename(up_file.name)
    print("basename:",basename)
    name, ext = basename.split('.', 1)
    ext="."+ext
    '''此时假设这个CT集合已经存在？？？？？？？？？？？？？？？？？？？？？？？？？暂时不考虑数据库部分'''
    # file_name = CTCollection.objects.create(nii_path=file_path,projects=project)
    #
    if ext not in ['.nii', '.nii.gz','.mhd', '.raw', '.dcm']:
        return HttpResponse('Invalid file type')
    if(ext=='.mhd' or ext=='.raw'):
        messages.error(request, 'please upload .mhd and .raw files together')
        return redirect('/upload')
    print(file_path)#D:/TEMP/test0b2be9e0-886b-4144-99f0-8bb4c6eaa848.nii.gz
    # 读取和转换文件格式
    reader = sitk.ImageFileReader()
    reader.SetFileName(file_path)
    image = reader.Execute()
    #nii_bytes = sitk.GetArrayFromImage(image).tobytes()

    #判断是否存在该文件夹
    destination_path = base_file+'get/'

    if not os.path.exists(destination_path):#判断目标地址是否存在
        os.makedirs(destination_path)#不存在就创建
    # destination_path = os.path.join(destination_path, up_file.name)
    # destination_path = os.path.normpath(os.path.join(base_file, 'get', up_file.name))
    # 保存 .nii 文件到本地
    destination_path = os.path.normpath(os.path.join(base_file, 'get', f'{name}.nii'))
    # with open(destination_path, 'wb') as f:
    #     f.write(nii_bytes)
    print(destination_path)#D:/TEMP/get/0b2be9e0-886b-4144-99f0-8bb4c6eaa848.nii
    sitk.WriteImage(image,destination_path)


    return destination_path
    return HttpResponseRedirect('/success/')#跳转地址

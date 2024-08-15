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

import os
import zipfile
import rarfile
from django.http import HttpResponseBadRequest
'''import_file和import_directory放到views_upload里面去了'''

'''文件夹命名
\temp临时存储上传的文件夹，压缩包解压后的文件夹
\get 存储nii文件
\stl 存储stl文件
\test 存储转为nii前的文件（刚刚上传的文件）
\back 存储nii转为其他格式的文件
'''
def send_nii(request, file_path):
    # CTCollection.objects.create()#需要先创建患者
    return FileResponse(open(file_path, 'rb'))
# destination_stl_path=r"D:\TEMP\stl\0b2be9e0-886b-4144-99f0-8bb4c6eaa848.stl"
# destination_path=r"D:\TEMP\get\0b2be9e0-886b-4144-99f0-8bb4c6eaa848.nii"
#连接用户

def userLog(request):
    return 
def gotoIndex(request):
    return redirect('/upload/')
def gotoDir(request):
    return redirect('/upload_dir/')
base_file = "D:/TEMP/"
#base_file = "C:/Users/92090/Desktop/TEMP/"

'''import_file和import_directory放到views_upload里面去了'''

#有用户
# def convertTostl(request,username):
#     file_path=Medical_infor.objects.filter(userName=username).values('storeName')#获得数据库中存储的
#     destination_path = os.path.join(r"D:\TEMP\get", file_path)
#     print(destination_path)

#     name, ext = os.path.splitext(file_path)
#     print(name)

#     destination_stl_path = os.path.join(r"D:\TEMP\stl", name + '.stl')
#     print(destination_stl_path)
#无数据库
def convertTostl(request):
    destination_stl_path=r"D:\TEMP\stl\0b2be9e0-886b-4144-99f0-8bb4c6eaa848.stl"
    destination_path=r"D:\TEMP\get\0b2be9e0-886b-4144-99f0-8bb4c6eaa848.nii"

    # 读取 NIfTI 文件
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(destination_path)
    reader.Update()

    # 转换为 STL
    surface_filter = vtk.vtkMarchingCubes()
    surface_filter.SetInputConnection(reader.GetOutputPort())
    surface_filter.SetValue(0, 0.5)
    surface_filter.Update()

            # 写入 STL 文件
    writer = vtk.vtkSTLWriter()
    writer.SetFileName(destination_stl_path)
    writer.SetInputConnection(surface_filter.GetOutputPort())
    writer.Write()
    return HttpResponseRedirect('/success/')#跳转地址




#如果显示tool有问题，可以https://blog.csdn.net/im_hwp/article/details/108724749
#这里默认一次上传一个压缩包

#暂时写死
def converBack(request,type):
    nii_path=r"brain_1.nii"#这里需要根据数据库得到
    temp_dir = base_file+"back/"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    if(type=='nii.gz'):
        destination_path=os.path.join(base_file,r"back",'out.nii.gz')
        image=sitk.ReadImage(nii_path)# 读取要转换格式的图像
        sitk.WriteImage(image,destination_path)
        return FileResponse(open(destination_path, 'rb'))
        return HttpResponse(json.dumps({'status':'OK','file_path':destination_path}))
    elif(type=='mhd'):#生成raw和mhd两个文件，因为.mhd文件只是描述图像元数据的文件，而图像数据则存储在.raw文件中
        destination_path=os.path.join(base_file,r"back",'out.mhd')
        image=sitk.ReadImage(nii_path)# 读取要转换格式的图像
        sitk.WriteImage(image,destination_path) 
        return FileResponse(open(destination_path, 'rb')) 
        return HttpResponse(json.dumps({'status':'OK','file_path':destination_path}))
    elif(type=='raw'):#生成单独raw文件，用simpleitk转会报错
        nii = nib.load(nii_path)
        nii_data = nii.get_fdata()
        destination_path=os.path.join(base_file,r"back",'out.raw')
        with open(destination_path, 'wb') as f:
        # Convert data to 16-bit integers (assuming data is in [0, 1] range)
            data = (nii_data * 65535).astype(np.uint16)
            # Write data to binary file
            f.write(data.tobytes())
        return FileResponse(open(destination_path, 'rb'))
        return HttpResponse(json.dumps({'status':'OK','file_path':destination_path}))
    elif(type=='dcm'):
        destination_path=os.path.join(base_file,r"back",'out.dcm')
        image=sitk.ReadImage(nii_path)# 读取要转换格式的图像
        sitk.WriteImage(image,destination_path)
        return FileResponse(open(destination_path, 'rb'))
        return HttpResponse(json.dumps({'status':'OK','file_path':destination_path}))
    else:
        return HttpResponse(json.dumps({'status':'sorry,invalid type'}))
    return render(request, 'upload.html')
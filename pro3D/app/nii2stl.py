import vtk
import glob
import SimpleITK as sitk
import numpy as np
import os

# base_file = "D:/TEMP/"
base_file = "C:/Users/92090/Desktop/TEMP/"
#folder是存在base_file下stl里
# if __name__ == '__main__':
def Tostl(filename_nii) : 
    # can be done in a loop if you have multiple files to be processed, speed is guaranteed if GPU is used:)
    # filename_nii =  'nii2stl/0c593893-56d7-4169-8f8e-703d9b205196.nii.gz'
    filename = filename_nii.split(".")[0].split("/")[-1]

    # read all the labels present in the file
    multi_label_image=sitk.ReadImage(filename_nii)
    img_npy = sitk.GetArrayFromImage(multi_label_image)
    labels = np.unique(img_npy)
    
    # read the file
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(filename_nii)
    reader.Update()
    foldername =  os.path.join(base_file,'stl', filename)
    os.makedirs(foldername, exist_ok=True)
    # for all labels presented in the segmented file
    file_dict = {}
    volume_dict = {}
    for label in labels:

        if int(label) != 0:

            # apply marching cube surface generation
            surf = vtk.vtkDiscreteMarchingCubes()
            surf.SetInputConnection(reader.GetOutputPort())
            surf.SetValue(0, int(label)) # use surf.GenerateValues function if more than one contour is available in the file
            surf.Update()
            
            
            
            #smoothing the mesh
            smoother= vtk.vtkWindowedSincPolyDataFilter()
            if vtk.VTK_MAJOR_VERSION <= 5:
                smoother.SetInput(surf.GetOutput())
            else:
                smoother.SetInputConnection(surf.GetOutputPort())
            
            # increase this integer set number of iterations if smoother surface wanted
            smoother.SetNumberOfIterations(30) 
            smoother.NonManifoldSmoothingOn()
            smoother.NormalizeCoordinatesOn() #The positions can be translated and scaled such that they fit within a range of [-1, 1] prior to the smoothing computation
            smoother.GenerateErrorScalarsOn()
            smoother.Update()
            
            # save the output
            writer = vtk.vtkSTLWriter()
            writer.SetInputConnection(smoother.GetOutputPort())
            writer.SetFileTypeToASCII()

            massProps = vtk.vtkMassProperties()
            massProps.SetInputConnection(smoother.GetOutputPort())
            massProps.Update()
            volume_dict[label] = massProps.GetVolume()*0.001
            
            # file name need to be changed
            # save as the .stl file, can be changed to other surface mesh file
            writer.SetFileName(os.path.join(foldername, f'{filename}_{label}.stl'))
            writer.Write()
            file_dict[label] = os.path.join(foldername, f'{filename}_{label}.stl')
    return foldername,file_dict,volume_dict
#因为前缀一样，都是base_file stl里面
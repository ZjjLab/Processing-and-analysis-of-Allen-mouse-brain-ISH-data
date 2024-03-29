import glob
import SimpleITK as sitk
from libtiff import TIFF
from PIL import Image
import os
#import numpy as np

def write_to_tiff(tiff_image_name, im_array, image_num):
    tif = TIFF.open(tiff_image_name, mode = 'w')
    for i in range(0, image_num):
        im = Image.fromarray(im_array[0][i])
        # im = im.resize((480, 480), Image.ANTIALIAS)
        tif.write_image(im, compression = None)
    tif.close()
    return


if __name__ == "__main__":
    read_path = r"C:\Users\wangtong1\Desktop\developing_mouse geneexpression_1\P56"    # 获取文件路径 P56 58 P28 53 P14 50 P4 50
    output_path = r"C:\Users\wangtong1\Desktop\developing_mouse geneexpression_1\P56"
    for i in os.listdir(read_path):
        file_name = glob.glob(read_path+'/'+i+"/energy.mhd")
        image = sitk.ReadImage(file_name)
        image_array = sitk.GetArrayFromImage(image)
        write_to_tiff(output_path+'/'+i+'/energy.tif',image_array,58)#输出路径


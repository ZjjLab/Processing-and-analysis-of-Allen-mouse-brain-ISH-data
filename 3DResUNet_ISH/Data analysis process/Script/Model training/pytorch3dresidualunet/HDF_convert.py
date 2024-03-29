import h5py
# import cv2 ## for image conversion
import tifffile
import numpy as np
filename = r'E:\pytorch-3dunet-master\dataset\test\1-1_predictions.h5'

with h5py.File(filename,'r') as hdf:
    # get image dataset
    # img_ds = hdf['label']
    img_ds = hdf['predictions']
    print(f'Image Dataset info: Shape={img_ds.shape},Dtype={img_ds.dtype}')
    ## following depends on dataset shape/schema
    ## code below assumes images are along axis=0
    # for i in range(img_ds.shape[0]):
    #     cv2.imwrite(f'test_img_{i:03}.tiff',img_ds[i,:]) # uses slice notation
    #     # alternately load to a numpy array first
    #     img_arr = img_ds[i,:]   # slice notation gets [i,:,:,:]
    #     cv2.imwrite(f'test_img_{i:03}.tiff',img_arr)
    # tifffile.imwrite('output_raw.tif', np.asarray(img_ds).transpose(0,1,2).astype('f'), imagej=True)
    tifffile.imwrite('output.tif', np.asarray(img_ds).transpose(1,2,0).astype('f'), imagej=True)
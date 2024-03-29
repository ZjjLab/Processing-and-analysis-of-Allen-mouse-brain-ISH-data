import h5py
import numpy as np
import scipy.stats as stats
import os,random
import pandas as pd
from skimage.metrics import adapted_rand_error, peak_signal_noise_ratio, mean_squared_error, structural_similarity
from sklearn.metrics import r2_score
import math


all = []
data = pd.read_csv('D:/63113/coronal_581/581-(log2_Min-Max Normalization(everyone))/list.csv',header=0,index_col=0)
data = np.array(data)

for i in range(100):
    lst = []
    filedir = 'D:/63113/coronal_581/581-(log2_Min-Max Normalization(everyone))/h5(log2_Min-Max Normalization(everyone))-MAR(1940)/test'
    pathDir = os.listdir(filedir)  # 取图片的原始路径
    filenumber = len(pathDir)
    rate = 0.25  # 自定义抽取图片的比例，比方说100张抽10张，那就是0.1
    picknumber = int(filenumber * rate)  # 按照rate比例从文件夹中取一定数量图片
    files = random.sample(pathDir, picknumber)  # 随机选取picknumber数量的样本图片

    for file in files:

        path = 'D:/63113/coronal_581/581-(log2_Min-Max Normalization(everyone))/h5(log2_Min-Max Normalization(everyone))-MAR(1940)/test/' + file
        # file1 = str.split(file,'.')[0] + '_predictions.h5'
        path1 = 'D:/63113/coronal_581/581-(log2_Min-Max Normalization(everyone))/h5(log2_Min-Max Normalization(everyone))-MAR(1940)/test(for knn)/'+ file  #file1
        id = str.split(str.split(file,'.')[0],'-')[-1]
        f = h5py.File(path, 'r')
        f1 = h5py.File(path1, 'r')

        #读取海马h5文件
        ff = h5py.File(r'C:\Users\DELL\Desktop\genedata\hip_template.h5','r')


        hip_mask = (ff['raw'])[()]

        raw = (f['raw'])[()]
        label = (f['label'])[()]
        # predict = (f['interpolate1'])[()]
        predict = (f1['raw'])[()]

        bb = np.argwhere(raw == 0)
        a = np.unique(bb[:, 2])


        label1 = label[:, :, a]
        predict1 = predict[:, :, a]
        raw1 = raw[:, :, a]

        cc = data[(int(id)-1)][0]



        #计算全脑
        raw1[label1 > 0] = np.power(2, (raw1[label1 > 0] ))
        label1[label1 > 0] = np.power(2, (label1[label1 > 0]* cc))-1
        predict1[label1 > 0] = np.power(2, (predict1[label1 > 0]* cc))-1
        #predict[raw > 0] = raw[raw > 0]

        #计算海马
        #raw[label > 0] = np.power(2, (raw[label > 0]* cc))-1
        # label[label > 0] = np.power(2, (label[label > 0]* cc))-1
        # predict[label > 0] = np.power(2, (predict[label > 0]* cc))-1
        #predict[raw > 0] = raw[raw > 0]

        #raw1[label1>0] = np.power(2,(raw1[label1>0]*5)) - epsilon


        #predict1[label1>0] = np.power(28,(predict1[label1>0])) - epsilon

        hip_label = label[hip_mask>0]
        hip_predict = predict[hip_mask>0]

        # if hip_label.size > 2:
        if np.where(raw1==0)[0].size >0:


            #求全脑
            # SSR = np.sum((predict1[raw1==0]-np.mean(label1[raw1==0]))**2)
            # SST = np.sum((label1[raw1 == 0] - np.mean(label1[raw1 == 0])) ** 2)
            # R2 = SSR/SST
            # R2 = r2_score(label1[raw1==0], predict1[raw1==0])
            # cor = stats.pearsonr(label1[raw1==0], predict1[raw1==0])[0]
            # mse = mean_squared_error(label1[raw1==0], predict1[raw1==0])
            # psnr = peak_signal_noise_ratio(label1[raw1==0], predict1[raw1==0], data_range=max(label1[raw1==0].max(), predict1[raw1==0].max()))
            # ssim = structural_similarity(label1[raw1==0], predict1[raw1==0],win_size=3, data_range=max(label1[raw1==0].max(), predict1[raw1==0].max()))  #win_size默认为7

            R2 = r2_score(label1[label1 > 0], predict1[label1 > 0])
            cor = stats.pearsonr(label1[label1 > 0], predict1[label1 > 0])[0]
            mse = mean_squared_error(label1[label1 > 0], predict1[label1 > 0])
            psnr = peak_signal_noise_ratio(label1[label1 > 0], predict1[label1 > 0],
                                           data_range=max(label1[label1 > 0].max(),
                                                          predict1[label1 > 0].max()))
            ssim = structural_similarity(label1[label1 > 0], predict1[label1 > 0], win_size=3,
                                         data_range=max(label1[label1 > 0].max(),
                                                        predict1[label1 > 0].max()))  # win_size默认为7

            # #求海马部分
            # R2 = r2_score(hip_label, hip_predict)
            # cor = stats.pearsonr(hip_label, hip_predict)[0]
            # mse = mean_squared_error(hip_label, hip_predict)
            # psnr = peak_signal_noise_ratio(hip_label, hip_predict,data_range=max(hip_label.max(), hip_predict.max()))
            # ssim = structural_similarity(hip_label, hip_predict, win_size=3,data_range=max(hip_label.max(), hip_predict.max()))


            print(R2,cor,mse,psnr,ssim)
        else:
            R2 = -1
            cor = -1
            mse = -1
            psnr = -1
            ssim = -1
        lst.append([file,R2,cor,mse,psnr,ssim])

    data2 = pd.DataFrame(data=lst, index=None)
    mean_df = data2.iloc[:, 1:].mean()
    print(mean_df)
    all.append(['mean', np.array(mean_df)[0], np.array(mean_df)[1], np.array(mean_df)[2], np.array(mean_df)[3],np.array(mean_df)[4]])


data22 = pd.DataFrame(data=all, index=None)
data22.to_csv(r'D:\63113\coronal_581\581-(log2_Min-Max Normalization(everyone))\h5(log2_Min-Max Normalization(everyone))-MAR(1940)\MAR(1940)_knn(iteration).csv')



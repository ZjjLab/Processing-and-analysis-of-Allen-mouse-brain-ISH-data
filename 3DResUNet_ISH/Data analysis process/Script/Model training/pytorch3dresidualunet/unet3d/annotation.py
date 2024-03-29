import numpy as np
import pandas as pd
import torch
import torch.nn as nn


hip_subregion = pd.read_csv(r'C:\Users\DELL\Desktop\genedata\hip_subregion_template.csv',header=0)
hip_subregion = hip_subregion.values
hip_subregion[:,0:3] = hip_subregion[:,0:3]-1
# hip_subregion = torch.from_numpy(hip_subregion)
# hip_subregion = hip_subregion.cuda()
#hip_subregion.iloc[:,0:3] = hip_subregion.iloc[:,0:3]-1
# sy_CA1 = np.where(hip_subregion.iloc[:,3]==1)
# CA1 = hip_subregion.iloc[sy_CA1[0],:]
# CA1 = CA1.iloc[:,0:3]
#
# sy_halfbrain_left = np.where(hip_subregion.iloc[:,1]<=28)
# halfbrain_left = hip_subregion.iloc[sy_halfbrain_left[0],:]
# halfbrain_left = halfbrain_left.iloc[:,0:3]

#class annotation:

def subregion(data, region,output,target):
    sy = np.where(data[:, 3] == region)#torch.nonzero(data == region)
    data1 = data[sy[0], :]
    data2 = np.array((data1[:, 0:3]))
    data2 = torch.from_numpy(data2)
    data2 = data2.cuda()
    col = data2[:, 0]
    col1 = data2[:, 0]
    col = col.to(torch.float32)
    col1 = col1.to(torch.float32)
    for i in range(data2.shape[0]):
        col[i] = output[0, 0, data2[i][2], data2[i][1], data2[i][0]]
        col1[i] = target[0, 0, data2[i][2], data2[i][1], data2[i][0]]
    return col,col1

# def halfbrain_left(data,output,target):
#     sy = np.where(data.iloc[:,1]<=28)
#     data1 = data.iloc[sy[0], :]
#     data2 = data1.iloc[:, 0:3]
#     col = []
#     col1 = []
#     for i in range(np.size(data2, 0)):
#         col.append(output[data2[i][0], data2[i][1], data2[i][2]])
#         col1.append(target[data2[i][0], data2[i][1], data2[i][2]])
#     return col, col1
#
# def halfbrain_right(data,output,target):
#     sy = np.where(data.iloc[:,1]>28)
#     data1 = data.iloc[sy[0], :]
#     data2 = data1.iloc[:, 0:3]
#     col = []
#     col1 = []
#     for i in range(np.size(data2, 0)):
#         col.append(output[data2[i][0], data2[i][1], data2[i][2]])
#         col1.append(target[data2[i][0], data2[i][1], data2[i][2]])
#     return col, col1




# if __name__ == '__main__':
#     result = expression_values()
#     print(result)
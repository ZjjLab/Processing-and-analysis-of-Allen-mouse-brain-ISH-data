clear;clc;

%[filename,pathname]=uigetfile({'*.*';'*.jpg';'*.tif';'*.bmp';'*.png'},'File Selector');
%a=importdata('*.txt');
%sy = importdata("C:/Users/wangtong1/Desktop/structer_id-2.txt");
%for i =1 : 13
    %a = sy{i,1};
%sy1=sy.textdata;%%%文件中的非数字
    %mask = ReadTiff(strcat("C:/Users/wangtong1/Desktop/Tissue/photo/",a,'.tif'));
list1 = ["P4";"P14";"P28";"P56"];
for l = 1:4
mask = ReadTiff(strcat("C:\Users\wangtong1\Desktop\developing_mouse geneexpression_1\gridAnnotation\",list1(l,:),"_DevMouse2012_gridAnnotation\gridAnnotation.tif"));
mask(mask>0)=1; %将A中等于x的值全部替换为X
% mask = mask>0;

processFolder = strcat('C:\Users\wangtong1\Desktop\developing_mouse geneexpression_1\',list1(l,:),'\');%转换后tif数据文件放入此目录
%savingFolder = 'C:\Users\wangtong1\Desktop\P56_DevMouse2012_gridAnnotation\';%输出xlsx文件目录
filefolder = ls(processFolder);
[m,~] = size(filefolder);
    for i = 3:m
        fileList = strcat(processFolder,filefolder(i,:),'\energy.tif');
        data = ReadTiff(fileList);
        out = data.*mask;
        outName = strcat(processFolder,filefolder(i,:),'\energy.mat');
        %outName = 'F:\allen_brain_data\3_include=energy,intensity,density\energy-ECT.mat';
        save(outName,'out');
    end
end

% for i = 5 : 5
%     fileList = strcat(processFolder,filefolder(i,:),'\energy.tif');
%     data = ReadTiff(fileList);
%     out = data.*mask;
%     outName = strcat(processFolder,filefolder(i,:),'\energy-DG.mat');
%     save(outName,'out');
% 
%     %     outName = strcat(processFolder,filefolder(i,:),'\energy-brain.xlsx');
% %     writematrix(out,outName);
% end
% for i = 1 : length(fileList)
%     fileName = [processFolder, fileList(i).name];
%     data = ReadTiff(fileName);
%     out = data.*mask;
%     outName = [savingFolder , num2str(i),'.xlsx'];
%     writematrix(out,outName);
% end
library(data.table)
library(parallel)
library(rhdf5)


###0
q.coronal <- as.data.frame(fread('D:/analysis data/brain-energy-coronal-1.csv'))
q.coronal <- q.coronal[,-2:-1]
q.coronal.hip <- q.coronal[which(q.coronal[,1]%in%c(30:49)),]
brain_position <- q.coronal.hip[,1:3]
q.coronal.hip_1 <- q.coronal.hip[,-3:-1]




#统计基因的缺失模式后生成随机缺失数据
hip.subregion <- as.data.frame(fread('C:/Users/DELL/Desktop/hip_subregion_template.csv'))

CA1 <- hip.subregion[which(hip.subregion$V4==1),]
CA2 <- hip.subregion[which(hip.subregion$V4==2),]
CA3 <- hip.subregion[which(hip.subregion$V4==3),]
DG <- hip.subregion[which(hip.subregion$V4==4),]

for (hh in 1:20){
  
  fu <- function(xx){
    setwd(paste('D:/63113/coronal_421/421-(log2_Min-Max Normalization(everyone))/h5(log2_Min-Max Normalization(everyone))-MAR(1609)_test'))
    library(parallel)
    library(rhdf5)
    library(data.table)
    h5f <- H5Fopen(paste('D:/63113/coronal_421/421-(log2_Min-Max Normalization(everyone))/h5(log2_Min-Max Normalization(everyone))/0-',xx,'.h5',sep = ''))
    h5f.data <- h5f$label
    h5f.data1 <- h5f$label

    data.zero <- as.data.frame(matrix(data = 0,nrow = 67,ncol=2378))
    x1 <- array(unlist(data.zero),dim=c(67,58,41))
    x2 <- array(unlist(data.zero),dim=c(67,58,41))
    x3 <- array(unlist(data.zero),dim=c(67,58,41))
    x4 <- array(unlist(data.zero),dim=c(67,58,41))
    
    data.one <- as.data.frame(matrix(data = 1,nrow = 67,ncol=2378))
    y <- array(unlist(data.one),dim=c(67,58,41))
    
    #挑1838其中一种缺失模式
    lon <- sample(1:1598, 1)
    mask <- q.coronal.hip_1[,lon]
    
    for (i in 1:28224) {
      y[brain_position[i,1],brain_position[i,2],brain_position[i,3]] <- mask[i]
    }
    y <- y[30:49,1:58,1:41]
  
    h5f.data1 <- h5f.data1*y
    
    for (l1 in 1:dim(CA1)[1]) {
      x1[CA1[l1,1],CA1[l1,2],CA1[l1,3]] <- 1}
    x1 <- x1[30:49,1:58,1:41]
    
    for (l2 in 1:dim(CA2)[1]) {
      x2[CA2[l2,1],CA2[l2,2],CA2[l2,3]] <- 1}
    x2 <- x2[30:49,1:58,1:41]
    
    for (l3 in 1:dim(CA3)[1]) {
      x3[CA3[l3,1],CA3[l3,2],CA3[l3,3]] <- 1}
    x3 <- x3[30:49,1:58,1:41]
    
    for (l4 in 1:dim(DG)[1]) {
      x4[DG[l4,1],DG[l4,2],DG[l4,3]] <- 1}
    x4 <- x4[30:49,1:58,1:41]
    
    
    
    
    h5createFile(paste(hh,'-0-',xx,'.h5',sep = ''))
    h5createDataset(paste(hh,'-0-',xx,'.h5',sep = ''), "label",c(20,58,41), storage.mode = "double", level=7)
    h5write(h5f.data, file=paste(hh,'-0-',xx,'.h5',sep = ''), name="label")
    h5createDataset(paste(hh,'-0-',xx,'.h5',sep = ''), "raw",c(20,58,41), storage.mode = "double", level=7)
    h5write(h5f.data1, file=paste(hh,'-0-',xx,'.h5',sep = ''), name="raw")
    
    h5createDataset(paste(hh,'-0-',xx,'.h5',sep = ''), "CA1",c(20,58,41), storage.mode = "double", level=7)
    h5write(x1, file=paste(hh,'-0-',xx,'.h5',sep = ''), name="CA1")
    
    h5createDataset(paste(hh,'-0-',xx,'.h5',sep = ''), "CA2",c(20,58,41), storage.mode = "double", level=7)
    h5write(x2, file=paste(hh,'-0-',xx,'.h5',sep = ''), name="CA2")
    
    h5createDataset(paste(hh,'-0-',xx,'.h5',sep = ''), "CA3",c(20,58,41), storage.mode = "double", level=7)
    h5write(x3, file=paste(hh,'-0-',xx,'.h5',sep = ''), name="CA3")
    
    h5createDataset(paste(hh,'-0-',xx,'.h5',sep = ''), "DG",c(20,58,41), storage.mode = "double", level=7)
    h5write(x4, file=paste(hh,'-0-',xx,'.h5',sep = ''), name="DG")
    
    h5createDataset(paste(hh,'-0-',xx,'.h5',sep = ''), "MASK",c(20,58,41), storage.mode = "double", level=7)
    h5write(y, file=paste(hh,'-0-',xx,'.h5',sep = ''), name="MASK")
    
    h5closeAll()
  }
  cl.cores <- detectCores()
  cl <- makeCluster(45)
  clusterExport(cl,c('CA1','CA2','CA3','DG','brain_position','hh','q.coronal.hip_2'),envir = environment())  #'sy1',
  res <- parLapply(cl, 1:421 ,fu)
  stopCluster(cl)
}


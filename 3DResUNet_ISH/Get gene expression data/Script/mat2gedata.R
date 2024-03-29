rm(list = ls())
library(openxlsx)
library(data.table)
library(R.matlab)



###基因表达数据提取三维坐标

coll <- NULL
col <- NULL
a <- read.table(file = 'C:/Users/wangtong1/Desktop/Tissue/id/sagittalid.txt',quote = "")
for (l in c(1:21717)) {
  pathname<-file.path(paste('F:/allen_brain_data/',a[l,1],'_include=energy,intensity,density/','energy-hip.mat',sep=''))
  data <- as.data.frame(readMat(pathname))
  collist <- NULL
  
  for (i in c(1:ncol(data))) {
    if(length(unique(data[,i]))>1){
      collist <- c(collist,i)
      }
  }
  
  if(length(collist) > 1){
    b <- data[,collist]
    colnames(b) <- gsub('X','',colnames(b)) 
    b$Row.names <- rownames(b) 
    c <- stack(b[,-(length(collist)+1)])
    c$z <- rep(b$Row.names,length(collist)) #z 水平面
    d <- NULL
    
    c$y <- floor(as.numeric(as.character(c$ind))/67) #y 矢状面
    c$x <- as.numeric(as.character(c$ind))%%67 # x 冠状面
    data2 <- c[which(rowSums(c==0)==0),-2]
    data2 <- data2[which(data2$y %in% c(9:28)),]#因矢状切片不一致而限定范围
    if(length(unique(data2[,1]))>1){
      data3 <- data2[which(data2$values!=-1.000000),]
      col <- c(col,l)
    }
  }else{
    coll <- c(coll,l)
  }
}
write.table(col,'C:/Users/wangtong1/Desktop/sample3-sy.txt',row.names = F)


#对全脑表达数据进行整合
data5<- read.csv(paste('F:/allen_brain_data/',155,'_include=energy,intensity,density/sample2-brain.csv',sep = ''))

q <- as.data.frame(matrix(data = NA,nrow = 63113,ncol = 3))
q[,1:3] <- data5[,3:5]
colnames(q) <- colnames(data5)[3:5]
#a <- read.table(file = 'F:/list1.txt',quote = "")
for (l in 1:4345){
  data<- fread(paste('F:/allen_brain_data/',b[l,],'_include=energy,intensity,density/sample2-brain.csv',sep = ''))
  dd <- data
  names(dd)[2] <- a[l,1]
  q <- merge(q,dd[,-1],by=c("x","y","z"),all.x=TRUE)
}
colnames(q)[4:4348] <- unlist(b)
write.csv(q,'E:/allen_brain_data/brain-energy-coronal-1.csv')

  





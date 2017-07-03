# where am i 
info = Sys.info()
os = info[["sysname"]]
data_file_name = "undef"
login = info[["login"]]


#load data
if(identical(os, "Windows")){
  #-Windows
  data_file_name = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\cb_data.csv", sep="")
  
}else{
  ##-Linux
  ## not functionnal for now
  data <- read.csv("/home/foulquier/Bureau/SpellCraft/WorkSpace/SCRIPTS/data/clinical_data_phase_1.csv", stringsAsFactors=TRUE)
}

## Load Data
data <- read.csv(data_file_name, stringsAsFactors=TRUE, sep=",")



##------------##
## Imputation ##
##------------##

##-------------------------##
## Scaling data before PCA ##
##-------------------------##

## Pareto scaling
library(MetabolAnalyze)
data_scaled <- scaling(data, type = "pareto")
data_scaled$X.Clinical.Sampling.OMICID <- data$X.Clinical.Sampling.OMICID
data_scaled$X.Clinical.Diagnosis.DISEASE <- data$X.Clinical.Diagnosis.DISEASE

## log transform 
log.ir <- log(data_scaled[, 3:length(data_scaled)])
ir.labels <- data$X.Clinical.Diagnosis.DISEASE 

##-------------##
## Perform PCA ##
##-------------##

## apply PCA
ir.pca <- prcomp(log.ir)
summary(ir.pca)
round(cor(log.ir[,3:length(log.ir)]), 2)

## PCA on unscaled data
ir.pca <- prcomp(data)
summary(ir.pca)
round(cor(log.ir[,3:length(log.ir)]), 2)


##-----------------##
## Display Results ##
##-----------------##

## Plot stuff
library(ggfortify)
plot(ir.pca, type = "l")

autoplot(ir.pca, data = data, colour = 'X.Clinical.Diagnosis.DISEASE',
         loadings = TRUE, loadings.colour = 'blue',
         loadings.label = TRUE, loadings.label.size = 3)



## TEST
library(pca3d)
pca <- prcomp(log.ir, scale.=TRUE) # real
gr <- factor(data$X.Clinical.Diagnosis.DISEASE) # real
summary(gr)
pca3d(pca, group=gr)

## same stuff with ellipses
pca3d(pca, group=gr, show.ellipses=TRUE,
      ellipse.ci=0.75, show.plane=FALSE)

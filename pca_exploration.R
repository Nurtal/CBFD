##----------------------------------##
## Perform and Display PCA analysis ##
##----------------------------------##

## where am i 
info = Sys.info()
os = info[["sysname"]]
data_file_name = "undef"
login = info[["login"]]

## Load data on Windows
if(identical(os, "Windows")){
  
  ## input file name
  data_file_name = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\pca_exploration\\pca_exploration_input.csv", sep="")
  
  ## output file name
  png_file_1 = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\pca_exploration\\explain_variance.png", sep="")
  png_file_2 = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\pca_exploration\\2d_representation.png", sep="")
}


data = read.csv(data_file_name, stringsAsFactors=FALSE, sep=",")

## Deal with the ID
drops <- c("identifiant")
data <- data[ , !(names(data) %in% drops)]

## Perform PCA
all.pca <- prcomp(data)


##-----------------##
## Display Results ##
##-----------------##
library(ggfortify)

## Plot components information
png(filename=png_file_1)
plot(all.pca, type = "l")
dev.off()

## Plot space representation
png(filename=png_file_2)
autoplot(all.pca, data = data,
         loadings = TRUE, loadings.colour = 'blue',
         loadings.label = TRUE, loadings.label.size = 3)
dev.off()
##----------------------------------##
## Perform and Display PCA analysis ##
##----------------------------------##


## Load data on Windows
if(identical(os, "Windows")){
  ## output file name
  all_data_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\cb_data_complete.csv", sep="")
  absolute_data_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\cb_data_absolute_complete_log_scaled.csv", sep="")
  proportion_data_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\cb_data_proportion_complete.csv", sep="")
}
all_data <- read.csv(all_data_file, stringsAsFactors=FALSE, sep=",")
absolute_data <- read.csv(absolute_data_file, stringsAsFactors=TRUE, sep=",")
proportion_data <- read.csv(proportion_data_file, stringsAsFactors=TRUE, sep=",")

## Deal with the ID
drops <- c("identifiant")
all_data <- all_data[ , !(names(all_data) %in% drops)]
absolute_data <- absolute_data[ , !(names(absolute_data) %in% drops)]
proportion_data <- proportion_data[ , !(names(proportion_data) %in% drops)]

## Perform PCA
all.pca <- prcomp(all_data)
summary(all.pca)

absolute.pca <- prcomp(absolute_data)
summary(absolute.pca)

proportion.pca <- prcomp(proportion_data)
summary(proportion.pca)



##-----------------##
## Display Results ##
##-----------------##
library(ggfortify)

## Plot components information
plot(all.pca, type = "l")
plot(absolute.pca, type = "l")
plot(proportion.pca, type = "l")

## Plot space representation
autoplot(all.pca, data = all_data,
         loadings = TRUE, loadings.colour = 'blue',
         loadings.label = TRUE, loadings.label.size = 3)

autoplot(absolute.pca, data = absolute_data,
         loadings = TRUE, loadings.colour = 'blue',
         loadings.label = TRUE, loadings.label.size = 3)

autoplot(proportion.pca, data = proportion_data,
         loadings = TRUE, loadings.colour = 'blue',
         loadings.label = TRUE, loadings.label.size = 3)

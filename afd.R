##-----------------------##
## AFD TESTS IN PROGRESS ##
##-----------------------##


## where am i 
info = Sys.info()
os = info[["sysname"]]
data_file_name = "undef"
login = info[["login"]]

## load data on Windows
if(identical(os, "Windows")){
  input_data_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\exploration\\LDA_input.csv", sep="")  
  log_data_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\exploration\\LDA_output.log", sep="")
  png_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\exploration\\LDA_image.png", sep="")
  
}
input_data = read.csv(input_data_file, stringsAsFactors=TRUE, sep=",")


##---------------##
## Run LDA (AFD) ##
##---------------##
library(MASS)

r <- lda(formula = DISEASE_SUGGESTION ~ ., 
         data = input_data[,2:18])

prop = r$svd^2/sum(r$svd^2)

##----------------##
## Write log file ##
##----------------##
write.csv(prop, file = log_data_file)
png(filename=png_file)
plot(r)
dev.off()


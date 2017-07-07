##---------------------##
## Clean The Input data##
##---------------------##

## Where am i 
info = Sys.info()
os = info[["sysname"]]
data_file_name = "undef"
login = info[["login"]]

## Load data on Windows
if(identical(os, "Windows")){
  
  ## input file name
  all_data_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\cb_data.csv", sep="")
  absolute_data_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\cb_data_absolute.csv", sep="")
  proportion_data_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\cb_data_proportion.csv", sep="")

  ## output file name
  complete_all_data_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\cb_data_complete.csv", sep="")
  complete_absolute_data_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\cb_data_absolute_complete.csv", sep="")
  complete_proportion_data_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\cb_data_proportion_complete.csv", sep="")
}
all_data <- read.csv(all_data_file, stringsAsFactors=TRUE, header=TRUE, sep=",")
absolute_data <- read.csv(absolute_data_file, stringsAsFactors=TRUE, sep=",")
proportion_data <- read.csv(proportion_data_file, stringsAsFactors=TRUE, sep=",")

## Format total a few columns
all_data$Lymphocytes..L..totaux <- as.numeric(as.character(all_data$Lymphocytes..L..totaux))
absolute_data$Lymphocytes..L..totaux <- as.numeric(as.character(absolute_data$Lymphocytes..L..totaux))
proportion_data$Lymphocytes..L..totaux <- as.numeric(as.character(proportion_data$NK.NAIF.CYTOTOX.CD3.CD16..CD56....))

## Remove patients with NA values
all_data <- all_data[complete.cases(all_data),]
absolute_data <- absolute_data[complete.cases(absolute_data),]
proportion_data <- proportion_data[complete.cases(proportion_data),]

## Remove specific patient
all_data<-all_data[!(all_data$identifiant=="350"),]
absolute_data<-absolute_data[!(absolute_data$identifiant=="350"),]
proportion_data<-proportion_data[!(proportion_data$identifiant=="350"),]

all_data<-all_data[!(all_data$identifiant=="1230"),]
absolute_data<-absolute_data[!(absolute_data$identifiant=="1230"),]
proportion_data<-proportion_data[!(proportion_data$identifiant=="1230"),]


## Write complete cases into new files
write.table(all_data, complete_all_data_file, sep=",")
write.table(absolute_data, complete_absolute_data_file, sep=",")
write.table(proportion_data, complete_proportion_data_file, sep=",")

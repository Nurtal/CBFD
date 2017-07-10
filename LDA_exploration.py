"""
Master script for the exploration
of cb data using an genomic algorithm and
linear discriminant analysis (LDA) as a score.
"""
import math
import random
import shutil
import os
import glob
import heapq


def create_individual(input_file, output_file):
	"""
	-> Add a column to the data from the input_file and write
	   the new data in output_file
	-> The new data is a "disease suggestion", i.e a random proposition
	   for a diagnostic between two possibility:
	   		- CONTROL
	   		- SICK
	"""

	input_data = open(input_file, "r")
	output_data = open(output_file, "w")

	cmpt = 0
	for line in input_data:
		line = line.split("\n")
		line = line[0]		
		line_to_write = ""
		if(cmpt == 0):
			line_to_write = line+",\"DISEASE_SUGGESTION\""
		else:
			suggestions = ["CONTROL", "SICK", "UNDEF"]
			disease_suggestion = suggestions[random.randint(0,2)]
			line_to_write = line+",\""+str(disease_suggestion)+"\""		
		output_data.write(line_to_write+"\n")

		cmpt +=1

	output_data.close()
	input_data.close()

def generate_random_population(size, source_file, output_directory):
	"""
	-> Generate a random population, i.e a batch of csv files in the
	   output_directory.

	"""

	for x in xrange(1, size+1):
		individual_name = output_directory+"/individu_"+str(x)+".csv"
		create_individual(source_file, individual_name)



def score(individual):
	"""
	-> Compute the score for a given individual (individual is
		a csv file name)
	-> the score is the amount of the between-group variance
	   that is explained by the first linear discriminant (so it's
	   	a value between 0 and 1)
	-> return the score as a float values
	-> return -1 if can't find a score in log data.
	"""
	score = -1

	## copy the individu to input dor the R script
	shutil.copy(individual, "data/exploration/LDA_input.csv")

	## Run the R script
	os.system("Rscript afd.R")

	## Read the log file
	log_data = open("data/exploration/LDA_output.log", "r")
	cmpt = 0
	for line in log_data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		if(line_in_array[0] == "\"1\""):
			score = line_in_array[1]
		cmpt +=1
	log_data.close()

	## Return score
	return float(score)



def select_best_individual(population_folder, size):
	"""
	-> select best individual from a population, the score
	   of each individual is compute from the score function
	-> write a log file
	-> return list of file name
	"""
	## List all the individu
	indPath_to_score = {}
	list_of_ind = glob.glob(str(population_folder)+"/*.csv")

	## Compute score for each individu
	for ind in list_of_ind:
		indPath_to_score[ind] = float(score(ind))

	## Select the best individu
	list_of_selected = []
	best_scores = heapq.nlargest(size, indPath_to_score.values())
	for ind in indPath_to_score.keys():
		if(indPath_to_score[ind] in best_scores):
			if(len(list_of_selected) < size):
				list_of_selected.append(ind)

	## Save selected individual
	for selected_file in list_of_selected:
		destination_file = selected_file.split("\\")
		destination_file = destination_file[-1]
		destination_file = "data/selected/"+str(destination_file)
		selected_file = selected_file.replace("\\", "/")
		shutil.copy(selected_file, destination_file)

	## Write population log
	log_data = open(str(population_folder)+"/data.log", "w")
	for key in indPath_to_score.keys():
		log_line = str(key) + "," +str(indPath_to_score[key])+"\n"
		log_data.write(log_line)
	log_data.close()

	return list_of_selected



##TEST SPACE##
generate_random_population(10, "data/cb_data_absolute_complete_log_scaled.csv", "data/population")
#machin = score("data/population/individu_1.csv")

select_best_individual("data/population", 4)

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
import sys

def create_individual(input_file, output_file):
	"""
	-> Add a column to the data from the input_file and write
	   the new data in output_file
	-> The new data is a "disease suggestion", i.e a random proposition
	   for a diagnostic between three possibility:
	   		- CONTROL
	   		- SICK
	   		- UNDEF
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
	os.system("Rscript afd.R > trash.txt")

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
	-> save the images in the images folder
	-> write a log file
	-> return list of file name
	"""
	## List all the individu
	indPath_to_score = {}
	list_of_ind = glob.glob(str(population_folder)+"/*.csv")

	## Compute score for each individu
	## save image in data/images folder
	progress = 0
	for ind in list_of_ind:
		ind_in_array = ind.split(".")
		ind_in_array = ind_in_array[0]
		ind_in_array = ind_in_array.split("_")
		ind_number = ind_in_array[-1]
		indPath_to_score[ind] = float(score(ind))
		image_destination_file = "data/images/LDA_ind_"+str(ind_number)+".png"
		shutil.copy("data/exploration/LDA_image.png", image_destination_file)

		## Display progress bar
		# progress bar
		step = float((100/float(len(list_of_ind))))
		progress += 1
		progress_perc = progress*step
		factor = math.ceil((progress_perc/2))
		progress_bar = "#" * int(factor)
		progress_bar += "-" * int(50 - factor)
		display_line = "["+str(ind_number)+"]|"+progress_bar+"|"+str(progress)+"/"+str(len(list_of_ind))+"|"
		sys.stdout.write("\r%d%%" % progress_perc)
		sys.stdout.write(display_line)
		sys.stdout.flush()

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




def complete_log_file(generation, log_file_name):
	"""
	-> complete the general log file log_file_name with
	   the data of the current population
	-> generation is an int, the number of the current generation
	"""

	## test if file already exist
	if(os.path.isfile(log_file_name)):

		## write generation log data into general log file
		generation_log_file = open("data/population/data.log")
		for line in generation_log_file:
			line = line.split("\n")
			line = line[0]
			line_in_array = line.split(",")
			line_to_write = ""
			ind_name = line_in_array[0].split("\\")
			ind_name = ind_name[-1]
			line_to_write = str(generation)+","+str(ind_name)+","+str(line_in_array[-1])
			log_file = open(log_file_name, "a")
			log_file.write(line_to_write+"\n")
			log_file.close()
		generation_log_file.close()

	else:
		## write generation log data into general log file
		generation_log_file = open("data/population/data.log")
		for line in generation_log_file:
			line = line.split("\n")
			line = line[0]
			line_in_array = line.split(",")
			line_to_write = ""
			ind_name = line_in_array[0].split("\\")
			ind_name = ind_name[-1]
			line_to_write = str(generation)+","+str(ind_name)+","+str(line_in_array[-1])
			log_file = open(log_file_name, "w")
			log_file.write(line_to_write+"\n")
			log_file.close()
		generation_log_file.close()






def select_bad_individual(size):
	"""
	-> select bad individuals from the population, i.e indiviuals not
	   present in the "selected" folder.
	-> size is an int, the number of bad ind to select
	-> copy the selected ind in "bad_selection" folder
	-> return the list of selected files
	"""
	## list of selected ID
	selected_id = []
	selected_files = glob.glob("data/selected/*.csv")
	for selected_file in selected_files:
		selected_file_in_array = selected_file.split(".")
		selected_file_in_array = selected_file_in_array[0]
		selected_file_in_array = selected_file_in_array.split("_")
		ind_id = selected_file_in_array[-1]
		selected_id.append(ind_id)

	## select bad individual
	bad_individuals = []
	population_files = glob.glob("data/population/*.csv")
	while(len(bad_individuals) < size):

		random_suggestion = population_files[random.randint(0, len(population_files)-1)]
		suggestion_id = random_suggestion.split(".")
		suggestion_id = suggestion_id[0]
		suggestion_id = suggestion_id.split("_")
		suggestion_id = suggestion_id[-1]

		if(suggestion_id not in selected_id and suggestion_id not in bad_individuals):
			bad_individuals.append(random_suggestion)
			shutil.copy(random_suggestion, "data/bad_selection/individual_"+str(suggestion_id)+".csv")

	return bad_individuals


def clean(target):
	"""
	-> Clean folders
	-> target is the targeted folder, could be:
		- population
		- selected
		- bad_selection
		- parents
		- children
		- images
		- all
	"""

	## Clean population folder
	if(target == "population" or target == "all"):
		population_files = glob.glob("data/population/*.csv")
		for pop_file in population_files:
			os.remove(pop_file)

	## Clean selected folder
	if(target == "selected" or target == "all"):
		population_files = glob.glob("data/selected/*.csv")
		for pop_file in population_files:
			os.remove(pop_file)

	## Clean bad_selection folder
	if(target == "bad_selection" or target == "all"):
		population_files = glob.glob("data/bad_selection/*.csv")
		for pop_file in population_files:
			os.remove(pop_file)

	## Clean parents folder
	if(target == "parents" or target == "all"):
		population_files = glob.glob("data/parents/*.csv")
		for pop_file in population_files:
			os.remove(pop_file)

	## Clean children folder
	if(target == "children" or target == "all"):
		population_files = glob.glob("data/children/*.csv")
		for pop_file in population_files:
			os.remove(pop_file)

	## Clean images folder
	if(target == "images" or target == "all"):
		population_files = glob.glob("data/images/*.csv")
		for pop_file in population_files:
			os.remove(pop_file)



def assemble_parents():
	"""
	-> copy selected ind from good and bad selection to
	   the parents folder.
	"""

	## Get the good individual
	good_selection = glob.glob("data/selected/*.csv")
	for ind in good_selection:
		destination = ind.split("\\")
		destination = destination[-1]
		destination = "data/parents/"+destination
		shutil.copy(ind, destination)

	## Get the bad individual
	bad_selection = glob.glob("data/bad_selection/*.csv")
	for ind in bad_selection:
		destination = ind.split("\\")
		destination = destination[-1]
		destination = "data/parents/"+destination
		shutil.copy(ind, destination)


def mutation(mutation_rate):
	"""
	-> Perform mutations on parents
	-> i.e change the diagnostic for a random number of patients
	   (max 100) in the cohorte file representing the individu
	-> mutation only trigger if a random generated number is lower
	   than the mutation rate.
	-> mutation rate is an int between 0 and 100
	"""

	## Get list of parents
	parents_file = glob.glob("data/parents/*.csv")
	
	## Perform mutation
	for parent in parents_file:
		if(random.randint(0,100) <= mutation_rate):
			
			tmp_file = parent.split(".")
			tmp_file = tmp_file[0]+"_tmp.csv"
			shutil.copy(parent, tmp_file)

			## Nombre de position a muter
			number_of_position_to_mutate = random.randint(1, 100)

			## Nombre de position dans le fichier
			## (i.e nombre de ligne - header)
			number_of_position = -1
			parent_data = open(tmp_file, "r")
			for line in parent_data:
				number_of_position += 1
			parent_data.close()

			## Position of mutations
			position_to_mutate = []
			for x in xrange(0, number_of_position_to_mutate):
				
				valid_position = False
				while(not valid_position):
					pos_suggested = random.randint(2, number_of_position)

					if(pos_suggested not in position_to_mutate):
						position_to_mutate.append(pos_suggested)
						valid_position = True

			## Perfrom the mutation
			pos_in_file = 0
			possible_diag = ["\"UNDEF\"", "\"SICK\"", "\"CONTROL\""]
			tmp_data = open(tmp_file, "r")

			parent_data = open(parent, "w")

			for line in tmp_data:
				line = line.split("\n")
				line = line[0]
				line_in_array = line.split(",")

				line_to_write = ""

				if(pos_in_file in position_to_mutate):
					for scalar in line_in_array[:-1]:
						line_to_write+=str(scalar)+","

					new_diag = possible_diag[random.randint(0,2)]
					line_to_write += new_diag
				else:
					line_to_write = line
				parent_data.write(line_to_write+"\n") 
				pos_in_file += 1

			parent_data.close()
			tmp_data.close()

			## delete tmp file
			os.remove(tmp_file)




def get_youngest_id_in_population():
	"""
	-> return the youngest member's id (i.e last generated)
	   from a population.
	"""
	population_id = []
	population = glob.glob("data/population/*.csv")
	for ind in population:
		ind_in_array = ind.split(".")
		ind_in_array = ind_in_array[0]
		ind_in_array = ind_in_array.split("_")
		ind_id = ind_in_array[-1]
		population_id.append(int(ind_id))
	return max(population_id)




def create_children():
	"""
	-> Compute the number of children needed to
	   create a new population (i.e population size - parents)
	-> Create the corresping number of children using a crossing
	   over between parents.
	"""

	## Get the number of children to create
	population = glob.glob("data/population/*.csv")
	parents = glob.glob("data/parents/*.csv")
	number_of_children = len(population) - len(parents)
	
	children = []
	child_id = get_youngest_id_in_population() + 1

	while(len(children) < number_of_children):
		
		## Define the couples amoung parents
		male = random.randint(0, len(parents)-1)
		female = random.randint(0, len(parents)-1)
		if(male != female):
			male = parents[male]
			female = parents[female]

			## Define the separation for the crossing over
			number_of_position = -1
			parent_data = open(male, "r")
			for line in parent_data:
				number_of_position += 1
			parent_data.close()
			half = number_of_position / 2

			## Child creation
			child_file_name = "data/children/individu_"+str(child_id)+".csv"

			## Legacy from father
			pos_in_father_file = 0
			father_file = open(male, "r")
			child_file = open(child_file_name, "w")
			for line in father_file:
				if(pos_in_father_file <= half):
					child_file.write(line)
				pos_in_father_file += 1
			child_file.close()
			father_file.close()

			## Legacy from mother
			pos_in_mother_file = 0
			mother_file = open(female, "r")
			child_file = open(child_file_name, "a")
			for line in mother_file:
				if(pos_in_mother_file > half):
					child_file.write(line)
				pos_in_mother_file += 1
			child_file.close()
			mother_file.close()

			children.append(child_file_name)
			child_id += 1



def assemble_new_population():
	"""
	-> clean the population folder and
	   copy the individual in parents and
	   children folder to the population folder
	"""

	## Clean the output folder
	clean("population")

	## Gather the parents and children
	parents = glob.glob("data/parents/*.csv")
	for ind in parents:
		destination = ind.split(".")
		destination = destination[0]
		destination = destination.split("\\")
		destination = destination[-1]
		destination = "data/population/"+destination+".csv"
		shutil.copy(ind, destination)
	children = glob.glob("data/children/*.csv")
	for ind in children:
		destination = ind.split(".")
		destination = destination[0]
		destination = destination.split("\\")
		destination = destination[-1]
		destination = "data/population/"+destination+".csv"
		shutil.copy(ind, destination)


def run_exploration():
	"""
	-> The main procedure, fonctionnal but room for improvements

	IN PROGRESS
	"""

	## Fix parameters
	max_number_of_generation = 200
	population_size = 25
	good_selection_number = 11
	bad_selection_number = 4
	mutation_rate = 15
	log_file_name = "data/log/scores.log"

	## really important, model for the individual
	input_data_file = "data/cb_data_absolute_complete_log_scaled.csv"
	
	## Generate first population
	## clean all the folder
	clean("all")
	log_files = glob.glob("data/log/*")
	for log in log_files:
		os.remove(log)
	generate_random_population(population_size, input_data_file, "data/population")

	## Evolution
	for x in xrange(1, max_number_of_generation+1):
		print "[*] ======== Generation "+str(x) +" ======== [*]"

		## Select the best candidates
		print "[+] Scoring the candidate"
		select_best_individual("data/population", good_selection_number)

		## Write results in log file
		complete_log_file(x, log_file_name)

		## Select the bad candidates
		select_bad_individual(bad_selection_number)

		## assemble the parents in "parents" folder
		assemble_parents()
		print "\n[+] Parents selected"

		## Mutation of the parents before reproduction
		print "[+] Perform mutation on parents"
		mutation(mutation_rate)

		## Reproduction, generate children
		print "[+] Create Children"
		create_children()

		## Assemble new population
		print "[+] Assemble new population"
		assemble_new_population()

		## Cleaning
		print "[+] Cleaning"
		clean("parents")
		clean("children")
		clean("selected")
		clean("bas_selection")




##TEST SPACE##
run_exploration()
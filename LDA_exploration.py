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
	-> save the images in the images folder
	-> write a log file
	-> return list of file name
	"""
	## List all the individu
	indPath_to_score = {}
	list_of_ind = glob.glob(str(population_folder)+"/*.csv")

	## Compute score for each individu
	## save image in data/images folder
	for ind in list_of_ind:
		ind_in_array = ind.split(".")
		ind_in_array = ind_in_array[0]
		ind_in_array = ind_in_array.split("_")
		ind_number = ind_in_array[-1]
		indPath_to_score[ind] = float(score(ind))
		image_destination_file = "data/images/LDA_ind_"+str(ind_number)+".png"
		shutil.copy("data/exploration/LDA_image.png", image_destination_file)

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





def create_children_1(parents, population):
	"""
	-> crossover between parents
	to create children
	-> parents are a list of individuals
	-> population is a list of Individuals (include parents)
	-> return a list of individuals
	"""
	parents_length = len(parents)
	desired_length = len(population) - parents_length
	children = []
	child_id = get_youngest_id_in_population(population) + 1
	while len(children) < desired_length:
		male = random.randint(0, parents_length-1)
		female = random.randint(0, parents_length-1)
		if male != female:
			male = parents[male]
			female = parents[female]

			parameters = male._intervals_to_variables.keys()
			half = len(parameters) / 2

			# child creation
			child = Individual()
			child._id = child_id

			# legacy from father
			for param in parameters[half:]:
				child._intervals_to_variables[param] = male._intervals_to_variables[param]
			
			# legacy from mother
			for param in parameters[:half]:
				child._intervals_to_variables[param] = female._intervals_to_variables[param]

			children.append(child)

		child_id += 1

		return children



##TEST SPACE##


clean("all")
generate_random_population(10, "data/cb_data_absolute_complete_log_scaled.csv", "data/population")
select_best_individual("data/population", 4)
select_bad_individual(2)
assemble_parents()
mutation(90)
create_children()
"""
TRASH FUNCTIONS
"""

import math
import random
import itertools
import glob
import shutil
import os
import sys

from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt

def log_scaled(input_file):
	"""
	-> Take input file as input,
	-> write new file containing log (log10) values of the input files
	-> Assume file is coming from a R dataFrame, i.e the first column
	   should not exist ...
	"""

	header = ""
	output_file_name = input_file.split(".csv")
	output_file_name = output_file_name[0]
	output_file_name = output_file_name+"_log_scaled.csv"

	output_data = open(output_file_name, "w")
	input_data = open(input_file, "r")

	cmpt = 0
	for line in input_data:
		new_line = ""
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		
		if(cmpt == 0):
			header = line
			output_data.write(header+"\n")
		else:
			index = 0
			for element in line_in_array:
				element = element.replace("\"", "")
				if(index > 1):
					if(float(element) >=1):
						new_element = math.log10(float(element))
					else:
						new_element = 0
					new_line += str(new_element)+","
				elif(index > 0):
					new_element = element
					new_line += str(new_element)+","
				
				index+=1
			new_line = new_line[:-1]
			output_data.write(new_line+"\n")
		cmpt += 1

	input_data.close()
	output_data.close()


def add_random_diagnostic(input_file, output_file):
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


from sklearn import preprocessing



def centre_reduire_transformation(data_file_name, output_file_name):
	"""
	-> scale the data in the data_file_name and write the
	   corresponding output in output_file_name
	"""

	## Create the data array
	data_file = open(data_file_name, "r")
	index_to_variables = {}
	variable_to_values = {}
	cmpt = 0
	for line in data_file:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		if(cmpt == 0):
			index = 0
			for variable in line_in_array:
				index_to_variables[index] = variable
				variable_to_values[variable] = []
				index += 1
		else:
			index = 0
			for scalar in line_in_array[1:]: # not taking the first row, stuff from R
				scalar = scalar.replace("\"", "")
				variable_to_values[index_to_variables[index]].append(scalar)
				index+=1
		cmpt += 1
	data_file.close()

	## Get the transformation for each variable except the ID
	for var in variable_to_values.keys():
		if(var != "\"identifiant\""):
			X = variable_to_values[var]
			X_scaled = preprocessing.scale(X, axis=0, with_mean=True, with_std=True, copy=True)
			variable_to_values[var] = X_scaled

	## Re-write file with new data
	output_data = open(output_file_name, "w")

	## write header
	header = ""
	for pos in index_to_variables.keys():
		var = index_to_variables[pos]
		header += str(var)+","

	header = header[:-1]
	output_data.write(header+"\n")

	# Write line
	for number_of_line in xrange(0, len(variable_to_values["\"identifiant\""])):
		line_to_write = ""
		for pos in index_to_variables.keys():
			var = index_to_variables[pos]
			line_to_write += str(variable_to_values[var][number_of_line]) + ","
		
		line_to_write = line_to_write[:-1]
		output_data.write(line_to_write+"\n")

	output_data.close()




def generate_proposition_file():
	"""
	-> Generate proposition file for pca & unsupervised exploration
	TODO:
		- complete the documentation
	"""

	## get the list of variables
	## store data in dict
	index_to_variables = {}
	variable_to_values = {}
	variables = []
	data_file = open("data/cb_data_absolute_complete_scaled.csv", "r")
	cmpt = 0
	for line in data_file:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		if(cmpt == 0):
			variables = line_in_array
			index = 0
			for var in line_in_array:
				index_to_variables[index] = var
				variable_to_values[var] = []
				index += 1
		else:
			index = 0
			for scalar in line_in_array:
				scalar = scalar.replace("\"", "")
				variable_to_values[index_to_variables[index]].append(scalar)
				index+=1

		cmpt += 1
	data_file.close()
	variables.remove("\"identifiant\"")

	cmpt = 0
	tupleLen = 4
	while(tupleLen < len(variables)):
		for h in itertools.combinations(variables, tupleLen):
			h = list(h)
			file_name = "data/subsets/proposition_"+str(cmpt)+".csv"
			
			## Write the proposition file
			proposition_file = open(file_name, "w")
			
			## write the header
			header = ""
			header += "\"identifiant\""+","
			for prop_var in h:
				header += str(prop_var)+","
			header = header[:-1]

			proposition_file.write(header+"\n")

			## write the lines
			for number_of_line in xrange(0, len(variable_to_values["\"identifiant\""])):
				line_to_write = ""
				line_to_write += str(variable_to_values["\"identifiant\""][number_of_line]) + ","
				for pos in index_to_variables.keys():
					var = index_to_variables[pos]
					if(var in h):
						line_to_write += str(variable_to_values[var][number_of_line]) + ","
		
				line_to_write = line_to_write[:-1]
				proposition_file.write(line_to_write+"\n")
			proposition_file.close()
			print "[+] "+str(file_name)+ " written" 
			cmpt +=1
		tupleLen+=1




def pca_exploration():
	"""
	IN PROGRESS
	"""

	## get list of files
	proposition_files = glob.glob("data/subsets/*.csv")

	for proposition in proposition_files:

		## prepare data for R pca Script
		shutil.copy(proposition, "data/pca_exploration/pca_exploration_input.csv")

		## Run the R script
		os.system("Rscript pca_exploration.R > pca_trash.txt")

		## Save the output
		destination_file_1 = proposition.split("\\")
		destination_file_1 = destination_file_1[-1]
		destination_file_1 = destination_file_1.split(".")
		destination_file_1 = destination_file_1[0]
		destination_file_1 = destination_file_1 + "_explain_variance.png"
		destination_file_1 = "data/pca_exploration_results/"+destination_file_1

		destination_file_2 = proposition.split("\\")
		destination_file_2 = destination_file_2[-1]
		destination_file_2 = destination_file_2.split(".")
		destination_file_2 = destination_file_2[0]
		destination_file_2 = destination_file_2 + "_2d_representation.png"
		destination_file_2 = "data/pca_exploration_results/"+destination_file_2

		shutil.copy("data/pca_exploration/explain_variance.png", destination_file_1)
		shutil.copy("data/pca_exploration/2d_representation.png", destination_file_2)


import numpy as np
import pylab
import mahotas as mh
from PIL import Image

def image_analysis(image_file_name):
	"""
	-> Detect the number of apparent cluster in the
	   image image_file_name.
	-> preprocess the image to hav only the grid 
	   (calibrated for the figures of pca exploration procedure)
	-> return a dict with number and sizes of the clusters

	-> TODO:
			- test with an image containing at least 2 clusters
	"""

	## Init variable
	results = {}

	## Preprocessing the image
	## Extract the interesting zone
	im = Image.open(image_file_name)
	crop_rectangle = (40, 10, 470, 445)
	cropped_im = im.crop(crop_rectangle)
	blurred = gaussian_filter(cropped_im, sigma=7)
	T = mh.thresholding.otsu(blurred)
	
	## Extract number of cluster
	## Extract size of cluster
	labeled,nr_objects = mh.label(blurred > T)
	sizes = mh.labeled.labeled_size(labeled)
	results["number_of_clusters"] = int(nr_objects)
	results["sizes"] = sizes[0]

	## Show stuff
	#pylab.imshow(labeled)
	#pylab.jet()
	#pylab.show()

	return results	


def graphical_analyze():
	"""
	-> Perform graphical analysis of pca figures
	   store results in a log file

	-> TODO :
			- complete documentation
	"""

	## Init log file
	log_file = open("data/graphical_analyze.log", "w")
	log_file.write("suggestion_id,nb_clsuters,size_clusters\n")

	## get all the files to analyse
	files_to_process = glob.glob("data/pca_exploration_results/*2d_representation.png")
	for image_file_name in files_to_process:
		
		## Get the id
		suggestion_id = image_file_name.split("\\")
		suggestion_id = suggestion_id[-1]
		suggestion_id = suggestion_id.split("_")
		suggestion_id = suggestion_id[1]

		## Just for print
		print "[+] Procesing case "+str(suggestion_id)

		## Perform the analysis
		analysis_results = image_analysis(image_file_name)

		## Write results in a log file
		log_file.write(str(suggestion_id)+","+str(analysis_results["number_of_clusters"])+","+str(analysis_results["sizes"])+"\n")

	log_file.close()


def log_analyse():
	"""
	-> Analyse the log file created by the
	   graphical_analyze() function.
	-> copy images of the good candidates (i.e at least 2 clusters
	   detected on the graphe) from the pca_exploration_results folder
       to the good_candidates fodler.
	"""

	## Read log file
	## Identify the good candidates
	log_file = open("data/graphical_analyze.log", "r")
	cmpt = 0
	good_candidate = 0
	good_candidate_list = []	
	for line in log_file:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		
		case_id = line_in_array[0]
		cluster_number = line_in_array[1]
		cluster_size = line_in_array[2]

		if(cmpt != 0):
			if(int(cluster_number) > 1):
				print "[+] Find a good candidate "+str(case_id)
				good_candidate_list.append(case_id)
				good_candidate += 1
		cmpt += 1
	log_file.close()
	print "[*] Find "+str(good_candidate)

	## Copy good candidates images to
	## A new results folder
	for candidate in good_candidate_list:
		source_file = "data/pca_exploration_results/proposition_"+str(candidate)+"_2d_representation.png"
		destination_file = "data/good_candidates/"+str(candidate)+".png"
		shutil.copy(source_file, destination_file)

	print "[*] Files saved"



def write_manifeste():
	"""
	-> write manifeste.log file, a csv file
	with the id of the case/suggestion and the variables
	involved in the case/suggestion.
	"""

	## Init log file
	
	print "[+] Writing Manifeste"
	log_file = open("data/manifeste.log", "w")
	log_file.write("ID,variables\n")
	log_file.close()

	## List of files to check
	candidates_list = glob.glob("data/subsets/*.csv")
	
	## Scan the files
	progress = 0
	for candidate in candidates_list:
		
		line_to_write = ""

		candidate_id = candidate.split("\\")
		candidate_id = candidate_id[-1]
		candidate_id = candidate_id.split("_")
		candidate_id = candidate_id[1]
		candidate_id = candidate_id.split(".")
		candidate_id = candidate_id[0]

		data_file = open(candidate, "r")
		cmpt = 0
		variables = ""
		for line in data_file:
			if(cmpt == 0):
				line = line.split("\n")
				line = line[0]
				line_in_array = line.split(",")

				for var in line_in_array:
					if(str(var) != "\"identifiant\""):
						variables += str(var)+";"
				variables = variables[:-1]
			cmpt += 1

		log_file = open("data/manifeste.log", "a")
		line_to_write += str(candidate_id)+","+str(variables)
		log_file.write(line_to_write+"\n")
		log_file.close()
		data_file.close()

		## Display progress bar
		# progress bar
		step = float((100/float(len(candidates_list))))
		progress += 1
		progress_perc = progress*step
		factor = math.ceil((progress_perc/2))
		progress_bar = "#" * int(factor)
		progress_bar += "-" * int(50 - factor)
		display_line = "["+str(candidate_id)+"]|"+progress_bar+"|"+str(progress)+"/"+str(len(candidates_list))+"|"
		sys.stdout.write("\r%d%%" % progress_perc)
		sys.stdout.write(display_line)
		sys.stdout.flush()

	print "\n[*] Manifeste Done"


def write_settings(input_file_name, scaling):
	"""
	-> Write a settings file with information
	   on the pca exploration:
	   	- input_file_name the name of the file used for as input 
	   	  for the pca exploration
	    - number of variables: all variables in the file except the identifiant column
	    - variables : name of variables in the file (except the identifiant)
	    - scaling : a string, information on the data scaling
	"""

	## prompt message
	print "[+] Write Settings"

	## Open file
	log_file = open("data/settings.log", "w")
	
	## Write header
	log_file.write("##------------------------------##\n")
	log_file.write("## SETTINGS FOR PCA EXPLORATION ##\n")
	log_file.write("##------------------------------##\n")
	
	## Input file
	log_file.write("> input file:"+str(input_file_name)+"\n")

	## Number of variables
	variables_list = []
	cmpt = 0
	input_data = open(input_file_name, "r")
	for line in input_data:
		if(cmpt == 0):
			line = line.split("\n")
			line = line[0]
			line_in_array = line.split(",")
			for var in line_in_array:
				if(str(var) != "\"identifiant\""):
					variables_list.append(var)
		cmpt += 1
	input_data.close()
	log_file.write("> Number of variables:"+str(len(variables_list))+"\n")

	## Variables pool
	line_to_write = ""
	for var in variables_list:
		line_to_write += str(var) +","
	line_to_write = line_to_write[:-1]
	log_file.write("> Variables list:"+line_to_write+"\n")

	## Scaling
	log_file.write("> scaling:"+str(scaling)+"\n")

	## Close file
	log_file.close()

	print "[*] Settings Done"



def cleaner():
	"""
	-> remove csv files in data/subsets folder
	-> remove the png files in data/pca_exploration_results folder
	-> remove the png files in data/good_candidates folder 
	-> use this function at the end of a pca exploration, 
	   after saving the results in a log file
	"""

	## list files to remove
	files_to_remove = glob.glob("data/subsets/*.csv")
	image_to_remove_1 = glob.glob("data/pca_exploration_results/*.png")
	image_to_remove_2 = glob.glob("data/good_candidates/*.png")

	## delete files
	for f in files_to_remove:
		os.remove(f)
	for f in image_to_remove_1:
		os.remove(f)
	for f in image_to_remove_2:
		os.remove(f)



def save_run():
	"""
	-> copy good candidates folder and a few files:
		- data/graphical_analyze.log
		- data/manifeste.log
		- data/settings.log
	"""

	## Display something
	print "[+] Save data"

	## Get the id of the run to save
	new_id = -1
	list_of_id = []
	for folder in os.listdir("save"):
		folder_in_array = folder.split("_")
		run_number = int(folder_in_array[-1])
		list_of_id.append(run_number)
	new_id = max(list_of_id)+1

	## Create the run folder
	save_folder = "save/RUN_"+str(new_id)
	os.mkdir(save_folder)

	## Save the informations
	shutil.copytree("data/good_candidates", save_folder+"/good_candidates")
	shutil.copy("data/graphical_analyze.log", save_folder+"/graphical_analyze.log")
	shutil.copy("data/manifeste.log", save_folder+"/manifeste.log")
	shutil.copy("data/settings.log", save_folder+"/settings.log")

	## Display something
	print "[*] Data saved"



def rebuild_file_from_id(settings_file, manifeste_file, proposition_id):
	"""
	-> Rebuild a proposition file
	-> settings_file is the emplacement of the settings.log file
	-> manifeste_file is the emplacement of the manifeste.log file
	-> proposition_id is the id of the proposition to rebuild
	"""

	print "[+] Build file from proposition "+str(proposition_id)

	## Retrieve the variable list associated with an id
	variables_list = []
	manifeste_data = open(manifeste_file, "r")
	for line in manifeste_data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		if(str(proposition_id) == line_in_array[0]):
			variables_list = line_in_array[1].split(";")
	manifeste_data.close()

	## Get the name of the input file used for exploration
	input_data_file = ""
	settings_data = open(settings_file, "r")
	for line in settings_data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(":")
		if(line_in_array[0] == str("> input file")):
			input_data_file = line_in_array[1]
	settings_data.close()

	## get the list of variables
	## store data in dict
	index_to_variables = {}
	variable_to_values = {}
	variables = []
	data_file = open(input_data_file, "r")
	cmpt = 0
	for line in data_file:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")
		if(cmpt == 0):
			variables = line_in_array
			index = 0
			for var in line_in_array:
				index_to_variables[index] = var
				variable_to_values[var] = []
				index += 1
		else:
			index = 0
			for scalar in line_in_array:
				scalar = scalar.replace("\"", "")
				variable_to_values[index_to_variables[index]].append(scalar)
				index+=1

		cmpt += 1
	data_file.close()
	identifiant_label = ""
	try:
		variables.remove("\"identifiant\"")
		identifiant_label = "\"identifiant\""
	except:
		variables.remove("identifiant")
		identifiant_label = "identifiant"

	## Reconstruct the file
	file_name = "data/cb_reconstruction_"+str(proposition_id)+".csv"
			
	## Write the proposition file
	proposition_file = open(file_name, "w")
			
	## write the header
	header = ""
	header += "\"identifiant\""+","
	for prop_var in variables_list:
		header += str(prop_var)+","
	header = header[:-1]
	proposition_file.write(header+"\n")

	## write the lines
	for number_of_line in xrange(0, len(variable_to_values[str(identifiant_label)])):
		line_to_write = ""
		line_to_write += str(variable_to_values[str(identifiant_label)][number_of_line]) + ","
		for pos in index_to_variables.keys():
			var = index_to_variables[pos]
			if(var in variables_list):
				line_to_write += str(variable_to_values[var][number_of_line]) + ","
		
		line_to_write = line_to_write[:-1]
		proposition_file.write(line_to_write+"\n")
	proposition_file.close()

	print "[*] Generation completed"



def plot_variable_frequencies(path_to_save_folder):
	"""
	-> plot the count of variables retains in the good candidates
	   proposition

	TODO:
		Complete doc
	"""

	## Get the list of proposition id in suggestion space
	solution_id_list = []
	solution_files = glob.glob(str(path_to_save_folder)+"/good_candidates/*.png")
	for solution in solution_files:
		solution_id = solution.split("\\")
		solution_id = solution_id[-1]
		solution_id = solution_id.split(".")
		solution_id = solution_id[0]
		
		solution_id_list.append(solution_id)

	## Get the list of variables present in the solution space
	## and the associated count
	variables_to_count = {}
	manifeste_file_name = str(path_to_save_folder)+"/manifeste.log"
	manifeste_data = open(manifeste_file_name, "r")
	for line in manifeste_data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(",")

		for solution in solution_id_list:
			if(str(solution) == str(line_in_array[0])):

				variables_from_solution = line_in_array[1].split(";")

				for var in variables_from_solution:
					if(var not in variables_to_count.keys()):
						variables_to_count[var] = 0
					else:
						variables_to_count[var] += 1
	manifeste_data.close()

	## Plot the results
	plt.bar(range(len(variables_to_count)), variables_to_count.values(), align='center')
	plt.xticks(range(len(variables_to_count)), variables_to_count.keys(), rotation=20)
	plt.show()




def independant_progress_bar():
	"""
	-> Run a progress bar to check the
	   progression of the pca exploration

	TODO:
		- dix display problem
	"""

	## Get the list of variables
	variables_list = []
	settings_data = open("data/settings.log", "r")
	for line in settings_data:
		line = line.split("\n")
		line = line[0]
		line_in_array = line.split(":")

		if(str(line_in_array[0]) == "> Variables list"):
			variables_list = line_in_array[1].split(",")
	settings_data.close()

	## Compute the number of possible combinations
	total_number_of_combinations = 0
	tupleLen = 4
	while(tupleLen < len(variables_list)):
		for h in itertools.combinations(variables_list, tupleLen):
			total_number_of_combinations += 1
		tupleLen += 1

	#files_in_folder = glob.glob("data/pca_exploration_results/*2d_representation.png")
	files_in_folder = []
	progress = 0
	while(len(files_in_folder) < total_number_of_combinations):

		current_files_in_folder = glob.glob("data/pca_exploration_results/*2d_representation.png")

		if(len(current_files_in_folder) > len(files_in_folder)):

			## Display the progress bar
			step = float((100/float(total_number_of_combinations)))
			progress += len(current_files_in_folder) - len(files_in_folder)
			progress_perc = progress*step
			factor = math.ceil((progress_perc/2))
			progress_bar = "#" * int(factor)
			progress_bar += "-" * int(50 - factor)
			display_line = "[EXPLORATION]|"+progress_bar+"|"+str(progress)+"/"+str(total_number_of_combinations)+"|"
			sys.stdout.write("\r%d%%" % progress_perc)
			sys.stdout.write(display_line)
			sys.stdout.flush()

		files_in_folder = current_files_in_folder



def get_number_of_good_candidates(good_candidates_folder):
	"""
	Return the number of png files found
	in good_candidates_folder
	"""
	number_of_good_canditates = len(glob.glob(good_candidates_folder+"*.png"))
	return number_of_good_canditates




def get_cross_variables():
	"""
	IN PROGRESS
	""" 

	## Get all Flow Cytometry variables from PRECISADS
	precisesads_variables = []
	cmpt = 0
	precisesads_data = open("transmart_23_05_2017_PHASE_I&II.txt", "r")
	for line in precisesads_data:

		if(cmpt == 0):
			line = line.replace("\n", "")
			line_in_array = line.split("\t")
			for var in line_in_array:
				var_in_array = var.split("\\")
				if("Flow cytometry" in var_in_array and str(var_in_array[-1]) not in precisesads_variables):
					precisesads_variables.append(str(var_in_array[-1]))
		cmpt += 1
	precisesads_data.close()

	## Get all variables from CB
	cb_variables = []
	cmpt = 0
	cb_data = open("data/cb_data.csv", "r")
	for line in cb_data:
		if(cmpt == 0):
			line = line.replace("\n", "")
			line_in_array = line.split(",")
			for var in line_in_array:
				if(var != "identifiant" and var not in cb_variables):
					cb_variables.append(var)
		cmpt += 1
	cb_data.close()


	print "[+] "+str(len(precisesads_variables)) +" variables from PRECISESADS"
	print "[+] "+str(len(cb_variables)) +" variables from CB"

	## Identify commun variables
	for var in precisesads_variables:
		print var




def get_distance_between_cluster():
	"""
	IN PROGRESS
	"""
	# import the necessary packages
	from scipy.spatial import distance as dist
	from imutils import perspective
	from imutils import contours
	import numpy as np
	import argparse
	import imutils
	import cv2

	def midpoint(ptA, ptB):
		return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


	# load the image, convert it to grayscale, and blur it slightly
	image = cv2.imread("distance_between_objects_reference.jpg")
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (7, 7), 0)

	# perform edge detection, then perform a dilation + erosion to
	# close gaps in between object edges
	edged = cv2.Canny(gray, 50, 100)
	edged = cv2.dilate(edged, None, iterations=1)
	edged = cv2.erode(edged, None, iterations=1)

	# find contours in the edge map
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
 
	# sort the contours from left-to-right and, then initialize the
	# distance colors and reference object
	(cnts, _) = contours.sort_contours(cnts)
	colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255), (255, 255, 0), (255, 0, 255))
	refObj = None

	# loop over the contours individually
	for c in cnts:
		# if the contour is not sufficiently large, ignore it
		if cv2.contourArea(c) < 100:
			continue
 
		# compute the rotated bounding box of the contour
		box = cv2.minAreaRect(c)
		box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
		box = np.array(box, dtype="int")
 
		# order the points in the contour such that they appear
		# in top-left, top-right, bottom-right, and bottom-left
		# order, then draw the outline of the rotated bounding
		# box
		box = perspective.order_points(box)
 
		# compute the center of the bounding box
		cX = np.average(box[:, 0])
		cY = np.average(box[:, 1])

		# if this is the first contour we are examining (i.e.,
		# the left-most contour), we presume this is the
		# reference object
		if refObj is None:
			# unpack the ordered bounding box, then compute the
			# midpoint between the top-left and top-right points,
			# followed by the midpoint between the top-right and
			# bottom-right
			(tl, tr, br, bl) = box
			(tlblX, tlblY) = midpoint(tl, bl)
			(trbrX, trbrY) = midpoint(tr, br)
 
			# compute the Euclidean distance between the midpoints,
			# then construct the reference object
			D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
			refObj = (box, (cX, cY), D / 0.955)
			continue

		# draw the contours on the image
		orig = image.copy()
		cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
		cv2.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2)
 
		# stack the reference coordinates and the object coordinates
		# to include the object center
		refCoords = np.vstack([refObj[0], refObj[1]])
		objCoords = np.vstack([box, (cX, cY)])

		# loop over the original points
		for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
			# draw circles corresponding to the current points and
			# connect them with a line
			cv2.circle(orig, (int(xA), int(yA)), 5, color, -1)
			cv2.circle(orig, (int(xB), int(yB)), 5, color, -1)
			cv2.line(orig, (int(xA), int(yA)), (int(xB), int(yB)), color, 2)
 
			# compute the Euclidean distance between the coordinates,
			# and then convert the distance in pixels to distance in
			# units
			D = dist.euclidean((xA, yA), (xB, yB)) / refObj[2]
			(mX, mY) = midpoint((xA, yA), (xB, yB))
			cv2.putText(orig, "{:.1f}in".format(D), (int(mX), int(mY - 10)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
 
			# show the output image
			cv2.imshow("Image", orig)
			cv2.waitKey(0)


### TEST SPACE ###
#log_scaled("data/cb_data_proportion_complete.csv")
#add_random_diagnostic("data/cb_data_proportion_complete.csv", "data/cb_data_proportion_complete_individu_test.csv")
#centre_reduire_transformation("data/cb_data_complete.csv", "data/cb_data_complete_scaled.csv")

get_distance_between_cluster()

#generate_proposition_file()
#pca_exploration()
#graphical_analyze()
#log_analyse()
#write_manifeste()
#write_settings("data/cb_data_absolute_complete_scaled.csv", "normalize")

#cleaner()
#save_run()

#rebuild_file_from_id("save/RUN_3/settings.log", "save/RUN_3/manifeste.log", 1045)
#plot_variable_frequencies("save/RUN_3")
#independant_progress_bar()
#get_cross_variables()

#p = get_number_of_good_candidates("save/RUN_3/good_candidates/")
#print p
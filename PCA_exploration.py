import os
import shutil
import itertools
import glob
import log_management
import math
import sys


def cleaner():
	"""
	-> remove csv files in data/subsets folder
	-> remove the png files in data/pca_exploration_results folder
	-> remove the png files in data/good_candidates folder 
	-> use this function at the end of a pca exploration, 
	   after saving the results in a log file
	"""

	## display something
	print "[+] Cleaning folders"

	## list files to remove
	files_to_remove = glob.glob("data/subsets/*.csv")
	image_to_remove_1 = glob.glob("data/pca_exploration_results/*.png")
	image_to_remove_2 = glob.glob("data/good_candidates/*.png")

	## delete files
	progress = 0
	for f in files_to_remove:
		os.remove(f)

		## Display progress bar
		step = float((100/float(len(files_to_remove))))
		progress += 1
		progress_perc = progress*step
		factor = math.ceil((progress_perc/2))
		progress_bar = "#" * int(factor)
		progress_bar += "-" * int(50 - factor)
		display_line = "[SUBSETS]|"+progress_bar+"|"+str(progress)+"/"+str(len(files_to_remove))+"|"
		sys.stdout.write("\r%d%%" % progress_perc)
		sys.stdout.write(display_line)
		sys.stdout.flush()

	progress = 0
	for f in image_to_remove_1:
		os.remove(f)

		## Display progress bar
		step = float((100/float(len(image_to_remove_1))))
		progress += 1
		progress_perc = progress*step
		factor = math.ceil((progress_perc/2))
		progress_bar = "#" * int(factor)
		progress_bar += "-" * int(50 - factor)
		display_line = "[EXPLORATION]|"+progress_bar+"|"+str(progress)+"/"+str(len(image_to_remove_1))+"|"
		sys.stdout.write("\r%d%%" % progress_perc)
		sys.stdout.write(display_line)
		sys.stdout.flush()

	progress = 0
	for f in image_to_remove_2:
		os.remove(f)

		## Display progress bar
		step = float((100/float(len(image_to_remove_2))))
		progress += 1
		progress_perc = progress*step
		factor = math.ceil((progress_perc/2))
		progress_bar = "#" * int(factor)
		progress_bar += "-" * int(50 - factor)
		display_line = "[CANDIDATES]|"+progress_bar+"|"+str(progress)+"/"+str(len(image_to_remove_2))+"|"
		sys.stdout.write("\r%d%%" % progress_perc)
		sys.stdout.write(display_line)
		sys.stdout.flush()
	

	## display something
	print "\n[*] Cleaning Done"



def generate_proposition_file(input_data_file):
	"""
	-> Generate proposition file for pca & unsupervised exploration
	
	-> default file:
		data/cb_data_absolute_complete_scaled.csv

	TODO:
		- complete the documentation
	"""

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
	try:
		variables.remove("\"identifiant\"")
	except:
		variables.remove("identifiant")

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
			print "[+] Write file :"+str(file_name) 
			cmpt +=1
		tupleLen+=1




def pca_exploration():
	"""
	TODO:
		- write doc
	"""

	## get list of files
	proposition_files = glob.glob("data/subsets/*.csv")

	for proposition in proposition_files:

		print "[+] Compute file "+str(proposition)

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
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt

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
		print "[+] Processing case "+str(suggestion_id)

		## Perform the analysis
		analysis_results = image_analysis(image_file_name)

		## Write results in a log file
		log_file.write(str(suggestion_id)+","+str(analysis_results["number_of_clusters"])+","+str(analysis_results["sizes"])+"\n")

	log_file.close()


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
	new_id = 0
	list_of_id = []
	for folder in os.listdir("save"):
		folder_in_array = folder.split("_")
		run_number = int(folder_in_array[-1])
		list_of_id.append(run_number)
	if(len(list_of_id) > 0):
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
	variables.remove("\"identifiant\"")

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
	for number_of_line in xrange(0, len(variable_to_values["\"identifiant\""])):
		line_to_write = ""
		line_to_write += str(variable_to_values["\"identifiant\""][number_of_line]) + ","
		for pos in index_to_variables.keys():
			var = index_to_variables[pos]
			if(var in variables_list):
				line_to_write += str(variable_to_values[var][number_of_line]) + ","
		
		line_to_write = line_to_write[:-1]
		proposition_file.write(line_to_write+"\n")
	proposition_file.close()

	print "[*] Generation completed"


### MAIN ###
print "[*]--- PREPARE DATA ---[*]"
cleaner()
input_file_name = "data/cb_data_absolute_complete_special.csv"
scaling = "No scaling, absolute data"
log_management.write_settings(input_file_name, scaling)
print "[*]--- GENERATE PROPOSITION ---[*]"
generate_proposition_file(input_file_name)
print "[*]--- COMPUTE PROPOSITION ---[*]"
pca_exploration()
print "[*]--- EXTRACT INFORMATIONS ---[*]"
graphical_analyze()
print "[*]--- GENERATE LOG FILES ---[*]"
log_management.log_analyse()
log_management.write_manifeste()
print "[*]--- SAVE RESULTS ---[*]"
save_run()
print "[*]--- CLEANING FOLDERS ---[*]"
cleaner()

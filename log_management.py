"""
Gestion des logs
"""

import math
import random
import itertools
import glob
import shutil
import os
import sys


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
				if(str(var) != "\"identifiant\"" and str(var) != "identifiant"):
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
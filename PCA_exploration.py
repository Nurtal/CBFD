import os
import shutil
import itertools
import glob


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


### MAIN ###
print "[*]--- GENERATE PROPOSITION ---[*]"
generate_proposition_file()
print "[*]--- COMPUTE PROPOSITION ---[*]"
pca_exploration()
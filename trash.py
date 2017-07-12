"""
TRASH FUNCTIONS
"""

import math
import random
import itertools

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





### TEST SPACE ###
log_scaled("data/cb_data_proportion_complete.csv")
add_random_diagnostic("data/cb_data_proportion_complete.csv", "data/cb_data_proportion_complete_individu_test.csv")
centre_reduire_transformation("data/cb_data_complete.csv", "data/cb_data_complete_scaled.csv")

generate_proposition_file()

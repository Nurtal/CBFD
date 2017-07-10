"""
TRASH FUNCTIONS
"""

import math
import random

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



### TEST SPACE ###
log_scaled("data/cb_data_proportion_complete.csv")
add_random_diagnostic("data/cb_data_proportion_complete.csv", "data/cb_data_proportion_complete_individu_test.csv")


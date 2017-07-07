"""
TRASH FUNCTIONS
"""

import math

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


### TEST SPACE ###
log_scaled("data/cb_data_proportion_complete.csv")

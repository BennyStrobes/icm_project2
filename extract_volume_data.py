import numpy as np
import os
import sys
import pdb

######################
# Helper funcionts
######################

# Extract names of samples from sample_id_file
def extract_sample_names(sample_id_file):
    sample_names = []
    case_controls = []
    f = open(sample_id_file)
    for line in f:
        data = line.rstrip().split()
        sample_names.append(data[0])
        case_controls.append(data[1])
    return sample_names, case_controls

####################
# Command line args
#####################
# Name of file containing all structure we are extracting
structure_name_file = sys.argv[1]
# Suffix of volume files
volume_data_suffix = sys.argv[2]
# Type of statistics in specific volume file
statistic_type = sys.argv[3]
# Where to save output to
output_file = sys.argv[4]
# Names of samples
sample_id_file = sys.argv[5]

# Extract names of samples from sample_id_file
sample_names, case_control_status = extract_sample_names(sample_id_file)

# Create dictionary contianing names of all structures we wish to extract
structures = {}
f = open(structure_name_file)
for line in f:
    line = line.rstrip()
    structures[line] = 1

# Loop through each sample and extract volume measurement
volumes = np.zeros(len(sample_names))
for i,sample_name in enumerate(sample_names):
    # Name of input file for this sample
    input_file = 'volume_data/' + sample_name + volume_data_suffix
    # Variable to keep track of whether we are at the correct statistic
    correct_statistic = False
    f = open(input_file)
    for line in f:
        line = line.rstrip()
        data = line.split()
        # Change statistic type to something that is not our statistic type
        if line.startswith('Type') == True and line.startswith(statistic_type) == False:
            correct_statistic = False
            continue
        # Change statistic type to our statistic type
        if line.startswith(statistic_type):
            correct_statistic = True
            continue
        # Ignore lines that do not belong to our statistic type
        if correct_statistic == False:
            continue
        # Skip blank lines
        if line == '':
            continue
        line_structure = data[1]
        line_volume = float(data[2])
        # This is what we wanted
        if line_structure in structures:
            volumes[i] = volumes[i] + line_volume

if len(volumes) != len(sample_names):
    print('FATAL ERROR: Something went wrong')

# Open output handle
t = open(output_file, 'w')
for index, sample_name in enumerate(sample_names):
    t.write(sample_name + '\t' + case_control_status[index] + '\t' + str(volumes[index]) + '\n')
t.close()

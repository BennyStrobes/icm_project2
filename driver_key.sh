# File containing names of sample ids (first column) and case/control status (second column)
sample_ids="sample_ids.txt"
# Where to save output files
output_directory="output/"


########################
# PARAMETERS
########################
# Suffix of files in volume_data
#  Options are "_283Labels_M2_MNI_stats.txt" and "_283Labels_M2_corrected_stats.txt"
#  Not really sure which one to use
volume_data_suffix="_283Labels_M2_MNI_stats.txt"

# Types of statistics (several different versions)
# Not really sure which one to use
statistic_type="Type2-L5"



###########################################
# Performa analysis for various structures
###########################################


# Name of structure as they appear in *.stats files
structure_name="SF_PFC_L"
# Name of output file to save parsed/extract volume measurements to
output_stem=$output_directory$structure_name
volume_output_file=$output_stem"_parsed_volume.txt"
# Extract volume measure measurements
python extract_volume_data.py $structure_name $volume_data_suffix $statistic_type $volume_output_file $sample_ids
# Perform data visualization and statistical analysis on parsed volume data
python volume_visualization_and_statistical_analysis.py $output_stem $volume_output_file $structure_name
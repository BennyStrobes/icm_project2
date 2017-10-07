import numpy as np
import os
import sys
import pdb
import matplotlib.pyplot as plt
import seaborn as sns 
sns.set_style("white")
import pandas as pd
import scipy.stats


# Plot histogram of volumes colored by cases and controls
def group_specific_histogram_plot(output_file, volume_file, structure_name):
    # Extract volumes
    volumes_ad = []
    volumes_norm = []
    f = open(volume_file)
    for line in f:
        data = line.rstrip().split()
        if data[1] == 'AD':  # AD gropu
            volumes_ad.append(float(data[2]))
        elif data[1] == 'Normal':
            volumes_norm.append(float(data[2]))
    f.close()
    ## Create bins
    max_vol = max(max(volumes_ad),max(volumes_norm))
    min_vol = min(min(volumes_ad), min(volumes_ad))
    num_bins = 6
    bins = np.arange(min_vol,max_vol,(max_vol-min_vol)/num_bins)
    # Initialize plot
    plt.clf()
    fig = plt.figure()
    ax = plt.subplot(111)
    # plots
    ax.hist(volumes_ad, label='AD',bins=bins,alpha=.55,color='cyan')
    ax.hist(volumes_norm, label='Normal',bins=bins,alpha=.55,color='salmon')
    # Axis labels
    plt.xlabel('Volume (mm3)',fontsize=18)
    plt.ylabel('Number of Samples',fontsize=18)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.tick_params(axis='both', which='minor', labelsize=12)
    # put legend outside plot
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize=18)
    plt.title(structure_name,fontsize=22)
    plt.savefig(output_file)


def volume_violin_plot(output_file, volume_file, structure_name):
    plt.clf()
    # Load data into pandas data frame
    data = np.loadtxt(volume_file, dtype=str)
    df = pd.DataFrame(data,columns=['sample_id','disease_status','volume'])
    df['volume'] = df['volume'].astype(float)
    # Plot
    ax = sns.violinplot(x='disease_status',y='volume',data=df, inner=None,palette=['cyan','salmon'],alpha=.1)
    sns.swarmplot(x='disease_status',y='volume',data=df,color='w',alpha=.5)
    # Increase tick text size
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.tick_params(axis='both', which='minor', labelsize=12)
    # Axis labels
    plt.xlabel('Disease Status', fontsize=18)
    plt.ylabel('Volume (mm3)', fontsize=18)
    plt.title(structure_name,fontsize=22)
    plt.savefig(output_file)

# Report required statistics:
###1. mean and sdev of volumes in each group
###2. signal difference to noise ratio
###3. t-test
def report_statistics(output_file, volume_file):
   # Extract volumes
    volumes_ad = []
    volumes_norm = []
    f = open(volume_file)
    for line in f:
        data = line.rstrip().split()
        if data[1] == 'AD':  # AD gropu
            volumes_ad.append(float(data[2]))
        elif data[1] == 'Normal':
            volumes_norm.append(float(data[2]))
    f.close()
    # open output file handle
    t = open(output_file, 'w')

    ##1.  Mean and SDEV
    ad_mean = np.mean(volumes_ad)
    ad_std = np.std(volumes_ad)
    norm_mean = np.mean(volumes_norm)
    norm_std = np.std(volumes_norm)
    t.write('AD mean: ' + str(ad_mean) + '\n')
    t.write('AD sdev: ' + str(ad_std) + '\n')
    t.write('Norm mean ' + str(norm_mean) + '\n')
    t.write('Norm sdev: ' + str(norm_std) + '\n')

    ##2. Signal difference to noise ratio
    average_variace = (ad_std**2 + norm_std**2)/2.0
    signal_diff_to_noise_ratio = abs(ad_mean - norm_mean)/np.sqrt(average_variace)
    t.write('signal difference to noise ratio: ' + str(signal_diff_to_noise_ratio) + '\n')

    ##3. t-test to check if distributions are significantly different
    t_statistic,pval = scipy.stats.ttest_ind(volumes_ad,volumes_norm)
    t.write('t-test t-statistic: ' + str(t_statistic) + '\n')
    t.write('t-test p-value: ' + str(pval) + '\n')
    t.close()


#########################
# Command Line Arguments
#########################
# Prefix to save output files to
output_stem = sys.argv[1]
# File with volume measurements
volume_file = sys.argv[2]
# Structure names
structure_name = sys.argv[3]

# Plot histogram of volumes colored by cases and controls
group_specific_histogram_plot(output_stem + "_volume_histogram_colored_by_disease_status.png", volume_file, structure_name)

# Plot violin plot showing distribution of volumes. One violin for cases and controls
volume_violin_plot(output_stem + '_volume_violin_plot.png', volume_file, structure_name)


# Report required statistics:
###1. mean and sdev of volumes in each group
###2. signal difference to noise ratio
###3. t-test
report_statistics(output_stem + '_statistics.txt', volume_file)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import time

chars = ['|', '/', '-', '\\']
# Read the distribution data into a DataFrame
distribution_df = pd.read_csv('distribution.csv')

#make sure the cancer type name are similar in both files
cancerlist= distribution_df['Broad Category Cancer Type'].unique()

# Read the input data into a DataFrame
input_df = pd.read_csv('input.csv')

i=0
# Iterate over each row in the input DataFrame
for _, row in input_df.iterrows():
    x=round((i+1)/len(input_df)*100)
	
    # Set up the figure and axes
    if row['Broad Category Cancer Type'] in cancerlist:
      fig, ax = plt.subplots(figsize=(8, 6))

    # Create a density plot for the entire cohort
      sns.kdeplot(data=distribution_df['TMB Score'], fill=True, label='Indian Pan Cancer Cohort', ax=ax, cut=0, color='grey')

    # Filter the distribution DataFrame for the current row's cancer type
      cancer_df = distribution_df[distribution_df['Broad Category Cancer Type'] == row['Broad Category Cancer Type']]
      percentage_above = round(cancer_df[cancer_df['TMB Score'] > 10].shape[0] / cancer_df.shape[0] * 100,2)

    # Create a density plot for the current cancer type
      sns.kdeplot(data=cancer_df['TMB Score'], fill=True, label=f"{row['Broad Category Cancer Type']} Cancer", ax=ax, cut=0, color='#148bcd', alpha=0.2)
      sns.rugplot(data=distribution_df, x="TMB Score", color='grey',height=.05)
      sns.rugplot(data=cancer_df, x="TMB Score", color='#148bcd', height=.05)
      plt.xlim([1,90])


    # Highlight the TMB score from the input.csv
      ax.axvline(x=row['TMB Score'], color='red', linestyle='--', label=f"{row['Sample Name']} TMB Score={row['TMB Score']}\n{percentage_above}% patients have TMB Score > 10")

      # ax.axvline(distribution_df['TMB Score'].median(), color='grey', label=f"Median (Indian Cohort)")
      # ax.axvline(cancer_df['TMB Score'].median(), color='grey')
      # plt.figtext(0.1, 0.055, f"Indian Cohort Median={distribution_df['TMB Score'].median()}, {row['Broad Category Cancer Type']} Cancer Median={round(cancer_df['TMB Score'].median(),2)}\n**The clinical outcomes of patients with cancer can vary significantly across different\ngeographies, highlighting the complexity of utilizing TMB as a predictive immunotherapy\nbiomarker.\n**It is important to recognize that assuming a universal criterion and cutoff for all\nethnicities and geographical areas may have adverse effects on cancer patients.\nTherefore, caution should be exercised when interpreting TMB data, considering the\ndiverse factors that influence its efficacy as a biomarker in clinical settings.", fontsize=10, ha='left')
      # plt.subplots_adjust(bottom=0.35)

   # Add labels 
      ax.set_xlabel('TMB Score (mut/Mb)')
      ax.set_ylabel('Density')
      ax.legend(labelcolor=['black', 'black', '#148bcd'])

    # Save the plot in the output_plots folder with the sample name as the file name
      output_folder = 'output_plots'
      os.makedirs(output_folder, exist_ok=True)
      output_file = os.path.join(output_folder, f"{row['Sample Name']}_density_plot.png")
      plt.savefig(output_file)

    # Close the figure to free up memory
      plt.close(fig)
      i=i+1
      for char in chars:
        sys.stdout.write(f'Processing >> {x}% {char}\r')
        sys.stdout.flush()
        time.sleep(0.01)



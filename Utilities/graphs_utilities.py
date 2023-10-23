import pandas as pd
import numpy as np

import seaborn as sns
from pylab import savefig
from matplotlib import pyplot as plt

from ydata_profiling import ProfileReport
import statsmodels.api as sm


"""
This function generates a report containing information about data profiling of the dataframe
For each variable a univariate analysis is completed and the results are saved as HTML files in the profiling directory
"""
def exportDataProfileReportToHTML(df, profilingDir, data_source_name, minim=True):
    profile = ProfileReport(df, title = f"{data_source_name}_Profiling_Report", minimal=minim)
    profile.to_file(f"{profilingDir}{data_source_name}_Report.html")

# This function generates the spearman correlation heatmap for the input dataframe
def generateCorrelationHeatMap(df, data_source_name, plotDir):
    numeric_columns = df.select_dtypes(include=['number']).columns
    cor = df[numeric_columns].corr(method="spearman")
    heatmap = sns.heatmap(cor, vmin=-1, vmax=1, annot=False, cmap='coolwarm', linecolor='black', linewidths=1)
    heatmap.set_title(f'{data_source_name} Correlation Heatmap', fontdict={'fontsize':12}, pad=12)
    plt.savefig(f"{plotDir}{data_source_name}_corr_heatmap.png", dpi=400)
    plt.clf()

# This function generates a pairplot between all the variables of the input dataframe
def generatePairplot(df, data_source_name, plotDir):
    pairplot = sns.pairplot(df, corner=True)
    fig = pairplot.fig
    fig.suptitle(f"{data_source_name} Pairplot", y=1.02)
    pairplot.savefig(f"{plotDir}{data_source_name}_pairplot.png", dpi=400)
    plt.clf()

# This function generates a lineplot between all the variables of the input dataframe
def generateLinePlot(df, data_source_name, plotDir):
    lineplot = sns.lineplot(data=df)
    #lineplot.fig.suptitle(f"{data_source_name} Lineplot")
    plt.savefig(f"{plotDir}{data_source_name}_lineplot.png", dpi=400)
    plt.clf()

# This function generates a boxplots for all the variables of the input dataframe
def generateBoxplot(df, data_source_name, plotDir):
    for col in df.columns:
        boxplots = sns.boxplot(data=df[col])
        plt.savefig(f"{plotDir}{data_source_name}{col}_boxplots.png", dpi=400)
        plt.clf()

# Function to convert a pandas correlation matrix to tidy format
def tidy_corr_matrix(corr_mat):
    corr_mat = corr_mat.stack().reset_index()
    corr_mat.columns = ['variable_1','variable_2','r']
    corr_mat = corr_mat.loc[corr_mat['variable_1'] != corr_mat['variable_2'], :]
    corr_mat['abs_r'] = np.abs(corr_mat['r'])
    corr_mat = corr_mat.sort_values('abs_r', ascending=False)

# Function to generate the correlation heatmap for the pandas correlation matrix
def generateCorrHeatMap(corr_matrix):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4))

    sns.heatmap(
        corr_matrix,
        annot     = True,
        cbar      = False,
        annot_kws = {"size": 8},
        vmin      = -1,
        vmax      = 1,
        center    = 0,
        cmap      = sns.diverging_palette(20, 220, n=200),
        square    = True,
        ax        = ax
    )

    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation = 45,
        horizontalalignment = 'right',
    )

    ax.tick_params(labelsize = 10)
import numpy as np

from Utilities.graphs_utilities import generateBoxplot
from Utilities.os_utilities import getDataSourcesNames, createDirectory
from Utilities.db_utilities import getDataframeFrom_trusted, saveDataframeTo_trusted_outliers
from paths import outliersDir, outliersPlotsDir, trustedZoneTables

# In this code we are generating a outlier detection and handling in the tables we have in the trusted zone
# Those tables are a final version so the data visualization would be updated

def outlierDetection(df, table, plotDir):
    numericDf = df.select_dtypes(include=[np.number])
    generateBoxplot(numericDf, table, plotDir)

    # Calculate Q1 and Q3
    Q1 = numericDf.quantile(0.25)
    Q3 = numericDf.quantile(0.75)

     # Calculate the IQR
    IQR = Q3 - Q1

    # Filter the dataset with the IQR
    IQRoutliers = df[((numericDf < (Q1 - 1.5 * IQR)) | (numericDf > (Q3 + 1.5 * IQR))).any(axis=1)]
    print(IQRoutliers.head)
    return IQRoutliers


def main():
    createDirectory(outliersDir)
    createDirectory(outliersPlotsDir)

    tables = getDataSourcesNames(trustedZoneTables)

    for table in tables:
        plotDir = outliersPlotsDir + table + '/'
        createDirectory(plotDir)

        print(f"\nDetecting outliers for {table} data source")
        df = getDataframeFrom_trusted(table)
        outliersDf = outlierDetection(df, table, plotDir)
        saveDataframeTo_trusted_outliers(outliersDf, table)

if __name__ == "__main__":
    main()
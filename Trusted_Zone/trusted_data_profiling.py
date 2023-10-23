from Utilities.graphs_utilities import *
from Utilities.os_utilities import *
from Utilities.db_utilities import *

import os

from paths import profilingDir, profilingPlotsDir, trustedZoneTables

# In this code we are generating a data profile for each of the tables we may have in the trusted zone
# Those tables are a final version so the data visualization would be updated

def dataProfiling(df, table, plotDir):
    exportDataProfileReportToHTML(df, profilingDir, table)

    # Multivariate analysis
    generateCorrelationHeatMap(df, table, plotDir)
    generatePairplot(df, table, plotDir)
    generateLinePlot(df, table, plotDir)


def main():
    createDirectory(profilingDir)
    createDirectory(profilingPlotsDir)

    tables = getDataSourcesNames(trustedZoneTables)

    for table in tables:
        plotDir = profilingPlotsDir + table + '/'
        createDirectory(plotDir)

        print(f"\nProfile generation for {table} data source")
        df = getDataframeFrom_trusted(table)
        dataProfiling(df, table, plotDir)

if __name__ == "__main__":
    main()
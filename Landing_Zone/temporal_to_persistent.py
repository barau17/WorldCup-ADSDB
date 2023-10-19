from Utilities.os_utilities import createDirectory, getTimestamp, copyFilesOfSourceToDestDirWithTimestamp
from paths import temporalPath, persistentPath


# Moving all the data sources from the temporal folder to the persistent folder, with the ingestion date
# The entrace of data is done manually, putting the ingested data into the Landing/Temporal folder

def main():
    createDirectory(persistentPath)
    ts = getTimestamp()
    copyFilesOfSourceToDestDirWithTimestamp(temporalPath, persistentPath, ts)

if __name__ == "__main__":
    main()
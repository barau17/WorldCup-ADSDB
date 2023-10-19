import os
import shutil
from datetime import datetime

# Creating the directory provided as input
def createDirectory(directoryPath):
  if not os.path.exists(directoryPath):
    os.mkdir(directoryPath)

# Handles base and extension separation for files of different type, like xlsx, tar.gz, etc.
def getBaseAndExtensionOfFile(file):
    # A list of types of files
    types_of_files = [".xlsx", ".csv", ".tar.gz"]
    # A list of folder separation characters
    folder_separation_characters = ["//", "\\", "/"]

    # Checking which is the type of separation character used in the absolute path of the file
    for folder_separation_character in folder_separation_characters:
      if folder_separation_character in file:
        separtion_character = folder_separation_character

    # Take only the filename from the absolute path of file
    filename = file.split(separtion_character)[-1]

    # Check the type of file from the list of types and separate base and extension
    for file_type in types_of_files:
      if filename.endswith(file_type):
        base = filename.split(file_type)[0]
        extension = file_type
        break

    # Return the base and extension of the filename
    return base, extension

#  Getting a list with all the names of the data sources saved in the landing zone inside the temporal folder
def getDataSourcesNames(temporalPath):
  data_sources_names = os.listdir(temporalPath)
  return data_sources_names

# Generating and returning a timestamp
def getTimestamp():
  dt = datetime.now()
  ts = datetime.timestamp(dt)
  return ts

"""
Copying all directories and files inside the source folder to the destination folder
Additionally, timestamps are added to the names of all directories and files to the destination folder
"""
def copyFilesOfSourceToDestDirWithTimestamp(sourceDir, destDir, timestamp):
  types_of_files = [".xlsx", ".csv", ".tar.gz"]
  files = [f for f in os.listdir(sourceDir) if any(f.endswith(ext) for ext in types_of_files)]
  for f in files:
    print("Landing: ", f)
    file_path = os.path.join(sourceDir, f)
    base, extension = getBaseAndExtensionOfFile(file_path)
    time = str(timestamp).split('.')[0]
    f = f"{base}_{time}{extension}"
    new_path = os.path.join(destDir, f)
    os.rename(file_path, new_path)
    print("Added as: ", f)


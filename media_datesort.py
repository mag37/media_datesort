import os
import shutil
import filecmp
import exifread
import logging

# User parameters:
input_path = "./Testing/Input"
output_path = "./Testing/Output"
file_types = (".jpeg", ".jpg", ".png", ".mp4", ".dng")
no_date_dir = "NoDate" # name of the directory to store no-dated images
date_separator = "-" # character to separate dates, eg. 2023-01-01 or 2023.01.01 DONT use slashes

# Logging format, handlers to write to file and console
logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s", 
        datefmt="%y/%m/%d %H:%M:%S", 
        level=logging.INFO,
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler() # writing to stderr
            ]
        )

# Check user-defined paths:
if not os.path.exists(input_path):
    print("Input directory does not exist, quitting")
    exit()
if not os.path.exists(output_path):
    print(f"Output directory does not exist - creating it @ {output_path}")
    os.mkdir(output_path)

def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
        logging.info(f"File copied. Source: {src} Destination: {dst}")
    except Exception as e:
        logging.error(f"Skipping file: {e}")

# function to make unique names
def unique_filename(dst):
    suffix = 0
    base, ext = os.path.splitext(dst)
    while os.path.exists(dst):
        dst = base + f"_{suffix}" + ext
        suffix += 1
    return dst

def date_and_copy(file_path):
    with open(file_path, "rb") as f:
        filename = os.path.basename(file_path)
        try:
            # grab exif data:
            exif_data = exifread.process_file(f, details=False, stop_tag="DateTimeOriginal")
            # strip and reformat date from "2023:08:01 10:18:45" to "2023-08-01"
            date_stamp = str(exif_data["EXIF DateTimeOriginal"])[:10].replace(":", date_separator) 
            date_list = date_stamp.split(date_separator)
            # Create full path of subdirectories ex: 2023/08/2023-08-01/image.jpg
            # Change date_stamp to date_list[2] to have the layout: 2023/08/01/image.jpg
            output_dir = os.path.join(output_path, date_list[0], date_list[1], date_stamp)
        except:
            # if no date-exif, copy file to "no-date dir"
            output_dir = os.path.join(output_path, no_date_dir)
            logging.warning(f"No exif-data on file {filename}. Copying to {no_date_dir}")
        src = file_path
        dst = os.path.join(output_dir, filename)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  # makedirs to be able to create the full path of subdirectories
        if os.path.exists(dst): # check src+dst same name
            if filecmp.cmp(src, dst): # check src+dst same content
                logging.info(f"Skipping file: {dst} already exists")
            else: 
                dst = unique_filename(dst)
                logging.info(f"Different content but same name, adding suffix {dst}")
                copy_file(src, dst)
        else:
            copy_file(src, dst)

# Iterate over all files and subdirectories
for root, dirs, files in os.walk(input_path):
    for file in files:
        # check extension - "lower" to be case-insensitive
        if file.lower().endswith(file_types):
            date_and_copy(os.path.join(root, file))

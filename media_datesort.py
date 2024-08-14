import os
import shutil
import filecmp
import exifread
import logging
import sys
import re
from datetime import datetime

# User parameters:
input_path = "./Testing/Input"
output_path = "./Testing/Output"
file_types = (".jpeg", ".jpg", ".png", ".dng")
no_date_dir = "NoDate" # name of the directory to store no-dated images
unsortable_dir = "Unsortables"
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

def process_file(output_dir, file_path):
    filename = os.path.basename(file_path)
    dst = os.path.join(output_dir, filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # makedirs to be able to create the full path of subdirectories
    if os.path.exists(dst): # check src+dst same name
        if filecmp.cmp(file_path, dst): # check src+dst same content
            logging.info(f"Skipping file: {dst} already exists")
        else: 
            dst = unique_filename(dst)
            logging.info(f"Different content but same name, adding suffix {dst}")
            copy_file(file_path, dst)
    else:
        copy_file(file_path, dst)

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

        # Create new copy+unique function
        process_file(output_dir, file_path)

def likely_date_format(file_path):
    filename = os.path.basename(file_path)
    # Order by most likely as first match will be used
    date_formats = ['%y%m%d', '%Y%m%d', '%y-%m-%d', '%Y-%m-%d', '%y.%m.%d', '%Y.%m.%d', '%d%m%y', '%d%m%Y', '%d-%m-%y', '%d-%m-%Y', '%d.%m.%y', '%d.%m.%Y']
    date_regex = [r'\d{6,8}', r'\d{2,4}-\d{2}-\d{2}', r'\d{2,4}\.\d{2}\.\d{2}']
    regex = r'|'.join(date_regex)
    date_pattern = re.search(regex, filename)
    # setting placeholder dir if no match
    output_dir = os.path.join(output_path, unsortable_dir)
    if date_pattern: # to check if pattern is found, else return None
        match = date_pattern.group(0)
        for format in date_formats:
            try:
                # Check if match is valid date, strftime() is required due to strptime() dont check zero padded month/day
                if match != datetime.strptime(match, format).strftime(format):
                    raise ValueError
                print(f"Match: {match}, Format: {format}")
                date_stamp = datetime.strptime(match, format).strftime(f"%Y{date_separator}%m{date_separator}%d")
                date_list = date_stamp.split(date_separator)
                output_dir = os.path.join(output_path, date_list[0], date_list[1], date_stamp)
                break # break to not interate on all possible matches
            except ValueError:
                pass # Skip if not valid date and try next
    process_file(output_dir, file_path)


if len(sys.argv) > 1:
    if sys.argv[1] == "dateguess":
        # Iterate over all files and subdirectories in no-date-dir for 2nd guessing
        for root, dirs, files in os.walk(os.path.join(output_path, no_date_dir)):
            for file in files:
                # check extension - "lower" to be case-insensitive
                if file.lower().endswith(file_types):
                    likely_date_format(os.path.join(root, file))
    else:
        print("Help: Use argument 'dateguess' to try to grab dates from filenames")
  
else:
    # Iterate over all files and subdirectories
    for root, dirs, files in os.walk(input_path):
        for file in files:
            # check extension - "lower" to be case-insensitive
            if file.lower().endswith(file_types):
                date_and_copy(os.path.join(root, file))

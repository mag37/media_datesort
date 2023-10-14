## A script sorting images based on Exif-date into dated subdirectories, like `Pictures/2023/09/2023-09-01/image.jpg`.

## Features:
- Crawls all subdirectories of the input-source, grabs exif-data from each file and copies it to a path based on the extracted date.   
- If two files got the same name - compares the file contents and skips if its the same, adds a suffix if its not.   
- If the date cant be decided - copies the file to a defined "no_date_dir" to be sorted manually.  
- Logs everything to a `debug.log`.

## Dependencies:
- Python3
- Exifread (python module, install with eg. pip)
- Only tested on Linux

## Settings:
Edit the `media_datesort.py` and adjust:
```
input_path = "./Testing/Input"
output_path = "./Testing/Output"
file_types = (".jpeg", ".jpg", ".png", ".mp4", ".dng")
no_date_dir = "NoDate" # name of the directory to store no-dated images
date_separator = "-" # character to separate dates, eg. 2023-01-01 or 2023.01.01 DONT use slashes
```
To change the final subdirectory layout from `/2023/09/2023-09-01/image.jpg` to `/2023/09/01/image.jpg` edit this line:
```python
# from /YYYY/MM/YYYY-MM-DD/image.jpg:
output_dir = os.path.join(output_path, date_list[0], date_list[1], date_stamp)
# to /YYYY/MM/DD/image.jpg:
output_dir = os.path.join(output_path, date_list[0], date_list[1], date_list[2])

```

### Extras:
Started working on some kind of filename-date-extraction but before I started validating the dates, I realised without a defined pattern and some rules, many dates will be valid but wrong.   
For another day..

## A script sorting images based on Exif-date into dated subdirectories, like `Pictures/2023/09/2023-09-01/image.jpg`.

## Features:
- Crawls all subdirectories of the input-source, grabs exif-data from each file and copies it to a path based on the extracted date.   
- If two files got the same name - compares the file contents and skips if its the same, adds a suffix if its not.   
- If the date cant be decided - copies the file to a defined *"no_date_dir"* to be sorted manually.  
- Optional `guess` argument, to run regex+dateformat on the *"no_date_dir"*
- Logs everything to a `debug.log`.

## Dependencies:
- Python3
- Exifread (python module, install with eg. pip)

## Settings:
Edit the `settings.py` and adjust:
```
input_path = "./Testing/Input"
output_path = "./Testing/Output"
file_types = (".jpeg", ".jpg", ".png", ".dng")
no_date_dir = "NoDate" # name of the directory to store images with no exif-date
unsortable_dir = "Unsortables" # name of the directory to store images that cant be guessed
date_separator = "-" # character to separate dates, eg. 2023-01-01 or 2023.01.01 DONT use slashes
```

To change the final subdirectory layout from `/2023/09/2023-09-01/image.jpg` to `/2023/09/01/image.jpg` edit this line:
```python
# from /YYYY/MM/YYYY-MM-DD/image.jpg:
output_dir = os.path.join(output_path, date_list[0], date_list[1], date_stamp)
# to /YYYY/MM/DD/image.jpg:
output_dir = os.path.join(output_path, date_list[0], date_list[1], date_list[2])
```

### Preferrably run it in a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate # See below for windows
pip install -r requirements.txt
```
Windows:
```powershell
env/Scripts/Activate.ps1 //Powershell
env/Scripts/activate.bat //CMD
```

Run it with `python3 media_datesort.py`
And the optional 2nd run with guess argument `python3 media_datesort.py guess`


# TODO:
- Fix paths to work for Windows
- Fix so that `guess` will give info if *"no_date_dir"* is empty.
- Add more filetypes
- Make interactive date-format selection?

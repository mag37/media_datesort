import re
from datetime import datetime

# Add this to main script with sys.argv?
# import sys
# if len(sys.argv) > 1:
#   if sys.argv[1] == "dateguess":
#       print("running guesswork")
# else:
#     print("running default")

date_separator = "-" # character to separate dates, eg. 2023-01-01 or 2023.01.01 DONT use slashes

def likely_date_format(filename):
    # Order by most likely as first match will be used
    date_formats = ['%y%m%d', '%Y%m%d', '%y-%m-%d', '%Y-%m-%d', '%y.%m.%d', '%Y.%m.%d', '%d%m%y', '%d%m%Y', '%d-%m-%y', '%d-%m-%Y', '%d.%m.%y', '%d.%m.%Y']
    date_regex = [r'\d{6,8}', r'\d{2,4}-\d{2}-\d{2}', r'\d{2,4}\.\d{2}\.\d{2}']
    #date_pattern = re.search(r'\d{6,8}', filename)
    regex = r'|'.join(date_regex)
    date_pattern = re.search(regex, filename)
    if date_pattern: # to check if pattern is found, else return None
        match = date_pattern.group(0)
        for format in date_formats:
            try:
                # Check if match is valid date, strftime() is required due to strptime() dont check zero padded month/day
                if match != datetime.strptime(match, format).strftime(format):
                    raise ValueError
                return match, format
            except ValueError:
              pass
    return None

files = [ "invalid1_1234.jpg", "invalid2-999999.jpg", "odd1_110723.jpg", "odd2_11072023.jpg" "file1_230711.jpg", "file2_20230821.jpg", "20231023_111211_946_img.jpg", "20230804_203421_960_img.jpg", "24-07-01_test1.jpg", "2024.07.02_test2.jpg"]
for file in files:
    print(file)
    result = likely_date_format(file)
    print(f"Date match: {result}")
    if result is not None:
        date_stamp = datetime.strptime(result[0], result[1]).strftime(f"%Y{date_separator}%m{date_separator}%d")
        print(f"Converted date: {date_stamp}")
        date_list = date_stamp.split(date_separator)
        print(f"Year: {date_list[0]} Month: {date_list[1]} Day: {date_list[2]}")
    print(" ")


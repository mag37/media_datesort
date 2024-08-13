import re
from datetime import datetime

# Add this to main script with sys.argv?
# import sys
# if sys.argv[1] == "nodate":
#     runThisBit
# else:
#     runMainBit

def likely_date_format(filename):
    date_formats = ['%y%m%d', '%Y%m%d', '%d%m%y', '%d%m%Y', '%y-%m-%d', '%Y-%m-%d', '%d-%m-%y', '%d-%m-%Y', '%y.%m.%d', '%Y.%m.%d', '%d.%m.%y', '%d.%m.%Y']
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

files = [ "invalid1_1234.jpg", "invalid2-999999.jpg", "file1_230711.jpg", "file2_20230821.jpg", "20231023_111211_946_img.jpg", "20230804_203421_960_img.jpg", "24-07-01_test1.jpg", "2024.07.02_test2.jpg"]
for file in files:
    print(file)
    print(likely_date_format(file))



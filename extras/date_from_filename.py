import re
from datetime import datetime

## Version 1
# def extract_date(filename):
#     date_pattern = re.compile(r'\d{2,4}[-_.]\d{2}[-_.]\d{2,4}')
#     match = date_pattern.search(filename)
#     if match:
#         return match.group()
#     else:
#         return None

# filename = 'my_report_2022-03-21.pdf'
# date = extract_date(filename)

# if date:
#     print(f'Date found in filename: {date}')
# else:
#     print('No valid date found in filename.')


## Version 2


def likely_date_format(filename):
    date_formats = ['%y%m%d', '%Y%m%d', '%d%m%y', '%d%m%Y']
    date_pattern = re.search(r'\d{6,8}', filename)
    match = date_pattern.group(0)
    if date_pattern:
        for format in date_formats:
            try: 
                datetime.strptime(match, format)
                return match, format
            except ValueError:
                pass
    return None

files = ["file1_230711.jpg", "file2_20230821.jpg", "file3-070923.jpg", "file4-990999.jpg", "20231023_111211_946_img.jpg", "20230804_203421_960_img.jpg"]
for file in files:
    print(file)
    print(likely_date_format(file))




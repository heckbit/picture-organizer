import os
from PIL import Image
from datetime import datetime

def coalesce(*params):
    return next((param for param in params if param is not None), None)

base_path = "C:\\Users\\jghd1\\OneDrive\\Pictures\\Camera Roll"

# Access picture files in Camera Roll
files = os.listdir(base_path)

pictures = list()
pics_with_date = list()

for file in files:
    file_split = file.split('.')
    if len(file_split) > 1:
        if 'jpg' in file_split[1]:
            pictures.append(file)

# Check picture date
for pic in pictures:
    full_path = base_path + "\\" + pic

    # get date from image metadata
    im = Image.open(full_path)
    exif = im.getexif()
    metadata_date = exif.get(306)
    
    # get date from file stats
    file_stats = os.stat(full_path)
    file_date = datetime.fromtimestamp(file_stats.st_birthtime)

    creation_date = coalesce(metadata_date,file_date)

    pics_with_date.append({'name':pic, 'date':creation_date})

# Move pictures to a folder base on year
## Create new folder for year if it does not exist yet

for pic in pics_with_date:
    if type(pic['date']) is str:
        year = pic['date'].strip()[0:4]
    else:
        year = f'{pic['date'].year}'

    year_path = base_path + "\\" + year
    
    if os.path.isdir(year_path) is False:
        os.mkdir(year_path)

    current_path = base_path+"\\"+pic['name']
    new_path = base_path+"\\"+year+"\\"+pic['name']

    os.rename(current_path,new_path)

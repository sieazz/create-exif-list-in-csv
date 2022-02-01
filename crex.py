from PIL import Image, ExifTags
import csv
import os
import logging

# path
while True:
    path = input("path of the directory: ")
    if os.path.exists(path):
        break
    else:
        print("wrong path")
        pass

logger = logging.getLogger(__name__)

error_handler = logging.FileHandler(str(os.path.basename(path))+".log")
error_handler.setLevel(logging.ERROR)
logger.addHandler(error_handler)

fieldnames = ["FileName", "Width", "Height"] + list(ExifTags.TAGS.values())

# tags to be omitted
omission = ["MakerNote", "UserComment"]
for tag in omission:
    fieldnames.remove(tag)

list_dir = os.listdir(path)

f = open(os.path.basename(path)+".csv", "w+", encoding='utf-8-sig')
reader = csv.DictReader(f)
writer = csv.DictWriter(f, fieldnames = fieldnames, lineterminator='\n')
writer.writeheader()

for filename in list_dir:
    if filename.lower().endswith(('.jpg', '.jpeg', '.tiff', '.wav')):
        try:
            exif_data = {"FileName": filename}
            img = Image.open(path + os.sep + filename)

            if img._getexif():
                for key, value in img._getexif().items():
                    try:
                        exif_data[ExifTags.TAGS[key]] = value
                    except KeyError: # ex) 59932
                        pass

            for tag in omission:
                if tag in exif_data:
                    del exif_data[tag]
            
            exif_data["Width"] = img.size[0]
            exif_data["Height"] = img.size[1]

            writer.writerow(exif_data)
        except Exception as e:
            logger.error(f"{filename}: {type(e)} {e}")
    else:
        pass

f.close()

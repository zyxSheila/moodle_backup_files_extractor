# Moodle Backup File Extractor
The `Download course content` in the More menu can help to download content in courses; but sometimes, the Moodle site may time out if the files are too large to pack up.

In this case, you may consider to `backup` your course and get a `.mbz` file. And this script extracts and renames files from a Moodle course backup (`.mbz` file), organizing them into directories based on their context names. Files without a corresponding context name are placed directly under the `renamed_files` directory.



## Prerequisites

- Python 3.x
- `xml.etree.ElementTree` library (part of the Python standard library)
- `shutil` library (part of the Python standard library)

## Setup and Usage

### Step 1: Extract the Moodle Backup File

1. Download your Moodle course backup file (usually with a `.mbz` extension).
2. Rename the `.mbz` file to `.zip`.
3. Extract the contents of the `.zip` file to a directory of your choice.

In my case (MacOS), I will use the following command lines to avoid losing anything:
```angular2html
mv backupfile.mbz backupfile.tar.gz
mkdir backup_course_folder
tar -xzf backupfile.tar.gz -C backup_course_folder
```

### Step 2: Prepare the Script

1. Update the `extracted_folder` variable in the script to point to your extracted backup folder.

### Step 3: Run the Script


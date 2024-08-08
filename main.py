import os
import xml.etree.ElementTree as ET
import shutil

# Paths
extracted_folder = 'backup_course_folder'  # You may need to update this path
files_folder = os.path.join(extracted_folder, 'files')
files_xml_path = os.path.join(extracted_folder, 'files.xml')
activities_folder = os.path.join(extracted_folder, 'activities')

# Build Context ID to Context Name mapping from activities/folder_<moduleid>/folder.xml
context_mapping = {}

for root_dir, dirs, files in os.walk(activities_folder):
    for dir_name in dirs:
        if dir_name.startswith('folder_'):
            folder_xml_path = os.path.join(root_dir, dir_name, 'folder.xml')
            if os.path.exists(folder_xml_path):
                tree = ET.parse(folder_xml_path)
                root = tree.getroot()
                contextid = root.attrib.get('contextid')
                section_name = root.find('folder/name').text if root.find(
                    'folder/name') is not None else f'contextid_{contextid}'
                if contextid:
                    context_mapping[contextid] = section_name

# Parse files.xml
tree = ET.parse(files_xml_path)
root = tree.getroot()

# Create a directory to store the renamed files
renamed_files_dir = os.path.join(extracted_folder, 'renamed_files')
os.makedirs(renamed_files_dir, exist_ok=True)


# Helper function to find file by contenthash in sub-folders
def find_file_in_subfolders(contenthash):
    for subdir, dirs, files in os.walk(files_folder):
        for file in files:
            if file == contenthash:
                return os.path.join(subdir, file)
    return None


# Process each file entry
for file_entry in root.findall('.//file'):
    component = file_entry.find('component').text
    if component not in ['mod_folder', 'mod_resource']:
        continue

    contenthash = file_entry.find('contenthash').text
    filename = file_entry.find('filename').text
    filepath = file_entry.find('filepath').text
    contextid = file_entry.find('contextid').text  # Get the contextid

    # Find the file in the sub-folders
    original_file_path = find_file_in_subfolders(contenthash)
    if original_file_path is None:
        print(f'File with contenthash {contenthash} not found')
        continue

    # Get the context name from the mapping or use the root if not found
    contextname = context_mapping.get(contextid, '')

    # Construct the full new file path with context name, place under renamed_files if no context name
    if contextname:
        new_file_dir = os.path.join(renamed_files_dir, contextname, filepath.strip('/'))
    else:
        new_file_dir = os.path.join(renamed_files_dir, filepath.strip('/'))
    os.makedirs(new_file_dir, exist_ok=True)
    new_file_path = os.path.join(new_file_dir, filename)

    # Copy the file to the new location with the original name
    shutil.copy2(original_file_path, new_file_path)

print(f'All files from mod_folder and mod_resource have been renamed and saved to {renamed_files_dir}')

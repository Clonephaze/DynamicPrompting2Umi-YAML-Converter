# Smashed together code from multiple sources, edited to work together. AI commented for clarity. 
# There are redunduncies in the code, but they were needed as there were odd formatting issues with some YAML conversions.

import importlib
import sys

# Check if PyYAML module is installed, and if not, install
try:
    print("Checking for PyYAML module...")
    importlib.import_module('yaml')
    print("PyYAML module is detected and ready.")
except ImportError:
    print("PyYAML module is not detected. Installing...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'pyyaml'])

# Check if Ruamel.yaml module is installed, and if not, install
try:
    print("Checking for Ruamel.yaml module...")
    importlib.import_module('ruamel.yaml')
    print("Ruamel.yaml module is detected and ready.")
except ImportError:
    print("Ruamel.yaml module is not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ruamel.yaml"])

import yaml
import subprocess
import os
import re
import ruamel.yaml

# Get the file path from the user or from dropped file
file_path = input("\nReady to convert your YAML file. \n\nEnter the file path or drop the file onto the command window, then press enter: ")
file_path = file_path.replace('"', '').replace("'", "") # Remove quotation marks from the file_path
if len(sys.argv) > 1:
    file_path = sys.argv[1]

print("Please wait, this may take a minute...")

# Load the YAML data
with open(file_path, 'r') as f:
    data = yaml.safe_load(f)


def extract_prompts(data, tags=None):
    if tags is None:
        tags = []

    prompts = []

    # Iterate over the key-value pairs in the data dictionary
    for key, value in data.items():
        # If the value is a dictionary, recursively call extract_prompts with updated tags
        if isinstance(value, dict):
            prompts.extend(extract_prompts(value, tags + [key]))
        else:
            # If the value is a list, iterate over its elements
            if isinstance(value, list):
                for element in value:
                    # Append the element with updated tags to the prompts list
                    prompts.append((element, tags + [key]))
            else:
                # Split the prompt string with spaces
                prompt_lines = value.split(' ')
                for line in prompt_lines:
                    # Replace double underscores with the desired format
                    replaced_line = re.sub(r'__(.*?)__', lambda m: '<[' + m.group(1).replace('/', '][') + ']>', line)
                    # Append the replaced line with updated tags to the prompts list
                    prompts.append((replaced_line, tags + [key]))

    return prompts

prompts = extract_prompts(data)

# Filter out lines starting with a comment character
prompts = [prompt for prompt in prompts if not prompt[0].startswith('#')]

# Split the original file path into base name and extension
base_name, extension = os.path.splitext(file_path)

# Create an empty list to store the new data
new_data = []

# Iterate over each prompt and its corresponding tags
for prompt, tags in prompts:

    # Replace double underscores with square brackets surrounded by greater or lesser than symbols
    prompt = re.sub(r'__(.*?)__', lambda m: '<' + '[%s]' % (m.group(1).replace('/', '][')) + '>', prompt)

    # Remove newlines from the prompt
    prompt = re.sub(r'\n|\r\n', ' ', prompt)

    # Remove single quotes from the prompt
    prompt = prompt.replace("'", "")

    # Create a new dictionary entry with the prompt as the key
    # The entry contains a description and the tags in reverse order
    new_entry = {
        f"'{prompt}'": {
            'Description': ["Auto Yaml Conversion"],
            'Tags': tags[::-1]
        }
    }

    # Append the new entry to the new_data list
    new_data.append(new_entry)

# Create the new file path by appending 'converted' to the base name
new_file_path = f"{base_name}Converted{extension}"

# Write the new data to the new file path
with open(new_file_path, 'w') as file:
    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=4, sequence=2, offset=0)
    yaml.dump(new_data, file)

def replace_text(file_path, old_text, new_text):
    # Open the file in read mode
    with open(file_path, 'r') as f:
        # Read the content of the file
        data = f.read()
    
    # Replace the old text with the new text in the file content
    data = data.replace(old_text, new_text)
    
    # Open the file in write mode
    with open(file_path, 'w') as f:
        # Write the modified content back to the file
        f.write(data)

# Replace the old text with the new text, fixes known issues with coverting the format from DP to UmiAI.
replace_text(new_file_path, "- '''", "'")
replace_text(new_file_path, "'''", "'")
replace_text(new_file_path, "    Description:", "Description:")
replace_text(new_file_path, "   Description:", "  Description:")
replace_text(new_file_path, "    Tags:", "Tags:")
replace_text(new_file_path, "    -", "  -")
replace_text(new_file_path, "- ? '", "'")
replace_text(new_file_path, "     ", " ")
replace_text(new_file_path, "'\":" , "':")
replace_text(new_file_path, "- \"'", "'")
replace_text(new_file_path, "- ? \"'", "'")
replace_text(new_file_path, "'\"\n  :", "':\n")
replace_text(new_file_path, "\"\n:", ":")
replace_text(new_file_path, ",\n", ", ")
replace_text(new_file_path, "\n<", " <")
replace_text(new_file_path, "|\n", "|")
replace_text(new_file_path, "}\n", "}")
replace_text(new_file_path, " # ", " ")
replace_text(new_file_path, "[*]", "")
replace_text(new_file_path, "[*]", "")
replace_text(new_file_path, " #\n", " ")
replace_text(new_file_path, "\\   \ ", "")
replace_text(new_file_path, ">\n", ">")

# Define a function to replace line breaks in a file
def replace_line_breaks(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as f:
        # Read the contents of the file
        data = f.read()
    
    # Find the lines enclosed in single quotes using regular expression pattern matching
    pattern = r"'([^']*)'"
    matches = re.findall(pattern, data)
    
    # Replace line breaks with spaces for each matched line
    for match in matches:
        # Replace line breaks with spaces in the current match
        replaced_match = match.replace('\n', ' ')
        # Replace the original match with the modified match in the data
        data = data.replace("'" + match + "'", "'" + replaced_match + "'")
    
    # Open the file in write mode
    with open(file_path, 'w') as f:
        # Write the modified data back to the file
        f.write(data)

def replace_text_underscores(file_path):
    with open(file_path, 'r') as f:
        data = f.read()  # Read the content of the file
    
    # Find text surrounded in double underscores
    pattern = r"__([^_]+)__"  # Define a regular expression pattern to match text surrounded in double underscores
    matches = re.findall(pattern, data)  # Find all matches of the pattern in the data
    
    # Replace underscores with square brackets surrounded by greater or lesser than symbols
    for match in matches:  # Iterate over each match
        # Separate words if there is a forward slash inside the text
        if "/" in match:  # Check if the match contains a forward slash
            words = match.split("/")  # Split the match into words based on the forward slash
            replacement = "<" + "".join(["[" + word + "]" for word in words]) + ">"  # Create the replacement string
        else:
            replacement = "<[" + match + "]>"  # Create the replacement string
        
        # Replace the matched text with the replacement
        data = data.replace("__" + match + "__", replacement)
    
    with open(file_path, 'w') as f:
        f.write(data)  # Write the modified data back to the file

def convert_to_percentage(file_path):
    with open(file_path, 'r') as f:
        data = f.read()

    pattern = r"(\d\.\d+)::"  # Define a regular expression pattern to match text like "0.4::" or "0.85::"
    matches = re.findall(pattern, data)  # Find all matches of the pattern in the data

    for match in matches:  # Iterate over each match
        percentage = str(int(float(match) * 100)) + "%"  # Convert the match to a percentage
        data = data.replace(match + "::", percentage)  # Replace the matched text with the percentage

    with open(file_path, 'w') as f:
        f.write(data)  # Write the modified data back to the file

# Call the function to replace the text in the file
replace_text(new_file_path, "'\n", "")
# Call the replace_line_breaks function with the specified file path
replace_line_breaks(new_file_path)
# Call the function to convert weighting formats
convert_to_percentage(new_file_path)

pause = input("Done converting Dynamic Prompting YAML format to UmiAI YAML format. Press enter to exit.")
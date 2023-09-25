# DynamicPrompting2Umi-YAML-Converter

## Table of Contents
- [DynamicPrompting2Umi-YAML-Converter](#dynamicprompting2umi-yaml-converter)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Usage](#usage)
  - [Known Issues, things  you'll need to manually fix after running the script.](#known-issues-things--youll-need-to-manually-fix-after-running-the-script)
  - [Credits](#credits)

## Introduction
This Python script, DynamicPrompting2Umi-YAML-Converter, is designed to convert Dynamic Prompting YAML format to UmiAI YAML format. It checks for the necessary modules (PyYAML and Ruamel.yaml), installs them if they are not found, and then proceeds to convert the YAML file. The script also handles text replacements and formatting to ensure the output is in the correct format.

## Requirements
- Python 3.x
- PyYAML module
- Ruamel.yaml module

The script will automatically check for the required modules and install them if they are not found.

## Usage
1. Ensure that you have Python installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).
2. Download the DynamicPrompting2Umi-YAML-Converter script.
3. Double click the downloaded Python script to run it.
4. When prompted, enter the file path of the YAML file you want to convert or drop the file onto the command window, then press enter.
5. Wait for the script to complete the conversion. The converted file will be saved in the same location as the original file with "Converted" added to the file name.

## Known Issues, things  you'll need to manually fix after running the script.
So at the moment there are a few things I am still working on fixing through my script, and until I figure these out you will need to manually fix them. 
  - There are instances in files, usually larger files from testing, where "`\   \`" (2 backslashes with 3 spaces) show up in the output file. These can be removed with a replace all operation in a file editor like notepad++.
  - If your original YAML file contains "`*`", they are culled by the script. Consequently, certain tags may not be converted accurately. For example, if you had something like "`__BoConstructions/*-scifi__`" in your original YAML file, it won't point to a working tag in the converted YAML file. Keep in mind that asterisks don't function in UmiAI for searching random tags. You'll need to specify the specific sci-fi elements you want for each instance where you call it. While I suggest making this adjustment before running the script, the choice is ultimately yours.

## Credits
- Clonephaze (Creator)
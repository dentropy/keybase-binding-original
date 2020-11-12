#!/bin/bash
directory_name=dentropydaemon-export-$(date +"%d-%m-%Y-%T")
mkdir $directory_name
python3 create_export_example.py $directory_name
keybase fs cp -r $directory_name keybase://team/dentropydaemon/exports
rm -r $directory_name
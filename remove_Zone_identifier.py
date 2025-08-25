"""
Script for Danny: every time I move a folder from Windows to WSL, I get a bunch
of excess files that all end with :Zone.Identifier. This script just deletes 
them all, specifically those in the `data` folder (since that's what's getting
moved from Windows to WSL lol).
"""
import os


data_folder = "data"
for root, dirs, files in os.walk(data_folder):
    for filename in files:
        if filename.endswith(":Zone.Identifier"):
            file_path = os.path.join(root, filename)
            os.remove(file_path)
            print(f"Removed {file_path}")
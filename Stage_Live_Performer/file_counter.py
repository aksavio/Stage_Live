import os
import sys
import re

count_lrc = 0

def count_lrc_files(directory='.'):
    """
    Counts .lrc files in specified directory
    Returns -1 on error
    """
    try:
        if not os.path.exists(directory):
            return -1
            
        count = 0
        for entry in os.scandir(directory):
            if entry.is_file() and entry.name.lower().endswith('.lrc'):
                count += 1
        return count
    except Exception as e:
        print(f"Error counting files: {e}", file=sys.stderr)
        return -1
    

def get_lrc_names_sorted(folder_path):
    # List all files in the given folder
    all_files = os.listdir(folder_path)
    
    # Filter for .lrc files with the expected pattern
    lrc_files = [f for f in all_files if f.endswith('.lrc') and re.match(r'\d+_.+\.lrc$', f)]
    
    # Sort the files based on their numeric prefix
    lrc_files.sort(key=lambda x: int(x.split('_')[0]))
    
    # Extract the name part without number prefix and extension
    names = [re.sub(r'^\d+_(.+)\.lrc$', r'\1', f) for f in lrc_files]
    
    return names

def get_lrc_names_sorted_f(folder_path):
    all_files = os.listdir(folder_path)
    lrc_files_f = [f for f in all_files if f.endswith('.lrc') and re.match(r'\d+_.+\.lrc$', f)]
    return lrc_files_f


# Example usage
folder = r"Lyrics"  # <-- Change this to your folder path
name_list = get_lrc_names_sorted(folder)
name_list_f = get_lrc_names_sorted_f(folder)
print(name_list)
print(name_list_f)



import os
from collections import Counter

########## FUNCTIONS THAT DO NOT DEPEND ON OTHER FUNCTIONS ##########
def print_rename_log(old_name, new_name, pad_length):
    '''
    Prints a formatted log of the renaming action.

    Parameters:
    old_name (str): The original name of the subdirectory.
    new_name (str): The new name of the subdirectory after renaming.
    pad_length (int): The length to which the old name should be padded for alignment in the output.
    '''
    print(f'Renamed:    {old_name.ljust(pad_length)}  ->  {new_name}')


def truncated_string(items, max_length=50):
    '''
    Creates a truncated string from a list of items, joining them with commas.

    Parameters:
    items (list): A list of items to be joined and truncated.
    max_length (int): The maximum length of the resulting string. Default is 50.

    Returns:
    str: The concatenated string of items, truncated if it exceeds max_length,
         with '...' appended.
    '''
    items_str = ', '.join(items)

    # Truncate if it exceeds the maximum length
    if len(items_str) > max_length:
        items_str = items_str[:max_length] + '...'

    return items_str
    # return items_str[:max_length] + ('...' if len(items_str) > max_length else '')


def disp_ext_stats_of_file_list(file_names_list):
    '''
    Displays statistics on file extensions in a given list of file names.

    Parameters:
    file_names_list (list): A list of file names to analyze for extension counts.

    Prints:
    A formatted output showing each unique file extension and the number of 
    files associated with that extension.
    '''
    # Create a Counter to count extensions
    extensions = [os.path.splitext(file)[1] for file in file_names_list]
    ext_count = Counter(extensions)

    # Print out the extension statistics
    print(f'Extension    Number of file(s)')
    for ext, count in ext_count.items():
        print(f'{ext}         {count} file(s)')



########## FUNCTIONS THAT DEPEND ON OTHER FUNCTIONS ##########
def rename_subdirs_to_lowercase(dir):
    '''
    Renames all subdirectories in the specified directory to lowercase
    if their names contain any capital letters.
    
    Parameters:
    root_dir (str): The path to the directory to check.
    '''
    # subdirs = os.listdir(dir)
    subdirs = [subdir for subdir in os.listdir(dir) if os.path.isdir(os.path.join(dir, subdir))]
    pad_length = len(max(subdirs, key=len))
    rename_needed = False

    print(f'Renaming subdirs: {truncated_string(subdirs)} --->')
    # print(f'Renaming subdirs: {subdirs}')

    for subdir in subdirs:
        subdir_path = os.path.join(dir, subdir)
        
        if os.path.isdir(subdir_path):  # chech if it's a directory
            if not subdir.islower():    #  check if has any uppercase letters
                new_subdir = subdir.lower() # convert the name to lowercase
                new_subdir_path = os.path.join(dir, new_subdir) # create lowercase dir path
                
                # rename the folder
                os.rename(subdir_path, new_subdir_path)
                print_rename_log(subdir, new_subdir, pad_length)
                rename_needed = True
        else:
            print(f'SKIPPED:  {subdir} is not a directory!')
    if rename_needed == False:
        print(f'SKIPPED:  None renamed')


def rename_img_files_in_order(path, subdir_name, sub_subdir_name):
    '''
    Checks if image files in a specified directory are named
    in a sequemtial order and does so if otherwise.

    Parameters:
    path (str): The path to the directory containing the image files.
    subdir_name (str): The name of the parent subdirectory for naming conventions.
    sub_subdir_name (str): The name of the child subdirectory for naming conventions.

    Prints:
    Logs the renaming process, including the number of files, their extensions,
    and any relevant extension statistics if files have mixed extensions.
    '''
    print(f'Renaming files in "{path}" --->')

    file_names_list = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    max_file_name_length = len(max(file_names_list, key=len))
    # print(file_names_list)

    # Check that files exist in the directory
    len_of_list = len(file_names_list)
    if len_of_list == 0:
        print(f'SKIPPED:  No files in "{path}"')
        return
    print(f'{len(file_names_list)} files')

    # Check that all files are of the same extension (with first file)
    extensions = {(os.path.splitext(file)[1]).lower() for file in file_names_list}    # Get the extensions of all files in a set, in lowercase
    if len(extensions) == 1:
        # All files have the same extension
        detected_extension = extensions.pop()  # Get the single extension
        print(f'CHECK:  All files have the same extension: {detected_extension}')
    else:
        print('FAILED:  All files do not have the same extension')
        disp_ext_stats_of_file_list(file_names_list)    # Display various extensions and number of files with it
        print()
        return
    
    counter = 1
    pad_len = 4

    # Check if files are already named in sequential order
    # First check only first 5 files
    # If passed, then check all files
    for file in file_names_list[:5]:
        if not file.startswith(sub_subdir_name + '__' + subdir_name + '_' + str(counter).zfill(pad_len)):
            break
        counter += 1
    for file in file_names_list[5:]:
        if not file.startswith(sub_subdir_name + '__' + subdir_name + '_' + str(counter).zfill(pad_len)):
            break
        counter += 1
    else:
        print(f'SKIPPED:  Files are already named in sequential order')
        print()
        return
    counter = 1
    
    # Iterate through file list and rename
    for file_name in file_names_list:
        new_file_name = (sub_subdir_name + '__' + subdir_name + '_' + str(counter).zfill(pad_len) + detected_extension).lower()

        # Get file paths
        old_file_name_path = os.path.join(path, file_name)
        new_file_name_path = os.path.join(path, new_file_name)

        # Rename file
        # os.rename(old_file_name_path, new_file_name_path)

        # Print logs
        print_rename_log(file_name, new_file_name, max_file_name_length)

        # Increment counter
        counter += 1
    print()
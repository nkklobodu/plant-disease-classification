import os
# from pathlib import Path
import shutil

########## FUNCTIONS THAT DO NOT DEPEND ON OTHER FUNCTIONS ##########
def create_dir(dest_dir, dir_name_to_create, force_create_new_dir=False):
    '''
    Creates a new directory in the specified destination.

    Parameters:
    dest_dir (str): The path of the destination directory where the new directory will be created.
    dir_name_to_create (str): The name of the directory to be created.
    force_create_new_dir (bool): If True, allows creation of a new directory even if one with the same name exists,
                                  appending a numeric suffix to the new directory name. Default is False.

    Returns:
    str: The name of the directory created, including any suffix added if a directory with the same name already exists.

    Raises:
    FileExistsError: If a directory with the same name already exists and force_create_new_dir is False.
    '''
    created_dir = ''

    # Check if the directory/folder exists
    if not os.path.exists(os.path.join(dest_dir, dir_name_to_create)):
        created_dir = os.path.join(dest_dir, dir_name_to_create)
        os.makedirs(created_dir)
    else:
        if not force_create_new_dir:
            raise FileExistsError(f'Directory {dir_name_to_create} already exists in {dest_dir}')

        # If the directory already exists, add a suffix to the directory name
        i = 1
        while os.path.exists(os.path.join(dest_dir, dir_name_to_create + '_' + str(i))):
            i += 1
        created_dir = os.path.join(dest_dir, dir_name_to_create + '_' + str(i))
        os.makedirs(created_dir)

    # Return the directory path created
    return created_dir


def copy_file(file_name, src_path, dest_path):
    '''
    Copies a file from the source path to the destination path.

    Parameters:
    file_name (str): The name of the file to be copied.
    src_path (str): The source directory where the file is located.
    dest_path (str): The destination directory where the file will be copied.

    Prints:
    The name of the file that was copied. If an error occurs during the copy process,
    an error message will be printed instead.
    '''
    src_file_path = os.path.join(src_path, file_name)
    dest_file_path = os.path.join(dest_path, file_name)
    
    try:
        shutil.copy2(src_file_path, dest_file_path)
        print(f'    {file_name}')
    except Exception as e:
        print(f'ERROR copying {file_name}: {e}')
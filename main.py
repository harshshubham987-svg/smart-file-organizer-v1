"""
AUTOMATION - SMART FILE MANAGER (V1)

This script provides a simple automated solution for organizing files on your system.
It scans a user-specified directory, categorizes each file by its extension, creates
appropriate sub-folders (e.g. Images, Videos, Documents, Apps, etc.) and moves the
files into those folders. The goal is to keep your downloads or any cluttered
folder tidy without manual effort – a lightweight, cross-platform automation
utility.

The code is deliberately straightforward: it uses only the Python standard
library (os, shutil) and makes no external calls, making it safe to run on any
machine. Feel free to extend the detect_type function with additional file
types or custom categorisation rules.
"""
import os
import shutil

#path = "C:\\Users\\HP\\Downloads"

def detect_type(file_path):
    """Detect the type of file based on extension and categorize it.

    Args:
        file_path (str): Full path to the file to analyze.

    Returns:
        str: Category of the file type. Possible returns:
            - "image" for photo files (.jpeg, .jpg, .png)
            - "videos" for video files (.mp4)
            - "Word Files" for Word documents (.docx)
            - "PDF Files" for PDF documents (.pdf)
            - "PPT Files" for PowerPoint presentations (.pptx)
            - "Excel Files" for spreadsheets (.xlsx, .csv)
            - "Apps" for executable files (.exe)
            - "Temp Files" for any other file type not specifically categorized
    """
    # error handling start
    try:
        file_name = os.path.basename(file_path)

        if file_name.lower().endswith('.jpeg') or file_name.lower().endswith('.jpg') or file_name.lower().endswith('.png'):
            return ("image")
        elif file_name.lower().endswith('.mp4'):
            return ("videos")
        elif file_name.lower().endswith('.docx'):
            return ("Word Files")
        elif file_name.lower().endswith('.pdf'):
            return ("PDF Files")
        elif file_name.lower().endswith('.pptx'):
            return ("PPT Files")
        elif file_name.lower().endswith('.xlsx') or file_name.lower().endswith('.csv'):
            return ("Excel Files")
        elif file_name.lower().endswith('.exe'):
            return ("Apps")
        else:
            return ('Temp Files')
    except Exception:
        return ('Temp Files')

def get_files(path):
    """Get a list of all files in the specified directory.

    Args:
        path (str): Directory path to scan for files.

    Returns:
        list: List of filenames (strings) in the directory.
    """
    # error handling start
    try:
        return os.listdir(path)
    # error handling: catch expected errors
    except (FileNotFoundError, PermissionError, OSError):
        return None

def create_folder(path, f_name):
    """Create a new folder if it doesn't exist, returns the full path.

    Args:
        path (str): Parent directory where folder should be created.
        f_name (str): Name of the folder to create.

    Returns:
        str: Full path to the folder (existing or newly created).
    """

    # error handling start
    try:
        full_path = os.path.join(path,f_name)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        return (full_path)
    # error handling: catch expected errors
    except (PermissionError, OSError):
        return None


def move_files(src_file,folder_path):
    """Move a file from source to destination folder.

    Args:
        src_file (str): Full path of the source file to move.
        folder_path (str): Destination folder path.

    Returns:
        str: Status message confirming the move with full destination path.
    """
    # error handling start
    try:
        if not os.path.isfile(src_file):
            return None

        file_name = os.path.basename(src_file)
        full_path = os.path.join(folder_path,file_name)

        # If a file with the same name already exists, create a unique name
        # instead of overwriting the old file.
        if os.path.exists(full_path):
            name, ext = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(full_path):
                full_path = os.path.join(folder_path, f"{name}_{counter}{ext}")
                counter += 1

        shutil.move(src_file,full_path)
        return f"moved :- {full_path}"
    # error handling: catch expected errors
    except (PermissionError, FileNotFoundError, OSError, shutil.Error):
        return None

def organize_files(orig_path):
    """Main organization function - processes files and categorizes them.

    This function is the core of the file organizer:
    1. Gets all files from the specified directory
    2. For each file: detects its type, creates the appropriate folder if needed,
       and moves the file to that folder
    3. Returns a status message indicating success or failure

    The function systematically organizes files by their type extensions,
    creating dedicated folders for each category (images, videos, documents, etc.)

    Args:
        orig_path (str): Original directory path containing files to organize.

    Returns:
        str: Status message - "Work is completed" on success,
             "some thing is wrong!" on failure
    """
    # error handling start
    try:
        if not orig_path or not orig_path.strip():
            return "some thing is wrong!"

        if not os.path.exists(orig_path):
            return "some thing is wrong!"

        if not os.path.isdir(orig_path):
            return "some thing is wrong!"

        lis = get_files(orig_path)
        if lis is None:
            return "some thing is wrong!"

        status = False
        moved_count = 0
        skipped_count = 0
        error_count = 0

        for file in lis:
            src_path = os.path.join(orig_path, file)

            # Skip sub-folders so only actual files are moved.
            if not os.path.isfile(src_path):
                skipped_count += 1
                continue

            #sending the path of each file to detecte function.
            folder_type = detect_type(src_path)
            #now create a new folder in the given address.
            new_path = create_folder(orig_path, folder_type)
            if new_path is None:
                error_count += 1
                continue

            #now we are going to move our files.
            status = move_files(src_path,new_path)
            if status:
                moved_count += 1
            else:
                error_count += 1

        if error_count == 0:
            return "Work is completed"
        else:
            return f"some thing is wrong! Moved {moved_count} files, skipped {skipped_count} folders, {error_count} errors."
    except Exception:
        return "some thing is wrong!"


def main():
    """Entry point of the application - handles user input and execution.

    This function:
    1. Prompts the user to enter a directory path
    2. Cleans and normalizes the input path for cross-platform compatibility
    3. Calls the organize_files function with the processed path
    4. Prints the result of the file organization process

    The path cleaning includes:
    - Removing surrounding quotes (single or double)
    - Escaping backslashes for Windows path compatibility
    - Normalizing path separators for the current OS
    """
    # error handling start
    try:
        user_input = input("Enter your path:- ")

        path = user_input.strip('"\'')
        path = path.replace("\\", "\\\\")
        path_mod = os.path.normpath(path)
        print(organize_files(path_mod))
    except KeyboardInterrupt:
        print("some thing is wrong!")
    except Exception:
        print("some thing is wrong!")


if __name__ = "__main__":
    main()
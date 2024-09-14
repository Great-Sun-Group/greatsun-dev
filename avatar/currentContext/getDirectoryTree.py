import os

def get_directory_tree(root_dir):
    """
    Returns a dictionary representing the directory tree structure with all files.
    """
    directory = {}
    
    # Fetch the contents of the root directory
    filenames = os.listdir(root_dir)
    
    # Iterate over the contents
    for item in filenames:
        path = os.path.join(root_dir, item)
        if os.path.isdir(path):
            # If the item is a directory, recursively call the function
            directory[item] = get_directory_tree(path)
        else:
            # If the item is a file, add it to the dictionary
            directory[item] = None
            
    return directory

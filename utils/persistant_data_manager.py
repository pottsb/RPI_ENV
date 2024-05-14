import json

def write_dict_to_file(dict_data, filename):
    """
    Writes a dictionary to a text file in JSON format.

    Args:
    dict_data (dict): The dictionary to write.
    filename (str): The name of the file where the dictionary will be stored.
    """
    with open(filename, 'w') as file:
        json.dump(dict_data, file, indent=4)  # Indent for pretty printing

def read_dict_from_file(filename):
    """
    Reads a dictionary from a text file in JSON format.

    Args:
    filename (str): The name of the file from which to read the dictionary.

    Returns:
    dict: The dictionary read from the file.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

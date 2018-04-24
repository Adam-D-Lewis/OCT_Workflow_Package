def read_key_value_comment_file(filepath):
    strip_chars = '\t \n'
    with open(filepath, 'r') as file:
        lines = file.readlines()

    key_val_dict = {}
    for line in lines:
        if '=' in line:
            #remove comment
            line = line.split('#')[0].strip(strip_chars)
            #separate into key, value pair
            key, value = line.split('=')
            #strip off strip_chars
            key = key.strip(strip_chars)
            value = value.strip(strip_chars)
            #add to dict
            key_val_dict[key] = float(value)
    return key_val_dict
import configparser


def read_config_file(filepath, section_title=None):
#  returns config if section title isn't given, otherwise it returns the config[section_title] dictionary
    config = configparser.ConfigParser()
    config.read(filepath)
    if section_title is None:
        return config
    else:
        return config[section_title]
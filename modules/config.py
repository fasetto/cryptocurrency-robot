
import os
from configparser import ConfigParser

config = ConfigParser()

path = os.path.join(os.path.dirname(__file__), r'../config.yml')

config.read(path)

token = config['telegram']['token']

def language(user_id):
    lang = None
    try:
        lang = config[str(user_id)]['language']
    except KeyError:
        lang = 'ENG'
    
    return lang

def write(section, **kwargs):
    if str(section) not in config.sections():
        config.add_section(str(section))
    
    for key, value in kwargs.items():
        config[str(section)][str(key)] = str(value)
    
    with open(path, 'w') as stream:
        config.write(stream)

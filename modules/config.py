
import os
from configparser import ConfigParser

config = ConfigParser()

path = os.path.abspath(__file__ + r'\..\..\config.yml')
user_path = os.path.abspath(__file__ + r'\..\..\user.yml')

config.read(path)

token = config['telegram']['token']

def language(chat_id):
    return config[str(chat_id)]['language']

def write(section, **kwargs):
    if str(section) not in config.sections():
        config.add_section(str(section))
    
    for key, value in kwargs.items():
        config[str(section)][str(key)] = str(value)
    
    with open(path, 'w') as stream:
        config.write(stream)

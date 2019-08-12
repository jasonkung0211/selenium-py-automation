import os
from configparser import ConfigParser


class Config:
    def __init__(self, model):
        if '' == model:
            model = 'Default'
        self.config = ConfigParser()
        self.config.read(os.getcwd() + '/config.ini')
        self.hostname = self.config_section(model)['hostname']
        self.timeout = int(self.config_section(model)['max_wait_time'])
        self.page_high = int(self.config_section(model)['screen_high'])
        self.page_width = int(self.config_section(model)['screen_width'])

    def config_section(self, section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def dump(self):
        print(', '.join("%s: %s" % item for item in vars(self).items()))
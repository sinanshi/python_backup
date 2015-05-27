import os
import shutil
import time

from sh import rsync
from collections import namedtuple
import yaml

class param:
    def __init__(self, p_yaml):
        self.backup_list = p_yaml["backup_list"].values()
        self.backup_dir = p_yaml["backup_dir"]
    

# check if directory exist
def check_dir_exist(os_dir):
    if not os.path.exists(os_dir):
        print os_dir, "does not exist."
        exit(1)






if __name__ == "__main__":
    f = open('backup.yaml')
    param_yaml = yaml.safe_load(f)
    f.close()

    p = param(param_yaml)

    for p in p.backup_list:
        print p




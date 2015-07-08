#!/usr/bin/python
import os, sys
import shutil
import time
from sh import rsync
from collections import namedtuple
import yaml


def getDirList(dic):
    back_list = dic.keys()
    exclude_list = []
    for key, value in dic.iteritems():
        if isinstance(value, dict):
            for exdir in value.iterkeys():
                exdpath = key + '/' + exdir
                exclude_list.append(exdpath)
    return back_list, exclude_list


class param:
    def __init__(self, p_yaml, dest):
        self.backlist, self.excludelist = getDirList(p_yaml['backup_dir'])
        self.check_dir_exist(self.backlist)
        self.check_dir_exist(self.excludelist)
        self.backup(dest)


    def check_dir_exist( self, os_dirs ):
        print 'checking listed directories...',
        fail_list = []
        exist = True
        for dir in os_dirs:
            if not os.path.exists(dir):
                fail_list.append(dir)
                exist = False

        if exist != True:
            print '\n[Error] The following floders cannot be found:'
            for f in fail_list: print f
            sys.exit(1)
        else:
            print '[pass]'

    def backup( self, dest ):
        assert len(self.backlist) > 0
        for backdir in self.backlist:
            cmd = 'rsync -aPv '
            cmd = cmd + backdir + ' ' + dest + backdir + ' '
            for exd in self.excludelist: cmd = cmd +' --exclude ' + exd
            if not os.path.isdir(dest + backdir):
                os.makedirs(dest + backdir)
            os.system(cmd)
        



if __name__ == "__main__":
    #get chosen file list from yaml file
    f = open('backup.yaml')
    param_yaml = yaml.safe_load(f)
    f.close()

    p = param(param_yaml, 'xxx')

#    getDirList(param_yaml['backup_dir'])

    #for p in p.backup_list:
    #    print p




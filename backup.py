#!/usr/local/bin/python
import os, sys
import shutil
import time
import yaml
import datetime


def getDirList(dic):
    back_list = dic.keys()
    exclude_list = []
    for key, value in dic.iteritems():
        back_dir_name = key.split('/')[-1]
        if isinstance(value, dict):
            for exdir in value.iterkeys():
                exdpath = back_dir_name + '/' + exdir
                exclude_list.append(exdpath)
    return back_list, exclude_list


def getParam(param_file):
    #get chosen file list from yaml file
    #path = os.path.dirname(os.path.realpath(__file__))
    try:
        f = open( param_file )
    except IOError:
        sys.exit('[Error]: '+param_file+' does not exist!')
        
    param_yaml = yaml.safe_load(f)
    f.close()
    return param_yaml['backup_dir'], param_yaml['dest_dir']



class backup:
    def __init__(self, param_file):
        backup_dir, self.dest = getParam(param_file)
        self.backlist, self.excludelist = getDirList(backup_dir)
        self.check_dir_exist(self.backlist)
        self.backup()


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

    def writelog( self, text ):
        logfile = open("/tmp/sync.log", "a")
        print >> logfile, text
        logfile.close()



    def backup( self ):
        assert len(self.backlist) > 0
        
        print 'start backup...',
        self.writelog( '\n----------------------------' )
        self.writelog( 'Backup start on:  ' + str(datetime.datetime.now()) )
        self.writelog( '----------------------------' )


        for backdir in self.backlist:
            self.writelog( '--> Backup: ' + backdir )
            cmd = 'rsync -av --copy-links --delete-after '
            cmd = cmd + backdir + ' ' +  self.dest + ' '
            for exd in self.excludelist: cmd = cmd +' --exclude ' + exd
            cmd = cmd + ' >> ' + '/tmp' + '/sync.log'
            os.system(cmd)

        self.writelog( '[Finish]' )
        print '[Finish]'


        
if __name__ == "__main__":
    try:
        param_file = sys.argv[1]
    except IndexError:
        sys.exit( '[Error]: parameter file is expected.' )
    backup( param_file )


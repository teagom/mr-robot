#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    output of struct of files and folders for these settings, see array position, config[x]

                    config[3] - (root backup folder)
                    /media/ext-hd/
                                    configx[0] - (app name folder)
                                    www_server/

                                                config[31] - incremental folder name
                                                incremental/

                                                config[1] - model store backup files / frequency of backup (once|daily|week-full|month-full)
                                                data-time/
                                                            log
                                                            log.err
                                                            db.ext
                                                            files.ext

'''

from setting import model
import copy

# # # # # # # # # # # # # # # # # # # # # # # #
# set app array
# # # # # # # # # # # # # # # # # # # # # # # #

config = copy.deepcopy(model)

# global variables of backup
config[0] = 'www_server' # name of config or app (string) Will be used to create a folder backup name
config[1] = 'week-full' # frequency of backup (once|daily|week-full|month-full)
config[2] = False # delete local/temporary backup after copy to remote server (True|False)
                  # if log.err are not empty will be not dropped and a will be send a email to report error.
                  # I will make backup two times, localhost at external HD and remote server
config[3] = '/media/ext-hd' # full path to backup folder or temporary folder
config[4] = True # sendmail after finish backup, log and log.err in attach.
config[5] = 'user@mail.com' # admin email address

# options to compact file and dump of data base
config[6] = 'zip' # extension (string)
config[7] = '/usr/bin/zip' # full path to binary (string)
config[8] = '-9r' # parameters to compact (string)
                  # password(-P passsword), better, faster, recursive, ...
config[9] = '-T'  # parameters to test (string)

# data base settings
config[10] =  True # dump of database (True|False)
config[11] = 'postgres'  # db server (postgres|mysql)
config[12] = '127.0.0.1' # host
config[13] = 'portal_db' # db name
config[14] = 'portal_user' # user
config[15] = 'portal_pass' # pass

# backup files
config[20] = True # compact file and folder
config[21] = ['/var/www/www.company.com'] # include
# to exclude, use * in the end of path.
config[22] = ['/var/www/www.company.com/temp/*','/var/www/www.company.com/.git/*','/var/www/www.company.com/upload/*'] 

# incremental file and folder
config[30] = True  # incremental using rsync (True|False)
config[31] = 'incremental' # incremental folder name (string)
config[32] = ['/etc/default','/etc/apache','/var/www/www.company.com/upload'] # include file and folder (string)
config[33] = ['google-chrome','cacerts'] # exclude file and folder (string) # this file are inside of /etc/default. Declared just file name or folder name without path.

# copy backup to remote server
'''
    Incremental folder will be not duplicated, will be incremental. :)
'''
config[40] = False # copy backup to remote host using rsync ssh (True|False)
config[41] = '192.168.0.254' # server ip or hostname (string)
config[42] = '222' # ssh port (string)
config[43] = '~/backup' # destiny folder in the remote server (string)
config[44] = '-arvz --progress --partial'  # rsync parameters (string)
config[45] = 'password' # authentication type (string), (password|pemfile|autorized)

# password - First connection have to be confirmed written "yes" in a command line.
# sshpass are required - $ sudo apt-get install sshpass
# ssh -p 222 backup@192.168.0.254
# The authenticity of host '([192.168.0.254]:222)' can't be established.
# ECDSA key fingerprint is bb:ee:cc:ee:aa:ff:gg.
# Are you sure you want to continue connecting (yes/no)? 

config[46] = '/opt/server-pem-2015.pem' # pem file if [45] is pemfile (string)
config[47] = 'user' # user (string) is required for any [45] option
config[48] = 'password' # password (string)

# permission section
config[50] = 'user:group' # (string) owner:group for root backup folder, full path to and recursive mode 
config[51] = '700' # (string) chmod for root backup folder.

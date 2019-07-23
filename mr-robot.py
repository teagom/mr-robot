#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from external import cmd_run, sendmail, dateformat

'''
    Mr-Robot-Backup. Dedicated the serie Mr Robot.

    author:
        Tiago de Souza Moraes
        teagom@gmail.com

    required lib:
        argparse
        sshpass

    1 - Dump and compact Data Base
    2 - Compact file and folder
    3 - Sync increment file and folder to incremental folder
    4 - copy backup to remote server
    5 - Set permission of folder and file

    struct of backup folder, see array position, config[x]
                    /x[3]/ (root backup folder)

                        x[0]/ (app name folder)

                            data-time/
                                    increment/
                                    log
                                    log.err
                                    db.ext
                                    files.ext
'''

parser = argparse.ArgumentParser()
parser.add_argument('integers', metavar='file.py', type=str, nargs='+', help='Python file, parameters to make backup. See example.py')
args = parser.parse_args()

# main code 
for cfg in args.integers:

    # import
    module = __import__(cfg.replace('.py', ''))
    x = module.config

    print
    print '# # # # # # # # # # # # # # # # # # # # # # # # #'
    print '# Mr Robot Backup. Dump, compact and increment  #'
    print '# Running %s' % cfg
    print '# # # # # # # # # # # # # # # # # # # # # # # # #'

    # # # # # # # # # # # # # # # # # # # # # # # #
    # create destiny folder and logs

    # root folder to app backup
    base_backup_app = '%s/%s' % (x[3], x[0])

    # once backup
    if x[1] == 'once':
        cmd_destiny_backup_app = 'mkdir -p %s/%s' % (base_backup_app, dateformat('once'))
        destiny_backup_app = '%s/%s' % (base_backup_app, dateformat('once'))

    # daily backup
    if x[1] == 'daily':
        cmd_destiny_backup_app = 'mkdir -p %s/%s' % (base_backup_app, dateformat('daily'))
        destiny_backup_app = '%s/%s' % (base_backup_app, dateformat('daily'))

    # weekly backup
    if x[1] == 'week-full':
        cmd_destiny_backup_app = 'mkdir -p %s/%s' % (base_backup_app, dateformat('week-full'))
        destiny_backup_app = '%s/%s' % (base_backup_app, dateformat('week-full'))

    # monthly backup
    if x[1] == 'month-full':
        cmd_destiny_backup_app = 'mkdir -p %s/%s' % (base_backup_app, dateformat('month-full'))
        destiny_backup_app = '%s/%s' % (base_backup_app, dateformat('month-full'))

    # call shell command
    cmd_run(cmd_destiny_backup_app)

    # create log files
    log = "%s/log" % destiny_backup_app
    log_err = "%s/log.err" % destiny_backup_app

    clean_log = 'rm -f %s' % log
    clean_log_err = 'rm -f %s' % log_err

    create_log = 'touch %s' % log
    create_log_err = 'touch %s' % log_err

    cmd_run(clean_log)
    cmd_run(clean_log_err)

    cmd_run(create_log)
    cmd_run(create_log_err)


    # # # # # # # # # # # # # # # # # # # # # # # #
    # dump data base and compress
    if x[10]:

        # DB backup file name 
        outputfile_db_tmp = u'%s/db.sql' % ( destiny_backup_app )
        outputfile_db = u'%s/db.%s' % ( destiny_backup_app, x[6] )

        # postgres
        if x[11] == 'postgres' :
            dump = 'export PGPASSWORD=%s\npg_dump --username=%s -h %s %s > %s' % ( x[15], x[14], x[12], x[13], outputfile_db_tmp )

        # mysql
        if x[11] == 'mysql' :
            dump = 'MYSQL_PWD="%s" mysqldump -h %s -u %s %s >  %s' % ( x[15], x[12], x[14], x[13], outputfile_db_tmp )

        if x[11]:
            print '> Dump and compact a data base                 '
            compact = '%s %s %s' % ( x[7], outputfile_db, outputfile_db_tmp )
            cmd_run(dump)
            cmd_run(compact, log, log_err, 'dump-database-compact')

            if x[8]:
                test = '%s %s' % ( x[8], outputfile_db )
                cmd_run(test, log, log_err,'dump-database-test-zip')

            cmd_run('rm -f %s' % (outputfile_db_tmp), log, log_err, 'dump-database-delete-sql')

    # # # # # # # # # # # # # # # # # # # # # # # #
    # compress file and folder

    # output file
    outputfile_backup = u'%s/files.%s' % ( destiny_backup_app, x[6] )

    if x[20]:
        print '> Compress file and folder'

        # exclude list
        exclude = ''
        for xx in x[22]:
            exclude += "--exclude \"%s\" " % xx

        # include list
        include = ''
        for xx in x[21]:
            include += "%s " % xx

        # compactor line command
        compact = "%s %s %s %s" % ( x[7], outputfile_backup, include, exclude )
        cmd_run(compact, log, log_err, 'file-folder-compact')

        if x[8]:
            test = '%s %s' % ( x[8], outputfile_backup )
            cmd_run(test, log, log_err, 'file-folder-compact-test')

    # # # # # # # # # # # # # # # # # # # # # # # #
    # increment file and folder
    if x[30]:
        print '> Increment file and folder'

        cmd_destiny_backup_app = 'mkdir -p %s/%s' % ( base_backup_app, x[31] )
        cmd_run(cmd_destiny_backup_app, log, log_err, 'incremental-file-folder')

        include = ""
        for xx in x[32]:
            include += "%s " % xx

        exclude = ""
        for xx in x[33]:
            exclude += "--exclude=\'%s\' " % xx

        rsync = "rsync %s %s %s %s/%s" % ( x[44] , exclude , include , base_backup_app , x[31] )
        cmd_run(rsync, log, log_err, 'file-folder-rsync')


    # # # # # # # # # # # # # # # # # # # # # # # #
    # set permission
    # change permission before transfer to preserve
    # permission at remove server.
    if x[50]:
        c = "chown %s %s -R" % (x[50], base_backup_app)
        cmd_run(c, log, log_err, 'permission-chown')

    if x[51]:
        c = "chmod %s %s -R" % (x[51], base_backup_app)
        cmd_run(c, log, log_err, 'permission-chmod')


    # # # # # # # # # # # # # # # # # # # # # # # #
    # transfer all backup to remote server. 
    # rsync from localhost to remote 
    if x[40]:
        print '> Copy backup to remote server'

        if x[45] == "password":
            rsync = "sshpass -p \"%s\" rsync %s -e \"ssh -p %s\" %s %s@%s:%s" % ( x[48] , x[44] , x[42] , base_backup_app , x[47] , x[41] , x[43] )

        if x[45] == "pemfile":
            rsync = "rsync %s -e \"ssh -p %s -i %s\" %s %s@%s:%s" % ( x[44] , x[42] , x[46] , base_backup_app , x[47] , x[41] , x[43] )

        if x[45] == "authorized":
            rsync = "rsync %s -e \"ssh -p %s \" %s %s@%s:%s" % ( x[44] , x[42] , base_backup_app , x[47] , x[41] , x[43] )

        cmd_run(rsync, log, log_err, 'rsync-backup')


    # sendmail
    # if log.err not empty then sendmail to report
    import os

    if x[4] == True or not os.stat("%s" % log_err).st_size == 0: 
        print '> Send a mail'
        sendmail( x[5], x[0], log_err, log )

    if x[2] == True:
        print '> Delete temporary folder or localhost backup'
        clean = 'rm -rf %s' % ( base_backup_app )
        cmd_run(clean, log, log_err, 'delete-temporary-backup-folder')

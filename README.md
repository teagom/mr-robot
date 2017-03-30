# Mr-Robot backup python script - Dump database, compact, incremental and copy to remote server.
# Dedicated the serie Mr Robot

# download from github
$ git clone https://github.com/teagom/mr-robot.git

$ cd mr-robot

# to copy a example.py
$ cp example.py config_app_name.py

$ chmod 700 config_app_name.py

$ vim config_app_name.py

# new setting
$ cp setting.py.DIST settings.py

$ chmod 700 setting.py

$ vim setting.py

# Security content of this script because user and password.
# Keep safe the content of scripts.
$ chmod 700 mr-robot.py

# run mr-robot backup script
$ mr-robot.py config_app_name.py

--- The ideia of this script is make a full backup for server or app.
	
	Step by step to facility the backup life!
	1	Dump database and compact
	2 	Compact file and folder
	3	Increment file and folder
    4   Copy backup to remote server
    5	Send a mail after finish backup.

	--- struct of file and folder:

        		backup-folder/
                            app_config_name/
                                            incremental/
                                            date-time/ ( maybe more than one backup per day )
                                                        db.ext
                                                        files.ext
                                                        log
                                                        log.err
	
--- config array

	--- base
	0	config or app name ( string )
	1	frequency of backup (once|daily|week-full|month-full)

        frequency
            date-time folder will be created based in frenquency choice.
            folder name will be created based in date-time
            
		crontab will be define backup hour
			example: two times per day
                		12:01 and 00:01 
		        
		once: backup of 1 day ago
            will overwrite last backup and incremental new files,
                                folders and altered files
			output format:
                            /backup/config_name/00h01m
                            /backup/config_name/12h01m
            
		daily: never repeat, never overwrite
            incremental new files, folders and altered files
			output format:
                			/backup/config_name/31_12_2015-00h01m
                            /backup/config_name/31_12_2015-12h01m
                            /backup/config_name/01_01_2016-00h01m
                            /backup/config_name/01_01_2016-12h01m
                            /backup/config_name/...-00h01m
                            /backup/config_name/...-12h01m
                
        week-full: sunday to saturday / backup of 7 days ago
            incremental new files, folders and altered files
			output format:
                            /backup/config_name/sunday_00h01m
                            /backup/config_name/sunday_12h01m
                            /backup/config_name/..._00h01m
                            /backup/config_name/..._12h01m
                            /backup/config_name/saturday_00h01m
                            /backup/config_name/saturday_12h01m
            
		month-full: 01 to 31
			output format:
                            /backup/config_name/01_00h01m
                            /backup/config_name/01_12h01m
                            /backup/config_name/..._00h01m
                            /backup/config_name/..._12h01m
                            /backup/config_name/31_00h01m
                            /backup/config_name/31_12h01m

    2   (True|False)
                    Delete local or temporary backup after copy to remote server
                    If log.err are not empty will be not dropped and a will be send a email to report error.
                    Is possible to make backup two times, in the external HD and remote server, use False.

                    [3] = '/media/usb-hd/  # full path to backup folder
                    [40] = True            # copy to remote server
                    
    3	(string) full path to backup folder
    4   (True|False) sendmail after finish backup
    5   (string) administrator email address
    
    --- compress settings
    6   (string) extension file of compactor program
	7   (string) full path to binary and parameters to compact
    8   (string) full path to binary and parameters to test
    
    --- database
    10  (True|False) Dump database
    11  (string) (postgres|mysql) database server
    12  (string) hostname or ip address
    13  (string) database name
    14  (string) user
    15  (string) password
        
    --- compress file and folder
    20  (True|False) compress file and folder
    21	(array)	Include theses paths to folder or file.
                ['/etc/apache','/var/www/blog']
                
    22 	(array) exclude ['/var/www/blog/temp/*']
    		this folder is not be included
	        use * to exclude all file and folder

    --- incremental file and folder
    30  (True|False)	incremental file and folder
	31  (string)        incremental folder name
    32	(array) [ '/etc/' , ' /var/log' , ' /backup/ ' ]
        include file and folder
	33	exclude	[ 'cacerts','bind9' ]	
				theses files and folders is not be included
                Declared just file name or folder name without path.
    --- copy to remote server
    40  (True|False) to copy to remote server
    41	(string) ip or hostname
    42	(string) port port number
    43	(string) backup folder name in the remote server
    44  (string) rsync parameters '-arvz --progress --partial'
    45  (string) (password|pemfile|autorized)
    46  (string)  full path to ssh pem file if [45] is pemfile
    
    # sshpass are required - $ sudo apt-get install sshpass
    # password - First connection have to be confirmed written "yes" in a line command.
    # backup@host$ ssh -p 222 backup@192.168.0.254
    # The authenticity of host '([192.168.0.254]:222)' can't be established.
    # ECDSA key fingerprint is bb:ee:cc:ee:aa:ff:gg.
    # Are you sure you want to continue connecting (yes/no)?
    47	(string) username
    48	(string) password

    --- permission of backup
    50	(string) owner:group chown
    51	(string) 700         chmod

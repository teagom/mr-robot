#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from setting import debug, sender, smtpserver, username, password

def cmd_run(cmd, log=False, log_err=False, action=False):

    if debug:
        print
        print 'You are seeing this message because debug is True'
        print cmd

    if action:
        os.system("echo '--- %s' 1>>%s 2>>%s" % (action, log, log_err) )

    if not log and not log_err:
        os.system(cmd)
    else:
        os.system(cmd + "> /dev/null 1>>%s 2>>%s" % (log, log_err) )


def sendmail(to, app, attach0=False, attach1=False):

    from smtplib import SMTP_SSL as SMTP
    from email.MIMEText import MIMEText

    destination = [to]

    # read attach
    contentattach = ''
    if attach0 and not os.stat("%s" % attach0).st_size == 0: 
        fp = open(attach0,'rb')
        contentattach += '------------------ Error begin\n\n'
        contentattach += fp.read()
        contentattach += '\n------------------ Error end'
        fp.close()

    if attach1 and not os.stat("%s" % attach1).st_size == 0: 
        fp = open(attach1,'rb')
        contentattach += '\n\n------------------ Success begin\n\n'
        contentattach += fp.read()
        contentattach += '\n------------------ Success end'
        fp.close()

    msg = MIMEText(contentattach, 'plain')
    msg['Subject'] = "Mr.Script %s" % app
    msg['From'] = sender
                    
    try:
        conn = SMTP(smtpserver)
        conn.set_debuglevel(False)
        conn.login(username, password)
        conn.sendmail(sender, destination, msg.as_string())
        conn.close()
    except:
        print '*** Error trying send a mail. Check settings.'


# date format
def dateformat(o):
    '''
        return date format based in frequency set
    '''
    if o == 'daily':
        return datetime.now().strftime("%A-%d_%m_%Y-%HH%MM").lower() # sunday-28_07_2014-14h00m (weekday_day of month-month-year_hour-min)

    if o == 'month-full':
        return datetime.now().strftime("%d-%HH%MM") # 28-14h00m (day of month_hour_min)

    if o == 'week-full':
        return datetime.now().strftime("%A-%HH%MM").lower() # sunday-14h00m (weekday_hour-min)

    if o == 'once':
        return datetime.now().strftime("%HH%MM") # 14h00m (hour-min)

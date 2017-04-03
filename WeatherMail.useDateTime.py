#!/root/.pyenv/shims/python
#-*- coding: UTF-8 -*-

import sys
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import time

#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}]

#dayly target time
t_time=datetime.time(8,0,0)

def send_email(weather_info_html):

    # setup to list
    tolist= ['TO']

    # login 
    fromaddr = "YOU EMAIL"
    fromaddr_pw = "YOUR email PASS"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, fromaddr_pw)

    # make up and send the msg
    msg = MIMEMultipart()
    msg['Subject'] = "Title" + "[" + time.strftime("%a, %d %b", time.gmtime()) + "]"
    msg['From'] = fromaddr
    msg['To'] = ", ".join(tolist)
    msg.attach(MIMEText(weather_info_html, 'html')) # plain will send plain text
    server.sendmail(fromaddr, tolist, msg.as_string())

    # logout
    server.quit()

def weather_notice():

    url='http://www.tenki.jp/forecast/3/17/4610/14203-daily.html' # Hiratsuka City, Japan 

    try:
         html = requests.get(url, headers=hds[0], allow_redirects=False, timeout=3)

         if html.status_code == 200:
             soup = BeautifulSoup(html.text.encode(html.encoding), "html.parser")

             town_info_block = soup.find('div', {'id': 'townWeatherBox'})
             town_info_block = str(town_info_block)
             send_email(town_info_block)

    except Exception as e:
        print(url, e, str(time.ctime()))


def timerRun():
    
    today = datetime.date.today()
    next_target_time=datetime.datetime(today.year,  today.month,   today.day, 
                                       t_time.hour, t_time.minute, t_time.second)

    #start from next day if today now time > sched time
    if datetime.datetime.now() > next_target_time:
        next_target_time =  next_target_time + datetime.timedelta(days=1)

    while True:
        now=datetime.datetime.now()

        if now > next_target_time:
            # inform  when sched time come.
            weather_notice()
            # update target time 
            next_target_time =  next_target_time + datetime.timedelta(days=1)
        # do nothing just wait the next target time
        else:
            pass

        time.sleep(1)

if __name__ == "__main__":
   timerRun()

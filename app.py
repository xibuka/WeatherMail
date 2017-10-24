#!/usr/bin/python
#-*- coding: UTF-8 -*-

import sys
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}]

def send_email(weather_info_html):

    # setup to list
    tolist= ['YOURMAIL@gmail.com', 'YOURMAIL2@gmail.com']

    # login 
    fromaddr = "SENDFROM@gmail.com"
    fromaddr_pw = "PASSWORD"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, fromaddr_pw)

    # make up and send the msg
    msg = MIMEMultipart()
    msg['Subject'] = "Weather inform" + "[" + time.strftime("%a, %d %b", time.gmtime()) + "]"
    msg['From'] = fromaddr
    msg['To'] = ", ".join(tolist)
    msg.attach(MIMEText(weather_info_html, 'html')) # plain will send plain text
    server.sendmail(fromaddr, tolist, msg.as_string())

    # logout
    server.quit()

def weather_notice():

    url='https://tenki.jp/forecast/3/17/4610/14203/'

    try:
         html = requests.get(url, headers=hds[0], allow_redirects=False, timeout=3)

         print (html.status_code)
         if html.status_code == 200:
             soup = BeautifulSoup(html.text.encode(html.encoding), "html.parser")

             town_info_block = soup.find('div', {'class': 'forecast-days-wrap clearfix'})
             town_info_block = str(town_info_block)
             send_email(town_info_block)

    except Exception as e:
        print(url, e, str(time.ctime()))


if __name__ == "__main__":
    weather_notice()

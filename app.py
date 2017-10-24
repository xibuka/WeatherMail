#!/usr/bin/python
#-*- coding: UTF-8 -*-

import sys
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse

#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}]

FROM_ADDR=''
FROM_PASS=''
TO=''

def send_email(weather_info_html):

    # setup to list
    tolist= [TO]

    # login 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM_ADDR, FROM_PASS)

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

    parser = argparse.ArgumentParser()
    parser.add_argument("--to",   help="To email address.")
    parser.add_argument("--gmail",help="gmail account")
    parser.add_argument("--pw",   help="password for gmail account ")
    args = parser.parse_args()
    args = vars(args) 

    FROM_ADDR=args['gmail']
    FROM_PASS=args['pw']
    TO=args['to']

    weather_notice()

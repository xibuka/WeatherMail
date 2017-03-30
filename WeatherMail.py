#-*- coding: UTF-8 -*-

import sys
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

toaddr_file="./toaddr.conf"

def send_email(weather_info_html):

    body = weather_info_html 

    fromaddr = "FROM MAIL ADDR"
    fromaddr_pw = "MAIL PASSWORD"
    toaddr = ""

    # login 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, fromaddr_pw)

    # make up and send the msg
    msg = MIMEMultipart()
    msg['Subject'] = "WeaterMail" + "[" + time.strftime("%a, %d %b", time.gmtime()) + "]"
    msg['From'] = fromaddr

    with open(toaddr_file) as f:
        toaddr_list = f.readlines()
        for toaddr in toaddr_list:
            msg['To'] = toaddr
            msg.attach(MIMEText(body, 'html')) # plain will send plain text
            server.sendmail(fromaddr, toaddr, msg.as_string())

    # logout
    server.quit()

def weather_notice():

    url='http://www.tenki.jp/forecast/3/17/4610/14203-daily.html' # Hiratsuka City, Japan 

    try:
         html = requests.get(url, headers=hds[0], allow_redirects=False, timeout=3)

         if html.status_code == 200:
             soup = BeautifulSoup(html.text.encode(html.encoding), "html.parser")

             town_info_block = soup.find('div', {'id': 'townWeatherBox'})
             send_email(town_info_block)

    except Exception as e:
        print(url, e, str(time.ctime()))

if __name__ == "__main__":
   weather_notice()
import requests
import datetime
import smtplib 
import json
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

time_now = datetime.datetime.now()

content = ""

def news_extraction(url):
    print("[-] Extracting Hacker News Stories...")
    cnt = ""
    cnt +=("<b>HN Top Stories:</b>\n"+"<br>"+"-"*50+"<br>")
    response = requests.get(url)
    content = response.content
    page = BeautifulSoup(content, "html.parser")
    for x, tag in enumerate(page.find_all("td", attrs={"class":"title","valign":""})):
        cnt += ((str(x + 1)+' :: '+ '<a href="' + tag.a.get('href') + '">' + tag.text + '</a>' + '\n' + '<br>') if tag.text !="More" else "")
    print("\n[+] Done Extracting Hacker News Stories")
    return cnt
    


cnt = news_extraction("https://news.ycombinator.com/")
content += cnt
content += ("<br>--------------------------------------------------<br>")
content += ("<br><br>End of Message")

print("\n[-] Composing email...")

with open("settings.json", "r") as file:
    settings = json.load(file)

    SERVER = settings["SERVER"]
    PORT = settings["PORT"]
    FROM_EMAIL = settings["FROM_EMAIL"]
    TO_EMAIL = settings["TO_EMAIL"]
    PASSWORD = settings["PASSWORD"]
   
msg = MIMEMultipart()

msg["Subject"] = "Top News Stories HN [Automated Email]" + " " + str(time_now.day) + "-" + str(time_now.month) + str(time_now.year)
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL

msg.attach(MIMEText(content, "html"))

print('\n[-] Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
server.ehlo()
server.starttls()
server.login(FROM_EMAIL, PASSWORD)
server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

print("\n[+] Email sent")

server.quit()
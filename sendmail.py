import sys;
reload(sys);
sys.setdefaultencoding("utf8")
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib
from lxml import html
from lxml import etree

letters = ['A','B','C','D','E','F','G']
EMAIL = '' //your email (for the mailer client)
PASSWORD = '' //your password 

def getQotD(addresses):
    hof = html.fromstring(urllib.urlopen('http://sat.collegeboard.org/practice/sat-question-of-the-day').read())
    questionID = datetime.date.today().strftime("%Y%m%d")
    typeOfQuestion = hof.find_class("floatLeft qotdLeftCol")[0].find('p').text_content() #Mathematics -> Standard Multiple Choice
    actualInstructions = etree.tostring(hof.find_class('questionStem')[0])
    actualInstructions = actualInstructions.replace("<p class=\"qotdInstruction\"><em><p>","<p style='font-size:16px;'><i>")
    actualInstructions = actualInstructions.replace("</p></em></p>","</i></p>")
    actualInstructions = actualInstructions.replace("&#13;","")
    actualInstructions = actualInstructions.replace('src="/','src="http://sat.collegeboard.com/')
    actualInstructions = actualInstructions.replace('<label for="answer','<label style="font-weight:bold;text-transform:uppercase;"')
    actualInstructions = actualInstructions.replace('<strong','<u')
    actualInstructions = actualInstructions.replace('</strong>','</u>')
    choices = []
    num = 0;
    for i in hof.find_class("qotdChoiceList qotdChoiceList none")[0].findall("li"):
        choices.append(etree.tostring(i.find('label')))

    hts = """<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    </head>
    <body style='font-family: Georgia, Times, "Times New Roman"; font-size: 18px; font-weight:550;'>
    """
    hts = hts + "<p style='font-size:14px'>" + typeOfQuestion + "</p>"
    # hts = hts + "<p style='font-size:16px;'><i>" + italicizedGeneralInstruction + "</i></p>"
    # hts = hts + "<p style='font-size:16px;'>" + actualInstructions
    hts = hts + actualInstructions

    for i in choices:
        hts = hts + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='http://sat.collegeboard.org/practice/answered-question-of-the-day?pageId=practiceQOTD&questionId=" + questionID + "&hintUsed=false&userResponse=" + letters[num] + "&qotdSubmit=Submit'><img src='http://i.imgur.com/LAWAm0J.gif'/></a>&nbsp;&nbsp;" + i + "<p></p>"
        num = num + 1

    hts = hts + "<div style='visibility:hidden;position:absolute;margin-left:-9999px;'>Question created by: <img src='http://www.collegeboard.org/image/cbLogo-local.png'</div> Note - this email service is unaffiliated with Collegeboard."
    hts = hts + "<div><a href='http://sat.collegeboard.org/practice/sat-question-of-the-day?questionId=" + questionID + "'>Link to question</a>"
    hts = hts + "</body></html>"
    sendMail(addresses,hts)

def sendMail(addresses,html):
    toaddr = EMAIL
    bcc = addresses
    message = MIMEMultipart("alternative")
    message['Subject'] = "SAT QotD: " + datetime.date.today().strftime("%m/%d/%y")
    message['From'] = EMAIL
    message['To'] = toaddr

    text = "Please turn on HTML in your email client!"

    htmlMessage = MIMEText(html,'html','utf-8')
    plaintextMessage = MIMEText(text,'plain','utf-8')

    message.attach(plaintextMessage)
    message.attach(htmlMessage)

    toaddresses = [toaddr] + bcc

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, toaddresses, message.as_string())
        server.close()

    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

getQotD([]) #array of emails (as strings)
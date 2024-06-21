import requests
import xlwt
from xlwt import Workbook
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


BASE_URL = 'https://remoteok.com/api'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
REQUEST_HEADER = {
    'User_Agent': USER_AGENT,
    'Aceept-Language': 'en-US, en;q=0.5',

}

#retreive jobs from remote.ok api
def get_job_postings():
    res = requests.get(url=BASE_URL, headers=REQUEST_HEADER)
    return res.json()

#load jobs data to excel sheet
def output_jobs_to_xls(data):
    wb = Workbook()
    job_sheet = wb.add_sheet('Jobs')
    headers = list(data[0].keys())

    for i in range(0, len(headers)):
        job_sheet.write(0, i, headers[i])
    
    for i in range(0, len(data)):
        job = data[i]
        values = list(job.values())
        for x in range(0, len(values)):
            job_sheet.write(i+1, x, values[x])

    wb.save('remote_jobs.xls')

#send emil
def send_email(send_from, send_to, subject, body, files=None):
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date']= formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    for f in files or []:
        with open(f, 'rb') as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        part['Content-Disposition'] = f'attachment; filename="{basename(f)}"'
        msg.attach(part)
    
    smtp = smtplib.SMTP('smtp.gmail.com: 587')
    smtp.starttls()
    smtp.login(send_from, 'fovfzzequyjqmyqy')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if __name__ == "__main__":
    json = get_job_postings()[1:]
    output_jobs_to_xls(json)
    send_email('adesinamubarak123@gmail.com', ['fortunatebusiness111@gmail.com', 'andywork870@gmail.com','apionly123@gmail.com', 'adesinafawziyat@gmail.com'], 'Jobs Posting',
               'Please find attached a list of jobs postings to this email.', files=['remote_jobs.xls'])
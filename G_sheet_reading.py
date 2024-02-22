import pandas as pd
from sqlalchemy import create_engine
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import datetime as dt

date = dt.datetime.today()

date_1 = date.strftime("%m-%d-%Y")


def send_mail(send_from, send_to, subject, text, server, port, username='', password=''):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(recipients)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    smtp = smtplib.SMTP_SSL(server, port)
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()


sender = "sakethg250@gmail.com"
recipients = ["sakethg250@gmail.com", "marcos@crystalwg.com"]
password = "xjyb jsdl buri ylqr"

gsheetid = "178Vx8365dlEqPnsMYL-tUTEroN9zmQl8ebRryC3Zqzs"
sheet_name = "Sheet1"
spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{gsheetid}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(spreadsheet_url)
df_1 = df[['Client_ID','Fecha','Casino','Tipo Comunicación','Motivo','Bono (cuando corresponde)','Comentarios']]

try:
    engine = create_engine(
        'postgresql://orpctbsqvqtnrx:530428203217ce11da9eb9586a5513d0c7fe08555c116c103fd43fb78a81c944@ec2-34-202-53-101.compute-1.amazonaws.com:5432/d46bn1u52baq92', \
        echo=False)

    df_1.to_sql('vip_contact_whatsapp', con=engine, if_exists='replace')

    subject = f'VIP Contacts via Whatsapp Data ingestion for {date_1} is Successful'
    body = f"VIP Contacts via Whatsapp data ingestion for {date_1} is Successful"
    send_mail(sender, recipients, subject, body, "smtp.gmail.com", 465, sender, password)
except Exception as ex:
    subject = f'Helpdesk Data ingestion for {date_1} is Failed'
    body = f"Helpdesk data ingestion for {date_1} is failed due to \n {str(ex)}"
    send_mail(sender, recipients, subject, body, "smtp.gmail.com", 465, sender, password)

import smtplib
from email.mime.text import MIMEText
from config import EMAIL_TO

def send_alert(message):
    msg = MIMEText(message)
    msg['Subject'] = 'GuardELNS Alert'
    msg['From'] = 'alert@guardelns.com'
    msg['To'] = EMAIL_TO
    with smtplib.SMTP('localhost') as server:  
        server.send_message(msg)
    print(message)  

def check_for_alerts(profiles):
    high_risk = profiles[profiles['risk_score'] > 70]
    for _, row in high_risk.iterrows():
        send_alert(f"High risk on {row['src_ip']}: Score {row['risk_score']}")
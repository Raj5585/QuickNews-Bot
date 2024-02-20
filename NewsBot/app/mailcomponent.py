#!/usr/bin/python

import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import nepali_datetime
from datetime import datetime
from QRUtils import display
from qrlib.QREnv import QREnv

class sendMail():

    def __init__(self) -> None:
        self.csv_file = './excelfiles/emails.csv'
        # url = args.url
        self.receiver = 'rajdhakal2056@gmail.com'
        #results= fetch_news()


    def send(self, lst):
        display("---------------sending Mail-----------------")
        keys = ['id', 'keyword', 'title', 'content', 'link', 'newspaper','date_ad','date_bs']
        results = []
        for  i in lst:
            my_dict = {key: value for key, value in zip(keys, i)}
            results.append(my_dict)
        print(results)

        nepali_date = nepali_datetime.date.today().strftime('%Y-%m-%d')
        eng_date = datetime.now().strftime('%Y-%m-%d')
        receivers = []
        with open(self.csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for item in reader:
                try:
                    if(len(item['Emails'])==0):
                        continue
                    receivers.append(item['Emails'])
                except:
                    break

        print(receivers)    
       
            
        Email_address = QREnv.VAULTS['Quickfox']['Email_address']  
        Email_password = QREnv.VAULTS['Quickfox']['Email_password'] 
        display(f"Email Address: {Email_address}")
        display(f"Email Password: {Email_password}")


       
        message = MIMEMultipart()
        #Change the subject to your choice if you wish
        # Adverse Reporting 
        #News coverage Reporting
        message['Subject'] = "Adverse Reporting "
        message['From'] = Email_address
        #message['To'] = receivers

        all_receivers = [self.receiver] + receivers
        display(all_receivers)
    
    
        if(len(results)==0):
            print("No articles to send")
            email_body = "<h2>No Articles Today:</h2>"
            message.attach(MIMEText(email_body, "html"))
        else:
            # Create the email body using HTML format
            email_body = "<h2 style='margin-left:7px; color:black;'>Today's News:</h2>"

            # Append each article to the email body
            for result  in results:
                display(result)
                if(result['date_bs']!=nepali_date) and (result['date_ad'] != eng_date):
                    continue
                print(result)
                email_body += f"""
                    <div style="background-color:#ededed; margin-top:14px; ">

                    <div style="margin-left:7px;">
                    <a style="text-decoration: none;" href='{result['link']}'><span style=" font-size:18px;color:black; font-weight: bold;">{result['title']}</span></a>
                    <span style="font-weight:bold; font-size:13px;font-style:italic; color:#280a4f;"> (#{result['keyword']})</span><br>
                    <span style="color:black;text-decoration: underline;font-weight:bold; font-size:14px;color:#4a4a4a">{result['newspaper']}</span>

                    <span style="font-style:italic;font-weight:bold;font-size:14px; color:#4a4a4a">({result['date_ad']})</span>
                    <div style="padding-bottom:8px;">
                    <p style=" color:black; font-size:14px">{result['content']}
                    <a style="text-decoration: none;" href='{result['link']}'>Read More...</a><br><br>
                    
                    </p>        
                    </div>
                    </div>
                    </div>


                """



        html_content = f"""
                        <html>
                        <body>
                        <div style="border: 1px solid black;border-radius:10px; text-align:centre;print:block;width:100%">
                                
                                <div style="margin-buttom:10px">
                                        {email_body}
                                </div>
                        </div>
                        </body>
                        </html>
                        """
        message.attach(MIMEText(html_content, 'html'))
    
        with smtplib.SMTP('smtp.gmail.com',587) as smtp:
            smtp.starttls()
            try:
                smtp.login(Email_address, Email_password)
                display("Logged in to Email")
            except:
                display("Login Failed")

            display("Sending Email")
            try:
                # message = "From: %s\r\n" % Email_address + "To: %s\r\n" % reciever + "CC: %s\r\n" % ",".join(cc) + "Subject: %s\r\n" % message['Subject'] + "\r\n"  + "hello"
                # to = [reciever] + cc 
                
                smtp.sendmail(Email_address, all_receivers, f'{message}')
                display(f"Email Sent to {all_receivers}")
            except Exception as e:
                display("Failed to send Email")
                display(e)


    
       
I have  pandas dataframe. In that dataframe i have many 10 columns.
The 2nd last column is Reject_Warn_Reason and last column is ManagerEmail.

1. I want to groupby on ManagerEmail column
2. Send email of grouped data to that Manager Email.

Code:

def send_reject_mail(self, data_vendors):
    # Group records by manager email
    logging.info(f"deepak data_vendors: \n{data_vendors.to_string()}")

    grouped_by_manager = data_vendors.groupby('ManagerEmail')
    logging.info(f"deepak grouped_by_manager: {grouped_by_manager}")

    with open(self.configstream['VENDOR_ProjConfig']['notification_reject_config'], 'r') as file:
        config = yaml.safe_load(file)

    for key in config.keys():
        if config[key]['is_enabled'] == 'Y':
            mail_subject = config[key]['MAIL_SUBJECT']
            mail_text = config[key]['MAIL_TEXT']

            for manager_email, group in grouped_by_manager:
                logging.info(f"deepak manager_email: {manager_email} ({type(manager_email)})")
                logging.info(f"deepak group: \n{group.to_string()}")

                to_email = ', '.join([manager_email] + self.mail_to)
                logging.info(f"deepak to_email: {to_email} ({type(to_email)})")

                # Create email message
                message = MIMEMultipart()
                message['From'] = formataddr((strHeader(self.mail_sender_name, 'utf-8'), self.mail_from))
                message['To'] = to_email
                message['Subject'] = mail_subject

                # Attach email body
                message.attach(MIMEText(mail_text))

                # Attach CSV file
                attachment = group.to_csv(index=False)
                part = MIMEText(attachment)
                part.add_header('Content-Disposition', 'attachment', filename="rejected_vendor_records.csv")
                message.attach(part)

                # Send email
                server = smtplib.SMTP(self.mail_server, self.mail_port)
                server.sendmail(self.mail_from, to_email.split(','), message.as_string())
               

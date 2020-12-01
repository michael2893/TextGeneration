import email_poem from emailPoem.py 

def send_mail():

	fromaddr = "dailymeditationsforyou@gmail.com"
	recip = []
	msg = MIMEMultipart()

	msg['From'] = fromaddr
	msg['To'] = ", ".join(recipients)
	msg['Subject'] = "Todays's Poem"

	body = email_poem(model)

	msg.attach(MIMEText(body, 'plain'))




	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


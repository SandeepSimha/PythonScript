# Python code to illustrate Sending mail from
# your Gmail account
import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login("srisapetest@gmail.com", "Sapient@17")

# message to be sent
message = "Message_you_need_to_send"

# sending the mail
s.sendmail("chsandeep511@gmail.com", "chsandeep511@gmail.com", message)

# terminating the session
s.quit()

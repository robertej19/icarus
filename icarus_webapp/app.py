from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail= Mail(app)

with open('.mail') as f: mail_pass = f.read()

print(mail_pass)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'icarus.messenger@gmail.com'
app.config['MAIL_PASSWORD'] = mail_pass
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def index():
   msg = Message('Notifications', sender = 'no.reply.icarus@gmail.com', recipients = ['robertej17@gmail.com'])
   msg.body = "Fire Alerts"
   mail.send(msg)
   return "Message Sent"

if __name__ == '__main__':
   app.run(debug = True)
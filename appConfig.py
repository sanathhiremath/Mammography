from flask import Flask

app = Flask(__name__)

# DB Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:sanath@localhost:5432/Mammogram"

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_SENDER'] = "Mammo Diagnostics"
app.config['MAIL_USERNAME'] = 'snehanarayan789@gmail.com'  # enter your email here
app.config['MAIL_PASSWORD'] = 'ambika1234'

# Json Configuration
app.config["JSON_SORT_KEYS"] = False

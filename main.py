from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("homepage.html")

@app.route('/doctor')
def doctor():
    return render_template("doctorhomepage.html")

@app.route('/doctor/doctorregistration')
def doctorregistration():
    return render_template("doctorregistration.html")

if __name__=="__main__":

    app.run(debug=True)
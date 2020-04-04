from appConfig import app


@app.route('/api/doctor', methods=['GET', 'POST'])
def doctorAPI():
    user = ""
    if request.method == 'GET':
        username = "sanath.hiremath@yahoo.com"
        password = "Sanath"

        user = db.session.query(DoctorModel).filter_by(email=username).first()

        db.session.commit()
        if user is None:
            return render_template("homepage.html")
        elif password != user.password:
            return render_template("homepage.html")
        else:
            return jsonify(user.password)
    else:
        return user

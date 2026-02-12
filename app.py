from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def func():
    doctor = {
        "name": "sishir",
        "speciality": "sishir",
        "about": "sishir",
        "rating": 2,
        "photo": "sishir",
        "status":0
    }
    return render_template("profileseenbydoctor.html", doctor=doctor)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# PostgreSQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123@localhost:5432/admin"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model definition
class Registerpage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    pas = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.name}"

# Registration route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        pas = request.form['pas']

        if password != pas:
            return jsonify({"message": "Passwords do not match"}), 400

       
        new_user = Registerpage(name=name, email=email, phone=phone, password=password, pas=pas)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))


    show = Registerpage.query.all()
    return render_template("register.html", show=show)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = Registerpage.query.filter_by(email=email, password=password).first()

        if user:
            # session['user'] = user.name
            return redirect(url_for('homepage'))
        else:
            return "Invalid credentials", 401

    return render_template("login.html")


@app.route("/homepage",methods=["POST","GET"])
def homepage():
    show=Registerpage.query.all()
    return render_template("home.html",show=show)
   
@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))
    

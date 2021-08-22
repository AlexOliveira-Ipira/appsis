from flask import Flask , redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'docker'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    cep = db.Column(db.Integer)

    def __init__(self, name, email, cep):
        self.name = name
        self.email = email
        self.cep = cep


@app.route('/')
@app.route('/home')
def home():
    if "user" in session:
            user = session["user"]
            return render_template("index.html", user=user)
    else:
        return render_template('index.html')

@app.route('/conectado')
def conectado():
    user = session["user"]
    return render_template('conectado.html', user=user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['nameusr']
        session['user'] = user 
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session['email'] = found_user.email 
            session['cep'] = found_user.cep
        else:
            usr = users(user, '', '')
            db.session.add(usr)
            db.session.commit()

        flash('Conectado no site com sucesso!')
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            flash('Você já esta conectado!')
            return redirect(url_for('conectado'))
    return render_template('login.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    email=None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email=request.form["email"]
            cep=request.form['cep']
            session["email"]= email
            session["cep"] = cep
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            found_user.cep = cep 
            db.session.commit()
            flash("Dados salvo com sucesso")
        else:
            if "email" in session:
                email = session["email"]
            return render_template("user.html", user=user)
    else:
        flash("Você já tem cadastro, identificar melhor loop para essa mensagem!")
    return redirect(url_for("home"))

@app.route('/logout')
def logout():
    session.pop('user', None)   
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/view', methods=["POST", "GET"])
def view():
    email = None
    if "email" in session:
        email = session["email"]
        cep = session['cep']
        found_user = users.query.filter_by(email=email)
        #found_user = users.query.all()

        if request.method == "POST":
            email = request.form["email"]
            cep = request.form["cep"]
            pulled_user = users.query.all().first()
            pulled_user.name = [email,cep]
            db.session.commit()

            flash("Account Successful updated. Cheers")

        return render_template("view.html", dados=found_user)
    else:
        flash("Desculpe, você precisa esta conectado para ver essa pagina")
        session.permanent = False
        return redirect(url_for("login"))
    
if __name__ =='__main__':
    db.create_all()
    app.run(debug=True , port=8880)
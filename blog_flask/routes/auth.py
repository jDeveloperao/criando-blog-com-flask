from flask import Blueprint , render_template , redirect , request , url_for , flash
from auth_services import create_user , get_data , user_login , user_logout
from models.user import User
from flask_login import login_user , current_user , login_required

auth_bp = Blueprint("auth" , __name__)

@auth_bp.route("/users/cadastro" , methods = ["GET" , "POST"])
def cadastro():

    if request.method == "POST":
        nome_form = request.form.get("nome")
        email_form = request.form.get("email")
        senha_form = request.form.get("senha")

        dados , erros = get_data(nome_form , email_form , senha_form)

        if erros:

           flash(erros)
           return redirect(url_for("auth.cadastro"))
    
        user , erro = create_user(dados , User)

        if erro:
           flash(erro)
           return redirect(url_for("auth.cadastro"))
        else:
            flash("Usuario cadastrado com sucesso!")
            return redirect(url_for("auth.login"))
        
    
    return render_template("cadastro.html")

        
    
@auth_bp.route("/users/login" , methods = ['GET' , 'POST' ])
def login():


    if request.method == "POST":
        email = request.form.get("email" ,"").strip()
        senha = request.form.get("senha")

        user , erro =   user_login(email , senha , User)

        if erro:

            flash(erro)
            return redirect(url_for("auth.login"))
        flash("O login foi feito com sucesso!")
        return redirect(url_for("user.dashboard"))
    
    return render_template("login.html")

@auth_bp.route("/users/logout")
@login_required

def logout_user():
    user_logout()
    flash("Saiu com sucesso!")
    return redirect(url_for("auth.login"))



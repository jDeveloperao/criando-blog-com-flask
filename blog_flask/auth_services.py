from extensios import db
from extensios import lm
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import login_user , logout_user , current_user 


def get_data(nome , email , senha):

    if not nome or not email or not senha:
        return None, "Todos os campos sao obrigatorios!"
    
    if len(nome) < 6:
        return None, "O nome deve ter no minimo 6 caracters!"
    
    if "@" not in email:
        return None, "Email invalido!"
    if "." not in email:
        return None, "Email invalido!"
    
    if len(senha) < 6:
        return None, "A senha deve ter no minimo 6 caracters!"
    
    return [nome , email , senha] , None


def create_user(dados , model):

    user = model.query.filter_by(email = dados[1]).first()

    if user:
        return None, "Este usuario ja existe!"
    else:

        new_user = model(

            nome = dados[0] ,
            email = dados[1] ,
            senha = generate_password_hash(dados[2])
        )


        try:

            db.session.add(new_user)
            db.session.commit()
        except Exception as erro:
            
            db.session.rollback()
            return None , "Houve um erro ao registrar o usuario!"
        
    return user , None

def user_login(email , senha , model):

    if not email or not senha:
        return None, "Todos os campos sao obrigatorios!"
    
    user = model.query.filter_by(email = email).first()

    if not user:
        return None , "Usuario ou senha incorrectos!"
    if not check_password_hash(user.senha , senha):
        return None, "Usuario ou senha incorrectos!"
    login_user(user)

    return user , None

def user_logout():

    return logout_user()



        
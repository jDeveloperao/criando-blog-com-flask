from flask_login import current_user
from extensios import db 


def get_data(titulo , conteudo):

    if not titulo or not conteudo:
        return None , "Os dados do post nao podem ser vazios!"
    
    return [titulo , conteudo ] , None

def create_post(dados , Model):

    new_post = Model(
        titulo = dados[0] , 
        conteudo = dados[1] ,
        dono = current_user.id ,
        nome_dono = current_user.nome
    )

    try:
        db.session.add(new_post) 
        db.session.commit()
    except Exception as erro:
        print(erro)
        db.session.rollback()
        return None, "Houve um erro ao criar post!"
    
    
    return new_post , None

def publicar_post(Model , id):

    post = Model.query.get_or_404(id)

    post.estado = not post.estado

    try:
        db.session.commit()
    except Exception as erro:
        db.session.rollback()
        return None, "Houve um erro ao publicar post!"
    
    return None

def delete(Model , id):

    post = Model.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()
    except Exception as erro:
        db.session.rollback()
        return None, "Houve um erro ao apagar o post!"
    
    return None

def edit_pos(Model , titulo , conteudo , id):

    if not titulo or not conteudo:
        return None, "Todos campos sao obrigatorios!"
    
    post = Model.query.get_or_404(id)

    post.titulo = titulo
    post.conteudo = conteudo

    try:
        db.session.commit()
    except Exception as erro:
        db.session.rollback()
        return None , "Houve um erro ao actualizar a publicacao!"
    
    return None


    




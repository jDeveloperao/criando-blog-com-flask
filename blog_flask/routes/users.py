from flask import Blueprint , render_template , request , url_for , flash , redirect
from extensios import db
from models.post import Post
from users_services import get_data , create_post , publicar_post , delete , edit_pos
from flask_login import login_required , current_user

user_bp = Blueprint("user" , __name__ )


@user_bp.route("/profile" , methods = ["GET"])
def profile():
    return render_template("profile.html")


@user_bp.route("/feed" , methods = ["GET"])
@login_required
def feed():

    posts = Post.query.filter_by(estado = 1).all()

    return render_template("feed.html" , posts = posts)

@user_bp.route("/dashboard" , methods = ["GET" , "POST"])
@login_required
def dashboard():

    publicados = []
    nao_publicados = []

    posts = Post.query.filter_by(dono = current_user.id).all()

    for post in posts:

        if post.estado:

            publicados.append(post)
        
        if not post.estado:

            nao_publicados.append(post)
    
    
    
    return render_template("dashboard.html" , posts = posts , nao_publicados = nao_publicados , publicados = publicados)

@user_bp.route("/new/post" , methods = ["GET" , "POST"])
@login_required
def cadastro():


    if request.method == "POST":

        titulo = request.form.get("titulo")
        conteudo = request.form.get("conteudo")



        dados , erro = get_data(titulo , conteudo )

        if erro:
            flash(erro)
            return redirect(url_for("user.cadastro"))
        
        post , erro_post = create_post(dados , Post)

        if erro_post:

            flash(erro_post)
            return redirect(url_for("user.cadastro"))
        
        flash("Post criado com sucesso!")
        return redirect(url_for("user.dashboard"))


    return render_template("cadastro_post.html")

@user_bp.route("/edit/post<int:id>" , methods = ['GET' , 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)

    if current_user.id != post.dono:

        flash("Forbiden!")
        return redirect(url_for("user.dashboard"))

    if request.method == 'POST':

        titulo = request.form.get("titulo")
        conteudo = request.form.get("conteudo")

        erro = edit_pos(Post , titulo , conteudo , id)

        if erro:

            return redirect(url_for("user.edit_post" , id = post.id))
        
        flash("Post editado com sucesso!")
        return redirect(url_for('user.dashboard'))

    return render_template("edit_post.html" ,  post = post)

@user_bp.route("/publicar/post<int:id>")
@login_required
def publicar(id):

    post = Post.query.get_or_404(id)

    if current_user.id != post.dono:
        flash("Forbiden")
        return redirect(url_for("user.dashboard")) 

    erro = publicar_post(Post , id)

    if erro:
        flash(erro)
        return redirect(url_for("user.dashboard"))
    
    flash("Post publicado com sucesso!")
    return redirect(url_for("user.dashboard")) 

@user_bp.route("/delete/post<int:id>" , methods = ["POST"])
def delete_post(id):

    post = Post.query.get_or_404(id)

    if current_user.id != post.dono:
        flash("Forbiden")
        return redirect(url_for("user.dashboard")) 



    erro = delete(Post , id)

    if erro:
        flash(erro)
        return redirect(url_for("user.dashboard"))
    
    flash("Post apagado com sucesso!")
    return redirect(url_for("user.dashboard"))  




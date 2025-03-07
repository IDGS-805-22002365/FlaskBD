from flask import Flask, render_template,request,redirect,url_for
from flask import flash,g  #la g es de variables globales
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig

import forms
from models import db
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect(app)

# @app.route("/")
# @app.route("/index")
# def index():
# 	return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/", methods=["GET", "POST"]) 
@app.route("/index")
def index():
    create_form = forms.UserForm2(request.form)
    alumno = Alumnos.query.all()
    return render_template("index.html", form=create_form, alumno=alumno)

@app.route("/detalles",methods=["GET", "POST"])
def detalles():
    create_form=forms.UserForm2(request.form)
    if request.method == "GET":
        id=request.args.get('id')
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        nom=alum1.nombre
        ape=alum1.apaterno
        email=alum1.email
    return render_template("detalles.html",form=create_form,nombre=nom,apellidoP=ape,Email=email)

@app.route("/Alumnos1",methods=["GET", "POST"]) 
def Alumnos1():
    create_form=forms.UserForm2(request.form)
    if request.method == "POST":
        alum=Alumnos(nombre=create_form.nombre.data,
			apaterno=create_form.apaterno.data,
			email=create_form.email.data)
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("Alumnos1.html",form=create_form)

@app.route('/editar',methods=["GET","POST"])
def modificar():
    create_form=forms.UserForm2(request.form)
    if request.method == "GET":
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.nombre.data=alum1.nombre
        create_form.apaterno.data=alum1.apaterno
        create_form.email.data=alum1.email
    if request.method == "POST":
        id = create_form.id.data
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum1.nombre = create_form.nombre.data
        alum1.apaterno = create_form.apaterno.data
        alum1.email = create_form.email.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("editar.html", form=create_form)
        
@app.route('/eliminar', methods=["GET", "POST"])
def eliminar():
    create_form = forms.UserForm2(request.form)
    if request.method == "GET":
        id = request.args.get('id')
        # select * from alumnos where id=id
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alum1 is None:
            flash('Registro no encontrado', 'error')
            return redirect(url_for('index'))
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apaterno.data = alum1.apaterno
        create_form.email.data = alum1.email
    if request.method == "POST":
        id = create_form.id.data
        alum = Alumnos.query.get(id)
        # delete from alumnos where id=id
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("eliminar.html", form=create_form)



if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()
 
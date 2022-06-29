
from flask import Flask, jsonify, redirect, request, session,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import  Marshmallow
from flask import flash
import forms
from flask_wtf.csrf import CSRFProtect 
import consulta


host1 = 'mysql-81434-0.cloudclusters.net'
port1 = 13003
user1 = 'marcos6533'
passwd1 = 'marcos12'
db1 = 'votaciones'
   
         

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://marcos6533:marcos12@mysql-81434-0.cloudclusters.net:13003/votaciones'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)
app.secret_key= 'my_secret_key'
csrf = CSRFProtect(app)

#Creacion de la tabla
class usuarios(db.Model):
    cat_id = db.Column(db.Integer,primary_key=True)
    nombre =db.Column(db.String(20))
    apellido =db.Column(db.String(20))
    cedula = db.Column(db.String(10),unique=True)
    expedicion = db.Column(db.String(10))
    voto = db.Column(db.String(2))
    
    def __init__(self,nombre,apellido,cedula,expedicion,voto):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula=cedula
        self.expedicion=expedicion
        self.voto=voto
 
 
        
db.create_all()


#Esquema Categoria 
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id','nombre','apellido','cedula','expedicion','voto')   
             
#Una respuesta             
categoria_schema = CategoriaSchema()  
#Muchas respuestas
categorias_schema = CategoriaSchema(many=True)

#GET
@app.route('/categoria',methods=['GET'])
def get_categorias():
    all_categorias = usuarios.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)        

#GET POR ID
@app.route('/categoria/<id>',methods=['GET'])
def get_categoria_x_id(id):
    una_categoria = usuarios.query.get(id)
    return categoria_schema.jsonify(una_categoria) 

@app.route('/login', methods=['GET','POST'])
def login():
    login_form=forms.LoginForm(request.form)
    cedula=login_form.cedula.data
    if request.method=='POST':      
        if consulta.verificar(cedula)==True:
            return render_template('html/votacion.html')
        else:
            success_message ='No esta registrado!!!'                 
            flash(success_message)
    return  render_template('html/login.html',form=login_form) 

    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('html/404.html')

@app.errorhandler(500)
def page_not_found(e):
    return render_template('html/500.html')

@app.route('/admin')
def admin():
   num_personas_habilitadas = consulta.Numero_personas_habilitas()
   num_personas_votaron = consulta.Numero_personas_votaron()
   num_personas_no_votaron=consulta.Numero_personas_no_votaron()
   return render_template('html/admin.html',num_personas_habilitadas=num_personas_habilitadas,num_personas_votaron=num_personas_votaron,num_personas_no_votaron=num_personas_no_votaron)  
   
#POST #########
@app.route('/registrar',methods=['POST','GET'])
def insert_categoria():
    register_form=forms.RegisterForm(request.form)
    username=register_form.username.data
    apellido=register_form.apellido.data
    cedula=register_form.cedula.data
    expedicion=register_form.expedicion.data
    voto='No'
    if request.method=='POST':
       if consulta.verificar(cedula)==True:
           success_message ='Ya esta registrado!!!'
           flash(success_message) 
       else:
            Insertar(username,apellido,cedula,expedicion,voto)
            
                 
    return render_template('html/registrar.html', form=register_form)

def Insertar(username,apellido,cedula,expedicion,voto):         
    nuevocategoria= usuarios(username,apellido,cedula,expedicion,voto)   
    try:
        db.session.add(nuevocategoria)
        db.session.commit()
        success_message ='Registrado correctamente'
        flash(success_message)        
    except Exception as ex:
        print(ex)      
        
#PUT #########
@app.route('/categoria/<cedula>',methods=['PUT'])   
def update_categoria(cedula):
    actualizar = usuarios.query.get(cedula)
    
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    cedula=request.json['cedula']
    expedicion=request.json['expedicion']
    voto=request.json['voto']
     
    actualizar.nombre=nombre
    actualizar.apellido= apellido
    actualizar.cedula= cedula
    actualizar.expedicion= expedicion
    actualizar.voto= voto
    db.session.commit()
    
    return categoria_schema.jsonify(actualizar)

#DELETE
@app.route('/categoria/<cedula>',methods=['DELETE'])
def delete_categoria(cedula):
    eliminar_user = usuarios.query.get(cedula)
    db.session.delete(eliminar_user)
    db.session.commit()
    return categoria_schema.jsonify(delete_categoria)


#Mensaje de Bienvenida
@app.route('/',methods=['POST','GET'])
def index():  
    con_form=forms.ContactForm(request.form)
    nombre=con_form.nombre.data
    email=con_form.email.data
    comentario=con_form.message.data 
    return render_template('index.html',form=con_form)


@app.route('/logout')
def logout():
        return redirect(url_for('insert_categoria')) 

if __name__ == '__main__':
   app.run(debug=True)
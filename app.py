from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

from forms import PetForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'password'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """Returns home page"""
    pets = Pet.query.all()

    return render_template('home.html', pets=pets)

@app.route('/add', methods=["POST", "GET"])
def new_pet_form():
    """Renders Pet Form and handles submission"""
    form = PetForm()

    if form.validate_on_submit():
        name= form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('pet_add.html', form=form)

@app.route('/pets/<int:pet_id>')
def show_pet(pet_id):
    """ Renders detail page for pet"""
    pet = Pet.query.get_or_404(pet_id)
    return render_template('pet_details.html', pet=pet)
    
@app.route('/pets/<int:pet_id>/edit', methods=["GET", "POST"])
def edit_pet(pet_id):
    """Renders Pet Edit Form and handles submission"""
    pet = Pet.query.get_or_404(pet_id)
    form = PetForm(obj=pet)

    if form.validate_on_submit():
        pet.name= form.name.data
        pet.species = form.species.data
        pet.photo_url = form.photo_url.data
        pet.age = form.age.data
        pet.notes = form.notes.data

        
        db.session.add(pet)
        db.session.commit()

        return redirect(f'/pets/{pet.id}')


    return render_template('pet_edit.html', form=form, pet=pet)

@app.route('/pets/<int:pet_id>/delete', methods=["POST"])
def delete_pet(pet_id):
    """Handles delete of Pet"""
    pet = Pet.query.get_or_404(pet_id)

    db.session.delete(pet)
    db.session.commit()
    return redirect('/')

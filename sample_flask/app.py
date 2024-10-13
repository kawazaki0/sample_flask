from flask import Flask, redirect, url_for, flash
from flask import render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
    app.register_blueprint(convert_bp)
    app.register_blueprint(greet_bp)
    app.register_blueprint(homepage_bp)
    app.register_blueprint(storage_bp)
    return app


db = SQLAlchemy()

convert_bp = Blueprint("convert", __name__, url_prefix='/convert')
homepage_bp = Blueprint("homepage", __name__, url_prefix='/')
greet_bp = Blueprint("greet", __name__, url_prefix='/greet')
storage_bp = Blueprint("storage", __name__, url_prefix='/storage')


@greet_bp.route('/hello/<name>')
def greet(name):
    if name == 'admin':
        return 'Access denied', 401
    return f'Hello, {name}!'


@convert_bp.route('/<float:amount>/<currency>')
def convert(amount, currency):
    rate = {'USD': 3.92, 'EUR': 4.31}.get(currency.upper())
    if rate is None:
        return f'Invalid currency "{currency}"', 400
    return f'{amount} in {currency} = {amount * rate} PLN'


class EntryForm(FlaskForm):
    key = StringField('Key', validators=[DataRequired(), Length(max=16)])
    value = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Entry {self.key}={self.value}>'


@storage_bp.route('/')
def main():
    return f'What can I do for you?'


@storage_bp.route('/save/<key>/<value>')
def save_db(key, value):
    return f'Just saved: {key}={value}!'


@storage_bp.route('/load/<key>')
def load_db(key):
    values = Entry.query.filter_by(key=key).all()
    numbers_str = ', '.join(str(number.value) for number in values)
    return f'Retrieved {numbers_str}!'


@homepage_bp.route("/", methods=['GET'])
def index():
    return render_template("index.html", items=Entry.query.all(), form=EntryForm())


from flask import request


def add_to_db(key, value):
    new_instance = Entry(key=key, value=value)
    db.session.add(new_instance)
    db.session.commit()


@homepage_bp.route('/submit', methods=['POST'])
def submit():
    form = EntryForm()
    if form.validate_on_submit():
        key = form.key.data
        value = form.value.data
        add_to_db(key=key, value=value)
        flash(f'Successfully added {key}={value}', 'success')
        return redirect(url_for('homepage.index'))
    else:
        flash(f'Incorrect data', 'error')
        return redirect(url_for('homepage.index'))


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.init_app(app)
        db.create_all()
    app.run(debug=True)

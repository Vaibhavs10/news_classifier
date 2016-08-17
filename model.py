from wtforms import Form, TextField, validators, IntegerField

class InputForm(Form):
    a = TextField(label='Headline: ', default='', validators=[validators.InputRequired()])

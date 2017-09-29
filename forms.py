
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators

EVIDENCE_CHOICE = [('iea','Inferred from Electronic Annotaton'), ('experiment', 'Experimental'), ('cmap', 'CMAP DB'),
                   ('tas','Tracable Author Statement'), ('itm', 'Inferred by Text Mining'), ('other', 'Other')]
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=3, max=30)])
    email = StringField('Email', [validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
class RepurposeForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    chem_id = StringField('Chemical ID')
    drugbank_id = StringField('Drugbank ID')
    org_indication = StringField('Original Indication', [validators.DataRequired()])
    new_indication = StringField('New Indication', [validators.DataRequired()])
    evidence = SelectField('Evidence', choices=EVIDENCE_CHOICE)
    pubmed_id = StringField('Pubmed ID')
    website =  StringField('Website', [validators.URL])
    additional_info = TextAreaField('Additonal Information')


# if __name__ == "__main__"

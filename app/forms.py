from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, IntegerField, FileField, PasswordField
from wtforms.validators import DataRequired, Email, Optional, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=200)])
    category = SelectField('Category', choices=[
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('renovation', 'Renovation')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    location = StringField('Location', validators=[Optional(), Length(max=200)])
    year = StringField('Year', validators=[Optional(), Length(max=20)])
    image = FileField('Project Image')
    featured = BooleanField('Featured Project')
    order = IntegerField('Display Order', default=0)

class ServiceForm(FlaskForm):
    title = StringField('Service Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    icon_name = SelectField('Icon', choices=[
        ('building', 'Building'),
        ('office', 'Office'),
        ('industry', 'Industry'),
        ('structure', 'Structure'),
        ('renovation', 'Renovation'),
        ('management', 'Management')
    ])
    order = IntegerField('Display Order', default=0)
    active = BooleanField('Active', default=True)

class TeamForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=200)])
    title = StringField('Job Title', validators=[Optional(), Length(max=200)])
    bio = TextAreaField('Biography', validators=[Optional()])
    image = FileField('Photo')
    credentials = TextAreaField('Credentials (one per line)', validators=[Optional()])
    license_no = StringField('License Number', validators=[Optional(), Length(max=100)])
    experience = StringField('Experience', validators=[Optional(), Length(max=100)])
    registered_in = StringField('Registered In', validators=[Optional(), Length(max=200)])
    is_lead = BooleanField('Lead Engineer')
    order = IntegerField('Display Order', default=0)

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=200)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=200)])
    phone = StringField('Phone', validators=[Optional(), Length(max=50)])
    project_type = SelectField('Project Type', choices=[
        ('', 'Select Project Type'),
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
        ('Industrial', 'Industrial'),
        ('Renovation', 'Renovation'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    details = TextAreaField('Project Details', validators=[Optional()])

class BlogForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), Length(max=200)])
    slug = StringField('URL Slug', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    excerpt = TextAreaField('Excerpt', validators=[Optional()])
    image = FileField('Featured Image')
    author = StringField('Author', validators=[Optional(), Length(max=100)])
    published = BooleanField('Published')

class SiteSettingForm(FlaskForm):
    site_name = StringField('Site Name', validators=[Optional(), Length(max=200)])
    site_email = StringField('Contact Email', validators=[Optional(), Email(), Length(max=200)])
    site_phone = StringField('Phone', validators=[Optional(), Length(max=50)])
    site_address = StringField('Address', validators=[Optional(), Length(max=500)])
    site_hours = StringField('Business Hours', validators=[Optional(), Length(max=200)])

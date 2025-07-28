# wcp_tracker/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from models import Department  # CORRECTED: Changed from relative to absolute import
from datetime import datetime

# This helper function is used by the QuerySelectField to get a list of departments
def get_departments():
    return Department.query.all()

class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired()])
    email = StringField('Contact Email', validators=[DataRequired(), Email()])
    head_name = StringField('Head of Department', validators=[DataRequired()]) # CORRECTED: Typo fixed
    submit = SubmitField('Save Department')

class IndicatorForm(FlaskForm):
    department = QuerySelectField(
        'Department',
        query_factory=get_departments,
        get_label='name',
        allow_blank=False,
        validators=[DataRequired()]
    )
    indicator_name = StringField('Indicator Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    target_value = FloatField('Quarterly Target Value', validators=[DataRequired()])
    unit = StringField('Unit of Measurement', validators=[DataRequired()])
    submit = SubmitField('Save Indicator')

class SubmissionForm(FlaskForm):
    quarter = SelectField(
        'Quarter',
        choices=[(1, 'Q1'), (2, 'Q2'), (3, 'Q3'), (4, 'Q4')],
        coerce=int,
        validators=[DataRequired()]
    )
    year = IntegerField(
        'Year',
        validators=[DataRequired(), NumberRange(min=2020, max=2050)],
        default=datetime.now().year
    )
    actual_value = FloatField('Actual Value Achieved', validators=[DataRequired()])
    submitted_by = StringField('Your Name', validators=[DataRequired()])
    submit = SubmitField('Submit Performance Data')
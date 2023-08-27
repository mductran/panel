from wtforms import FileField, SubmitField, URLField
from flask_wtf import FlaskForm


class SearchForm(FlaskForm):
    picture = FileField("Upload your image")
    url = URLField("Enter image url")

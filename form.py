from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class Upload(FlaskForm):
    day = IntegerField("Day", validators=[DataRequired()])
    file = FileField(
        "imageFile",
        validators=[
            FileRequired(),
            FileAllowed(["png", "jpg"], "Image file only"),  # Image formats
        ],
    )
    submit = SubmitField("Upload")

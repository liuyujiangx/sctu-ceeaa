from wtforms import SelectField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

from app.models import T_classes

t_classes = T_classes.query.all()

class ClassesForm(FlaskForm):
    classes = SelectField(
        label="班级",
        validators=[
            DataRequired("请选择班级")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in t_classes],
        description="班级",
        render_kw={
            "class": "form-control",

        }
    )
    submit = SubmitField(
        '查找',
        render_kw={
            "class": "btn btn-primary",

        }

    )
from wtforms import SelectField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

from app import db
from app.models import T_classes, T_cmodules

t_classes = T_classes.query.all()
t_cmodules = db.session.execute('SELECT id,name FROM t_cmodules GROUP BY name')
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
class CmodulesForm(FlaskForm):
    cmodules = SelectField(
        label="模块",
        validators=[
            DataRequired("请选择模块")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in t_cmodules],
        description="模块",
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
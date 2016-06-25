# coding=utf-8
from flask.ext.wtf import Form
from wtforms import RadioField, SubmitField
from wtforms.validators import Required


class ChoiceForm(Form):
    choose = RadioField('choice', coerce=str, choices=[], validators=[Required("Please, choose some word")])
    submit = SubmitField('Выбрать'.decode('utf-8'))
    #
    # def __init__(self):
    #     Form.__init__(self)
    #     self.collection_name, self.theme_name, self.choices, self.extra_word = getData0()
    #     self.choose.choices = self.choices.items()


class AnswerForm(Form):
    submit = SubmitField('Да'.decode('utf-8'))
    reject = SubmitField('Нет'.decode('utf-8'))

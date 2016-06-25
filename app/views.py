# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for
import random
from os import listdir
import os, sys
from app import app
from forms import ChoiceForm, AnswerForm

app.SECRET_KEY = 'you-will-never-guess'


def getData0():
    folder = "app/data/"
    files = listdir(folder)

    choose_file = random.randint(0, len(files) - 1)

    file = files[choose_file]
    print(choose_file)

    lines = open(folder + file, 'r').readlines()
    collection_name = lines[0].strip()
    choose_theme = random.randint(1, len(lines) - 1)
    print(choose_theme)
    theme = lines[choose_theme]

    elements = theme.strip().split(": ")
    theme_name = elements[0].strip()
    words = set(elements[1].split())

    choose_another_theme = choose_theme
    while choose_another_theme == choose_theme:
        choose_another_theme = random.randint(1, len(lines) - 1)
    extra_word = lines[choose_another_theme].strip().split(": ")[1].split()[0]
    words.add(extra_word)
    print(extra_word)

    choices = {}
    counter = 0
    for word in words:
        choices['word' + str(counter)] = word.decode('utf-8')
        counter += 1
    print(theme_name)
    print(col_name)
    extra_word = extra_word.decode('utf-8')

    return collection_name, theme_name, choices, extra_word


def getData1():
    folder = "app/data/"
    files = listdir(folder)

    choose_file = random.randint(0, len(files) - 1)
    print(choose_file)
    file = files[choose_file]

    lines = open(folder + file, 'r').readlines()
    collection_name = lines[0].strip()
    choose_theme = random.randint(1, len(lines) - 1)
    print(choose_theme)
    theme = lines[choose_theme]

    elements = theme.strip().split(": ")
    theme_name = elements[0].strip()
    words = set(elements[1].split())

    choices = {}
    counter = 0
    for word in words:
        choices['word' + str(counter)] = word.decode('utf-8')
        counter += 1
    print(theme_name)
    print(col_name)
    return collection_name, theme_name, choices


def putData(col_name, doc_name, question, answer):
    results = open('results.txt', 'a')

    results.write(col_name + " " + doc_name + " " + str(question) + " " + str(answer) + "\n")


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    message = 'Добро пожаловать в исследование!'
    return redirect(url_for('.extra_word', message=message))


col_name = ""
theme_name = ""
data = {}
extra_word = ""


@app.route('/extra_word', methods=['GET', 'POST'])
def extra_word():
    global data, extra_word, col_name, theme_name

    if request.method == 'GET':
        col_name, theme_name, data, extra_word = getData0()

    form = ChoiceForm()
    form.choose.choices = data.items()

    if form.validate_on_submit():
        if data[form.choose.data] == extra_word:
            answer = 1
            message = 'Вы правильно определили лишнее слово.'
        else:
            answer = 0
            message = 'Вы ошиблись в выборе лишнего слова. Лишнее слово - ' + extra_word.encode('utf-8')
        putData(col_name, theme_name, 0, answer)
        return redirect(url_for('.interpreted', message=message))

    message = request.args['message']
    return render_template('extra_word.html', title='Research', form=form, message=message)


@app.route('/interpreted', methods=['GET', 'POST'])
def interpreted():
    global col_name, theme_name, data

    if request.method == 'GET':
        col_name, theme_name, data = getData1()

    form = AnswerForm()

    if form.validate_on_submit():
        if form.submit.data:
            answer = 1
        else:
            answer = 0
        putData(col_name, theme_name, 1, answer)
        message = 'Спасибо за помощь в исследовании :)'
        return redirect(url_for('.extra_word', message=message))

    message = request.args['message']
    return render_template('interpreted.html', title='Research', form=form, data=data, message=message)


@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html', title='Research')

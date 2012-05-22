#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, request, render_template, flash, url_for, \
    redirect
from flaskext import wtf
from flaskext.wtf import validators

from forms import NotesForm

app = Flask(__name__)
app.config.from_pyfile('settings.py')
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


class Notes(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    subject = db.Column(db.String(80))
    author = db.Column(db.String(80))
    description = db.Column(db.Text)
    pub_date = db.Column(db.Date)

    def __init__(
        self,
        title,
        author,
        description,
        subject,
        ):
        self.title = title
        self.author = author
        self.description = description
        self.subject = subject
        self.pub_date = datetime.now()


@app.route('/')
def redirect_to_home():
    return redirect(url_for('list_notes'))


@app.route('/notes/')
def list_notes():
    notes = Notes.query.all()
    return render_template('index.html', notes=notes)


@app.route('/notes/create/', methods=['GET', 'POST'])
def create():
    form = NotesForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            note = Notes(form.title.data, form.author.data,
                         form.description.data, form.subject.data)
            db.session.add(note)
            db.session.commit()
            flash('Note saved on database.')
            return redirect(url_for('list_notes'))
    return render_template('note.html', form=form)


@app.route('/notes/delete/<int:note_id>', methods=['GET'])
def delete(note_id):
    note = Notes.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('Note Deleted')
    return redirect(url_for('list_notes'))


@app.route('/notes/edit/<int:note_id>', methods=['GET', 'POST'])
def edit(note_id):
    note = Notes.query.get_or_404(note_id)
    form = NotesForm(obj=note)
    if request.method == 'POST':
        print request.form
        if form.validate_on_submit():
            print request.form['title']
            note.title = request.form['title']
            note.author = request.form['author']
            note.description = request.form['description']
            note.subject = request.form['subject']
            db.session.add(note)
            db.session.commit()
        return redirect(url_for('list_notes'))
    else:
        return render_template('note.html', form=form)

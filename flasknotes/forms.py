#!/usr/bin/python
# -*- coding: utf-8 -*-
from flaskext import wtf
from flaskext.wtf import validators


class NotesForm(wtf.Form):

    subject_list = [('0', 'English'), ('1', 'Philosophy'), ('2',
                    'Theology'), ('3', 'Mathematics')]

    title = wtf.StringField('Title', validators=[validators.Required()])
    author = wtf.StringField('Author',
                             validators=[validators.Required()])
    description = wtf.TextAreaField('Description',
                                    validators=[validators.Required()])
    subject = wtf.SelectField(choices=subject_list)

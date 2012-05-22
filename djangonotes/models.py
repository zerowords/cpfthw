#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

# Create your models here.

SUBJECT_CHOICES = (('English', 'English'), ('Mathematics', 'Mathematics'
                   ), ('History', 'History'), ('Philosophy',
                   'Philosophy'))


class Note(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    author = models.CharField(max_length=20)
    date_created = models.DateField(auto_now=True, auto_now_add=True)


class NoteForm(ModelForm):

    class Meta:

        model = Note



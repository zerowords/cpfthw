#!/usr/bin/python
# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render, redirect

from models import Note, NoteForm


def index(request):
    notes = Note.objects.all()
    return render(request, 'index.html', {'notes': notes})


def create(request):
    form = NoteForm(data=request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'form.html', {'form': form})


def edit(request, note_id):
    instance_data = Note.objects.get(id=note_id)
    form = NoteForm(data=request.POST or None, instance=instance_data)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'form.html', {'form': form})

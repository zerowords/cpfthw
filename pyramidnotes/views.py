#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from docutils.core import publish_parts
from formencode import Schema, validators

from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from models import DBSession, Note


class NoteSchema(Schema):

    filter_extra_fields = True
    allow_extra_fields = True

    title = validators.String(not_empty=True)
    author = validators.String(not_empty=True)
    subject = validators.String(not_empty=True)
    description = validators.PlainText(not_empty=True)


@view_config(name='edit', renderer='templates/edit.pt')
def edit(request):

    item_id = request.matchdict['item_id']
    item = session.query(Note).get(item_id)

    form = Form(request, schema=NoteSchema, obj=item)

    if form.validate():

        form.bind(item)

        # persist model somewhere...

        return HTTPFound(location='/')

    return dict(item=item, form=FormRenderer(form))


@view_config(name='add', renderer='templates/submit.pt')
def add(request):
    import ipdb
    ipdb.set_trace()
    form = Form(request, schema=NoteSchema)

    if form.validate():

        obj = form.bind(Note())

        # persist model somewhere...

        return HTTPFound(location='/')

    return dict(renderer=FormRenderer(form))


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(Note).filter(Note.note_id == 1).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain',
                        status_int=500)
    return {'one': one, 'project': 'PyramidNotes'}

conn_err_msg = \
    """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_PyramidNotes_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

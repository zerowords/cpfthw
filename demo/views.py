import jinja2
import os
import webapp2
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template

from models import Notes, Notebooks, Trans
import logging

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))


class MainPageNote(BaseHandler):

    def get(self, notebook_id):
        notebook = db.get(db.Key.from_path('Notebooks', notebook_id))
	note = db.Query(Notes)
	note.ancestor( notebook)
	notes = note.fetch(limit=100)
	if not notes:
	    return webapp2.redirect("/create/%s" % notebook_id)
	else:
	    self.render_template('read.html', {'notes': notes, 'notebook_id': notebook_id})


class CreateNote(BaseHandler):

    def post(self, notebook_id):
        notebook = db.get(db.Key.from_path('Notebooks', notebook_id))
	n = Notes(parent=notebook, author=self.request.get('author'),
                  text=self.request.get('text'),
                  priority=self.request.get('priority'),
                  status=self.request.get('status'))
        n.put()
	return webapp2.redirect("/read/%s" % notebook_id)

    def get(self, notebook_id):
        self.render_template('create.html', {})


class EditNote(BaseHandler):

    def post(self, notebook_id, note_id):
        iden = int(note_id)
        note = db.get(db.Key.from_path('Notebooks',notebook_id,'Notes', iden))
        note.author = self.request.get('author')
        note.text = self.request.get('text')
        note.priority = self.request.get('priority')
        note.status = self.request.get('status')
        note.date = datetime.now()
        note.put()
        return webapp2.redirect('/')

    def get(self, notebook_id, note_id):
        iden = int(note_id)
        note = db.get(db.Key.from_path('Notebooks',notebook_id,'Notes', iden))
	self.render_template('edit.html', {'note': note, 'notebook_id': notebook_id})


class DeleteNote(BaseHandler):

    def get(self, notebook_id, note_id):
        iden = int(note_id)
        note = db.get(db.Key.from_path('Notebooks',notebook_id,'Notes', iden))
        db.delete(note)
	return webapp2.redirect("/read/%s" % notebook_id)

class MainPage(BaseHandler):

    def post(self):
	notebook_id = self.request.get('ID', None)
	isUser = self.request.get('isUser', None)
	if not notebook_id:
	    return webapp2.redirect('/')
	else:
	    notebook_key = db.get(db.Key.from_path('Notebooks', notebook_id))
	    if isUser == "True":
		user = users.get_current_user()
		user_ID = user.user_id()
		if notebook_key:
		    if user_ID == notebook_key.user: 
			return webapp2.redirect("/editnotebook/%s" % notebook_id)
		    else:
			reason='That Notebook name is taken already.'
			trans = Trans(key_name='reason')
			trans.reason=reason
			trans.put()
			template_values = {'trans':trans}
			path = os.path.join(TEMPLATE_DIR, 'unexpected.html')
			self.response.out.write(template.render(path, template_values))
		else:
		    return webapp2.redirect("/createnotebook/%s" % notebook_id)


	    else:
		if notebook_key:
		    note = db.Query(Notes)
		    note.ancestor( notebook_key)
		    notes = note.fetch(limit=100)
		    if not notes:
			return webapp2.redirect("/create/%s" % notebook_id)
		    else:
			return webapp2.redirect("/read/%s" % notebook_id)
		else:
		    return webapp2.redirect('/')
	
    def get(self):
        user = users.get_current_user()
        if user: #offer user options 
            user_ID = str(user.user_id())
            notebook = db.Query(Notebooks)
            notebook.filter('user =', user_ID)
            notebook.filter('deleteRequested =', False)
            pages = notebook.fetch(limit=100)
	    t = []
	    for page in pages:
		t += [page.key().name()]
	    pages=t
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Signout'
            if not pages:
		userHasNotebook = False
        	url_linktextmore = ' if you wish. You will be returned to this page after you signout.'
            else:
		userHasNotebook = True
        	url_linktextmore = ' if you wish. If you signout you will be able to use your Notebook as if you were a visitor. You will be returned to this page after you signout.'

            template_values = {
        	'userHasNotebook': userHasNotebook,
        	'pages': pages,
        	'user': user,
        	'url': url,
        	'url_linktext': url_linktext,
        	'url_linktextmore': url_linktextmore,
            }
        else: #not a user
            userHasNotebook  = False
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Signin'
            url_linktextmore = ' if you will be creating a Notebook or if you wish to edit or manage your own Notebook. You will be returned to this page after you signin.'
            template_values = {
        	'userHasNotebook': userHasNotebook,
        	'url': url,
        	'url_linktext': url_linktext,
        	'url_linktextmore': url_linktextmore,
            }
        path = os.path.join(TEMPLATE_DIR, 'index.html')
        self.response.out.write(template.render(path, template_values))


class CreateNotebook(BaseHandler):

    def post(self, notebook_id):
	logging.info("CreateNotebook: %s " % notebook_id)
        n = Notebooks(key_name=notebook_id,
                  user=self.request.get('user_ID'),
                  moreinfo=self.request.get('moreinfo'),
                  deleteRequested=False)
        n.put()
        return webapp2.redirect('/')

    def get(self, notebook_id):
    	user = users.get_current_user()
        user_ID = user.user_id()
	template_values = {'ID':notebook_id,'user_ID': user_ID}
        path = os.path.join(TEMPLATE_DIR, 'createnotebook.html')
        self.response.out.write(template.render(path, template_values))


class EditNotebook(BaseHandler):

    def post(self, notebook_id):
        iden = notebook_id
        notebook = db.get(db.Key.from_path('Notebooks', iden))
        notebook.author = self.request.get('author')
        notebook.text = self.request.get('text')
        notebook.priority = self.request.get('priority')
        notebook.status = self.request.get('status')
        notebook.date = datetime.now()
        notebook.put()
        return webapp2.redirect('/')

    def get(self, notebook_id):
        iden = notebook_id
    	user = users.get_current_user()
        user_ID = user.user_id()
        notebook = db.get(db.Key.from_path('Notebooks', iden))
	template_values = {'ID':notebook_id,'user_ID': user_ID}
        path = os.path.join(TEMPLATE_DIR, 'editnotebook.html')
        self.response.out.write(template.render(path, template_values))


class DeleteNotebook(BaseHandler):

    def get(self, notebook_id):
        iden = notebook_id
        notebook = db.get(db.Key.from_path('Notebooks', iden))
        db.delete(notebook)
        return webapp2.redirect('/')

class Unexpected(BaseHandler):

    def get(self):
	trans=Trans.get_by_key_name('reason')
	template_values = {'trans':trans}
        path = os.path.join(TEMPLATE_DIR, 'unexpected.html')
        self.response.out.write(template.render(path, template_values))

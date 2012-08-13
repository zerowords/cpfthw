from google.appengine.ext import db


class Notes(db.Model):

    author = db.StringProperty()
    text = db.StringProperty(multiline=True)
    priority = db.StringProperty()
    status = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class Notebooks(db.Model):
    user = db.StringProperty()
    moreinfo = db.StringProperty(multiline=True)
    deleteRequested = db.BooleanProperty(default=False)

class Trans(db.Model):
    reason = db.StringProperty()


import webapp2
from views import MainPageNote, CreateNote, DeleteNote, EditNote, \
                    MainPage, CreateNotebook, DeleteNotebook, EditNotebook, Unexpected

app = webapp2.WSGIApplication([
        ('/', MainPage), 
        ('/unexpected', Unexpected), 
        ('/read/([\w]+)', MainPageNote), 
        ('/create/([\w]+)', CreateNote), 
        ('/createnotebook/([\w]+)', CreateNotebook), 
        ('/editnotebook/([\w]+)', EditNotebook),
        ('/deletenotebook/([\w]+)', DeleteNotebook),
        ('/edit/([\w]+)/([\d]+)', EditNote),
        ('/delete/([\w]+)/([\d]+)', DeleteNote)
        ],
        debug=True)

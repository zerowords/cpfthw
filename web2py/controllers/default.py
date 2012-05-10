def index():

    ''' Makes a db query to select all the notes, 
    orders the notes by the publication date and 
    returns a dictionary to the template, containing 
    all the notes.'''

    response.flash = "Welcome to the index view!"
    notes = db(db.notes).select(orderby=db.notes.pub_date)    
    return dict(notes=notes)
     
def create():

    ''' Generates a form corresponding to the model and 
        renders it, if the form sends some data, the function 
        validates the data and saves the data in the database.'''
        
    response.flash = "This is the create page"
    form=SQLFORM(db.notes)
    if form.process().accepted:
       response.flash = 'form accepted'
    elif form.errors:
       response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'       
    return dict(form=form)


def edit():

    ''' The function pre-populates the data from the note instance
        that has been requested to be edited and renders it,
        once client sends in some data, it saves it in the database.'''
        
    note = db.notes(request.args(0)) or redirect(URL('error'))
    form=SQLFORM(db.notes, note, deletable = True)
    if form.validate():
        if form.deleted:
            db(db.notes.id==note.id).delete()
            redirect(URL('index'))
        else:
            note.update_record(**dict(form.vars))
            response.flash = 'records changed'
    else:
        response.flash = 'Something went wrong!'
    return dict(form=form)    
    
    
    # ALL THE FUNCTIONS BELOW ARE AUTO GENERATED
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())




def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

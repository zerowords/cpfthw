from tgnotes.model import DBSession, metadata, Note
from tw.core import WidgetsList
from tw.forms import TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.formbase import EditableForm

class NoteForm(TableForm):
    # This WidgetsList is just a container
    class fields(WidgetsList):
        title = TextField(validator=NotEmpty)
        author = TextField(validator=NotEmpty)
        description = TextArea(attrs=dict(rows=3, cols=25))
        date_taken = CalendarDatePicker(validator=DateConverter())
        subject_list = ((1,"Philosophy"),
                         (2,"Maths"),
                         (3,"Literature"),
                         (4,"History"),
                         (5,"Politics"),
                         (6,"Sociology"))
        subject = SingleSelectField(options=subject_list)
note_add_form = NoteForm("create_note_form")
        
class NoteEditForm(EditableForm):
    __model__ = Note
    __omit_fields__ = ['note_id']
note_edit_form = NoteEditForm(DBSession)




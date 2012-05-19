"""Main Controller"""

from tgnotes.lib.base import BaseController
from tgext.crud import CrudRestController
from tgnotes.model import DBSession, Note
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.fillerbase import EditFormFiller

from tgnotes.widgets.forms import note_add_form, note_edit_form

class NoteTable(TableBase):
    __model__ = Note
    __omit_fields__ = ['note_id']
note_table = NoteTable(DBSession)

class NoteTableFiller(TableFiller):
    __model__ = Note
note_table_filler = NoteTableFiller(DBSession)

class NoteEditFiller(EditFormFiller):
    __model__ = Note
note_edit_filler = NoteEditFiller(DBSession)

class RootController(BaseController):
    notes = NoteController(DBSession)

class NoteController(CrudRestController):
    model = Note
    table = note_table
    table_filler = note_table_filler
    edit_filler = note_edit_filler
    new_form = note_add_form
    edit_form = note_edit_form


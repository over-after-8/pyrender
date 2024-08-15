import json

from flask import request, render_template
from flask_login import login_required

from render.builder.utils import outside_url_for
from render.builder.viewmodel import ViewModel, check_permission


class JobVM(ViewModel):
    list_fields = ["id", "name", "task", "schedule", "start", "end"]
    search_fields = ["id", "name", "task"]
    add_fields = ["name", "task", "schedule", "start", "end"]
    show_fields = ["id", "name", "task", "schedule", "start", "end"]
    edit_fields = ["name", "task", "schedule", "start", "end"]

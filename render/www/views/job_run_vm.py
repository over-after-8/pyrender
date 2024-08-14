import json

from flask import request, render_template
from flask_login import login_required

from render.builder.utils import outside_url_for
from render.builder.viewmodel import ViewModel, check_permission


class JobRunVM(ViewModel):
    list_fields = ["id", "status", "run_timestamp", "job"]
    search_fields = ["id", "run_timestamp", "status"]
    show_fields = ["id", "job", "run_timestamp", "status"]
    disabled_view_models = ["add", "edit"]
    field_types = {
        "status": "JobRunStatus"
    }

    multi_select_actions = {"delete": outside_url_for(".multi_delete_job_run")}

    def register(self, flask_app_or_bp):
        self.bp.route("/job_runs_delete", methods=["POST", "GET"])(self.multi_delete_job_run)
        super().register(flask_app_or_bp)

    @login_required
    @check_permission("delete")
    def multi_delete_job_run(self):
        if request.method == "GET":
            items = [1, 2, 3]
            return render_template("render/multi_delete_view.html",
                                   title="Delete Job Runs", model=json.dumps(items)), 200
        else:
            raise NotImplemented

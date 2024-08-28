import json

from flask import request, render_template, redirect
from flask_login import login_required

from render.builder.utils import outside_url_for
from render.builder.viewmodel import ViewModel
from render.models.job import JobRun
from render.utils.db import create_session


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

    # @check_permission("delete")
    @login_required
    def multi_delete_job_run(self):
        if request.method == "GET":
            items = request.args.getlist("item_id")
            return render_template("render/multi_delete_view.html",
                                   title="Delete Job Runs", model=json.dumps(len(items))), 200
        else:
            items = request.args.getlist("item_id")
            with create_session() as session:
                items_to_delete = session.query(JobRun).filter(JobRun.id.in_(items)).all()
                for item in items_to_delete:
                    session.delete(item)
            return redirect(self.list_view_model.search_url_func()), 302
import logging

from flask import Blueprint, render_template
from flask_login import login_required

group_page = Blueprint("group_page", __name__, template_folder="templates")


@group_page.route("/teacher/group/<int:group_id>", methods=["GET"])
@group_page.route("/student/group/<int:group_id>", methods=["GET"])
@login_required
def group(group_id):
    logging.info(f"Group id = {group_id}")

    return render_template("group.html")

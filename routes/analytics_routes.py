from flask import Blueprint, jsonify
from services.analytics_engine import compute_utilization_stats
from utils.auth_utils import token_required, role_required

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics/utilization", methods=["GET"])
@token_required
@role_required("admin", "faculty")
def get_utilization():
    stats = compute_utilization_stats()
    return jsonify(stats), 200
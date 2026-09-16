from flask import Blueprint, request, jsonify
from models.resource import get_all_resources, create_resource
from services.parallel_search import search_available_resources
from utils.auth_utils import token_required

resource_bp = Blueprint("resources", __name__)


@resource_bp.route("/resources", methods=["GET"])
@token_required
def list_resources():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")

    all_resources = get_all_resources()

    if start_time and end_time:
        available = search_available_resources(all_resources, start_time, end_time)
        return jsonify(available), 200

    return jsonify(all_resources), 200


@resource_bp.route("/resources", methods=["POST"])
@token_required
def add_resource():
    data = request.get_json()

    name = data.get("name")
    type = data.get("type")
    capacity = data.get("capacity")
    department = data.get("department")
    location = data.get("location")

    if not name or not type:
        return jsonify({"error": "name and type are required"}), 400

    new_id = create_resource(name, type, capacity, department, location)
    return jsonify({"message": "Resource created", "id": new_id}), 201
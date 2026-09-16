from flask import Blueprint, request, jsonify
from services.ml_engine import predict_demand_batch
from utils.auth_utils import token_required, role_required
from services.ml_engine import predict_demand, train_demand_model, get_clusters

ml_bp = Blueprint("ml", __name__)


@ml_bp.route("/ml/demand-forecast", methods=["GET"])
@token_required
@role_required("admin", "faculty")
def demand_forecast():
    day_of_week = request.args.get("day_of_week", type=int, default=0)
    hour_of_day = request.args.get("hour_of_day", type=int, default=10)
    resource_type_code = request.args.get("resource_type_code", type=int, default=0)
    department_code = request.args.get("department_code", type=int, default=0)
    past_usage_frequency = request.args.get("past_usage_frequency", type=int, default=10)

    predicted_demand = predict_demand(
        day_of_week, hour_of_day, resource_type_code, department_code, past_usage_frequency
    )

    return jsonify({
        "day_of_week": day_of_week,
        "hour_of_day": hour_of_day,
        "resource_type_code": resource_type_code,
        "department_code": department_code,
        "past_usage_frequency": past_usage_frequency,
        "predicted_demand": predicted_demand
    }), 200


@ml_bp.route("/ml/demand-forecast/retrain", methods=["POST"])
@token_required
@role_required("admin")
def retrain_demand():
    train_demand_model()
    return jsonify({"message": "Demand model retrained"}), 200


@ml_bp.route("/ml/clusters", methods=["GET"])
@token_required
@role_required("admin", "faculty")
def clusters():
    result = get_clusters()

    if result is None:
        return jsonify({"error": "Not enough resource data to form clusters yet"}), 400

    return jsonify(result), 200


@ml_bp.route("/ml/demand-forecast/batch", methods=["POST"])
@token_required
@role_required("admin", "faculty")
def demand_forecast_batch():
    data = request.get_json()
    resource_requests = data.get("resources")

    if not resource_requests or not isinstance(resource_requests, list):
        return jsonify({"error": "resources must be a non-empty list"}), 400

    results = predict_demand_batch(resource_requests)

    return jsonify(results), 200

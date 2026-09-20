from flask import Blueprint, request, jsonify
from models.booking import (
    create_booking,
    get_bookings_for_user,
    get_all_bookings,
    get_booking_by_id,
    update_booking_status
)
from services.scheduling import enqueue_booking_request, dequeue_next_request, get_resource_lock
from services.conflict_detection import has_conflict
from utils.auth_utils import token_required, role_required

booking_bp = Blueprint("bookings", __name__)


@booking_bp.route("/bookings", methods=["POST"])
@token_required
def submit_booking():
    data = request.get_json()

    resource_id = data.get("resource_id")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not resource_id or not start_time or not end_time:
        return jsonify({"error": "resource_id, start_time, and end_time are required"}), 400

    enqueue_booking_request(request.user_id, request.user_role, resource_id, start_time, end_time)
    request_data = dequeue_next_request()

    resource_lock = get_resource_lock(request_data["resource_id"])

    with resource_lock:
        conflict_exists = has_conflict(
            request_data["resource_id"],
            request_data["start_time"],
            request_data["end_time"]
        )

        if conflict_exists:
            return jsonify({"error": "This resource is already booked for the requested time"}), 409

        new_booking_id = create_booking(
            request_data["user_id"],
            request_data["resource_id"],
            request_data["start_time"],
            request_data["end_time"]
        )

    return jsonify({"message": "Booking created", "booking_id": new_booking_id}), 201


@booking_bp.route("/bookings", methods=["GET"])
@token_required
def list_bookings():
    if request.user_role == "admin":
        bookings = get_all_bookings()
    else:
        bookings = get_bookings_for_user(request.user_id)

    return jsonify(bookings), 200


@booking_bp.route("/bookings/<int:booking_id>", methods=["PATCH"])
@token_required
def update_booking(booking_id):
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["approved", "rejected", "cancelled"]:
        return jsonify({"error": "status must be approved, rejected, or cancelled"}), 400

    booking = get_booking_by_id(booking_id)
    if booking is None:
        return jsonify({"error": "Booking not found"}), 404

    if booking["status"] != "pending":
        return jsonify({"error": "This booking has already been " + booking["status"] + " and cannot be changed"}), 400

    is_owner = booking["user_id"] == request.user_id
    is_admin = request.user_role == "admin"

    if new_status == "cancelled":
        if not is_owner and not is_admin:
            return jsonify({"error": "You can only cancel your own bookings"}), 403
    else:
        if not is_admin:
            return jsonify({"error": "Only admin can approve or reject bookings"}), 403

    update_booking_status(booking_id, new_status)

    return jsonify({"message": "Booking updated", "booking_id": booking_id, "status": new_status}), 200
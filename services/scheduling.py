import heapq
import itertools
import threading

_priority_map = {
    "faculty": 1,
    "admin": 1,
    "student": 2
}

_counter = itertools.count()
_queue = []
_queue_lock = threading.Lock()

_resource_locks = {}
_resource_locks_guard = threading.Lock()


def enqueue_booking_request(user_id, role, resource_id, start_time, end_time):
    priority = _priority_map.get(role, 3)
    sequence_number = next(_counter)

    request_data = {
        "user_id": user_id,
        "role": role,
        "resource_id": resource_id,
        "start_time": start_time,
        "end_time": end_time
    }

    with _queue_lock:
        heapq.heappush(_queue, (priority, sequence_number, request_data))


def dequeue_next_request():
    with _queue_lock:
        if len(_queue) == 0:
            return None
        priority, sequence_number, request_data = heapq.heappop(_queue)
        return request_data


def get_resource_lock(resource_id):
    with _resource_locks_guard:
        if resource_id not in _resource_locks:
            _resource_locks[resource_id] = threading.Lock()
        return _resource_locks[resource_id]
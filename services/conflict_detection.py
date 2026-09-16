from concurrent.futures import ThreadPoolExecutor
from models.booking import get_conflicting_bookings


def check_conflicts_parallel(resource_ids, start_time, end_time):
    results = {}

    def check_one(resource_id):
        conflict_count = get_conflicting_bookings(resource_id, start_time, end_time)
        return (resource_id, conflict_count)

    with ThreadPoolExecutor(max_workers=8) as executor:
        outcomes = list(executor.map(check_one, resource_ids))

    for resource_id, conflict_count in outcomes:
        results[resource_id] = conflict_count

    return results


def has_conflict(resource_id, start_time, end_time):
    conflict_map = check_conflicts_parallel([resource_id], start_time, end_time)
    return conflict_map[resource_id] > 0
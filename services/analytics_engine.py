from concurrent.futures import ThreadPoolExecutor
from utils.db import get_connection, release_connection


def _fetch_all_bookings_raw():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT resource_id, start_time, end_time, status FROM bookings WHERE status IN ('approved', 'pending')"
    )
    rows = cursor.fetchall()
    cursor.close()
    release_connection(conn)
    return rows


def _split_into_chunks(data, num_chunks):
    chunk_size = max(1, len(data) // num_chunks)
    chunks = []
    for i in range(0, len(data), chunk_size):
        chunks.append(data[i:i + chunk_size])
    return chunks


def _partial_aggregate(chunk):
    resource_counts = {}
    hour_counts = {}

    for row in chunk:
        resource_id = row[0]
        start_time = row[1]

        if resource_id not in resource_counts:
            resource_counts[resource_id] = 0
        resource_counts[resource_id] += 1

        hour = start_time.hour
        if hour not in hour_counts:
            hour_counts[hour] = 0
        hour_counts[hour] += 1

    return {"resource_counts": resource_counts, "hour_counts": hour_counts}


def _merge_results(partial_results):
    merged_resource_counts = {}
    merged_hour_counts = {}

    for partial in partial_results:
        for resource_id, count in partial["resource_counts"].items():
            if resource_id not in merged_resource_counts:
                merged_resource_counts[resource_id] = 0
            merged_resource_counts[resource_id] += count

        for hour, count in partial["hour_counts"].items():
            if hour not in merged_hour_counts:
                merged_hour_counts[hour] = 0
            merged_hour_counts[hour] += count

    return {"resource_counts": merged_resource_counts, "hour_counts": merged_hour_counts}


def compute_utilization_stats():
    all_bookings = _fetch_all_bookings_raw()

    if len(all_bookings) == 0:
        return {"most_booked_resources": [], "peak_hours": [], "total_bookings": 0}

    num_workers = 4
    chunks = _split_into_chunks(all_bookings, num_workers)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        partial_results = list(executor.map(_partial_aggregate, chunks))

    merged = _merge_results(partial_results)

    most_booked = sorted(merged["resource_counts"].items(), key=lambda x: x[1], reverse=True)
    peak_hours = sorted(merged["hour_counts"].items(), key=lambda x: x[1], reverse=True)

    return {
        "most_booked_resources": [{"resource_id": r[0], "booking_count": r[1]} for r in most_booked],
        "peak_hours": [{"hour": h[0], "booking_count": h[1]} for h in peak_hours],
        "total_bookings": len(all_bookings)
    }
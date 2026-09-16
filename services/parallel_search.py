from concurrent.futures import ThreadPoolExecutor
from models.resource import check_resource_availability


def search_available_resources(resources, start_time, end_time):
    available = []

    def check_one(resource):
        is_available = check_resource_availability(resource["id"], start_time, end_time)
        if is_available:
            return resource
        return None

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(check_one, resources))

    for result in results:
        if result is not None:
            available.append(result)

    return available
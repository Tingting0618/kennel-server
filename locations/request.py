LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville South",
        "address": "1st happy road"
    },
    {
        "id": 2,
        "name": "Nashville North",
        "address": "2nd happy road"
    }
]


def get_all_locations():
    return LOCATIONS


def get_single_location(id):
    requested_location = None
    for location in LOCATIONS:
        location["id"] = id
        requested_location = location
    return requested_location


def create_location(location):
    max_id = LOCATIONS[-1]["id"]
    new_id = max_id + 1
    location["id"] = new_id
    LOCATIONS.append(location)
    return location
def delete_location(id):
    location_index = -1
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            location_index = index
    if location_index >= 0:
        LOCATIONS.pop(location_index)
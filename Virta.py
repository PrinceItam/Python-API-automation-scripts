import requests
import json


BASE_URL = "https://api-energy-k8s.test.virtaglobal.com/v1/tests/"
station_ids = [1, 2, 3, 4, 5]


def make_api_request(method: str, station_id: int, command: str, payload=None) -> any:
    """
    Makes an API request to the specified station with the given method and payload.

    Args:
        method: The HTTP method to use (e.g., "GET", "POST").
        station_id: The ID of the station to interact with.
        command: The API command to execute.
        payload: The data to send with the request (optional).

    Returns:
        The parsed JSON response from the API, or None if an error occurred.
    """

    url = f"{BASE_URL}{station_id}"
    data = {"command": command, "payload": payload}

    try:
        response = requests.request(method.upper(), url, json=data)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error making API request for station {station_id}: {e}")
        return None


def test_get_version(station_id: int):
    """
    Tests the getVersion command for a station.

    Args:
        station_id: The ID of the station to test.
    """

    response = make_api_request("GET", station_id, "getVersion")
    if response:
        version = float(response.get("version", 0))
        if version <= 1.6:
            print(f"Station {station_id} failed version check (version: {version})")
        else:
            print(f"Station {station_id} version check passed")
    else:
        print(f"Error getting version for station {station_id}")


def test_get_interval(station_id: int):
    """
    Tests the getInterval command for a station.

    Args:
        station_id: The ID of the station to test.
    """

    response = make_api_request("GET", station_id, "getInterval")
    if response:
        interval = float(response.get("interval", 0))
        if not (1 <= interval < 60):
            print(f"Station {station_id} failed interval check (interval: {interval})")
        else:
            print(f"Station {station_id} interval check passed")
    else:
        print(f"Error getting interval for station {station_id}")


def test_set_values(station_id: int):
    """
    Tests the setValues command for a station with different payloads.

    Args:
        station_id: The ID of the station to test.
    """

    for payload in (5, 15):
        response = make_api_request("POST", station_id, "setValues", payload)
        if response:
            status = response.get("status", "")
            expected_status = "OK" if 1 < payload < 10 else "FAILED"
            if status != expected_status:
                print(f"Station {station_id} setValues check failed for {payload} (expected: {expected_status}, got: {status})")
            else:
                print(f"Station {station_id} setValues check passed for {payload}")
        else:
            print(f"Error setting values for station {station_id} with payload {payload}")


if __name__ == "__main__":
    for station_id in station_ids:
        test_get_version(station_id)
        test_get_interval(station_id)
        test_set_values(station_id)
        print("-" * 20)  # Separator for clarity between stations

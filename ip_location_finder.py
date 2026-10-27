# Before use: pip install requests
import sys
import requests


def ip_geolocation(ip=""):
  # If an IP is not entered, it will automatically detect your own IP address.
  url = f"https://ipinfo.io/{ip}/json" if ip else "https://ipinfo.io/json"

  response = requests.get(url)
  if response.status_code == 200:
    geo_data = response.json()
    # .get() The KeyError error is prevented using the method.
    print(f"IP: {geo_data.get('ip', 'N/A')}")
    print(f"City: {geo_data.get('city', 'N/A')}")
    print(f"Region: {geo_data.get('region', 'N/A')}")
    print(f"Country: {geo_data.get('country', 'N/A')}")
    print(f"Org: {geo_data.get('org', 'N/A')}")
  else:
    print(f"Error: {response.status_code}")


# Checking if an IP address has been entered from the terminal
ip = sys.argv[1] if len(sys.argv) > 1 else ""
ip_geolocation(ip)

                   

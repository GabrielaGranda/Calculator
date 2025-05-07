from js import document, drawRoute
from pyodide.ffi import create_proxy
from pyodide.http import pyfetch
import json

geoapify_key = "your_geoapify_key_here"
backend_url = "https://calculatorrates.onrender.com"  # <-- replace with your actual backend URL

async def calculate_estimate(event):
    try:
        loading_city = document.getElementById("loading").value
        delivery_city = document.getElementById("delivery").value
        origin = document.getElementById("origin").value
        destination = document.getElementById("destination").value

        # Get coordinates
        url_geo = f"https://api.geoapify.com/v1/geocode/search?format=json&apiKey={geoapify_key}&text="
        res_load = await pyfetch(url_geo + loading_city)
        data_load = await res_load.json()
        lat_load = data_load['results'][0]['lat']
        lon_load = data_load['results'][0]['lon']

        res_del = await pyfetch(url_geo + delivery_city)
        data_del = await res_del.json()
        lat_del = data_del['results'][0]['lat']
        lon_del = data_del['results'][0]['lon']

        # Calculate distance
        dist_url = f"https://api.geoapify.com/v1/routing?mode=drive&units=imperial&apiKey={geoapify_key}&waypoints={lat_load},{lon_load}|{lat_del},{lon_del}"
        res_dist = await pyfetch(dist_url)
        data_dist = await res_dist.json()
        miles = round(float(data_dist['features'][0]['properties']['distance']), 2)

        # Call your backend API with miles, origin, destination
        res = await pyfetch(
            url=backend_url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps({
                "miles": miles,
                "origin": origin,
                "destination": destination
            })
        )
        data = await res.json()

        document.getElementById("rate").innerText = str(data["estimate"])
        document.getElementById("currency").innerText = data["currency"]
        document.getElementById("miles").innerText = str(data["miles"])
        document.getElementById("ppm").innerText = str(data["ppm"])

        # Draw map route
        drawRoute(lat_load, lon_load, lat_del, lon_del, loading_city, delivery_city, geoapify_key)

    except Exception as e:
        print(f"❌ Error: {e}")

# Bind button
calculate_button = document.getElementById("calculate")
calculate_button.addEventListener("click", create_proxy(calculate_estimate))




import requests

def get_suggested_params(city):
    """
    Consulta Open-Meteo y devuelve p y f sugeridos según el enunciado.
    """
    # Geocodificación para obtener latitud y longitud
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&format=json"
    geo_res = requests.get(geo_url).json()
    
    if not geo_res.get('results'):
        return None

    location = geo_res['results'][0]
    lat, lon = location['latitude'], location['longitude']

    # Consultar clima actual
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    data = requests.get(weather_url).json()['current']

    temp = data['temperature_2m']
    humidity = data['relative_humidity_2m']
    wind = data['wind_speed_10m']

    # Lógica de parámetros p y f según el enunciado
    p, f = 0.05, 0.001 

    if wind > 30: p -= 0.02          # Viento > 30 km/h reduce p
    if humidity > 70:                # Humedad > 70%
        p += 0.03                    # aumenta p
        f += 0.002                   # aumenta f
    if temp > 35: f += 0.005         # Temp > 35°C aumenta f

    return {"p": max(0.01, p), "f": max(0.0001, f), "city": city, "temp": temp}
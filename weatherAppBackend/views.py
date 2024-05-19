import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.http import Http404, HttpResponse

import jsonschema
from jsonschema import validate

import os
from . import settings

schema = {
    "type": "object",
    "properties": {
        "latitude": {"type": "number", "minimum": -90, "maximum": 90},
        "longitude": {"type": "number", "minimum": -180, "maximum": 180}
    },
    "required": ["latitude", "longitude"]
}


def get_weather_data(request, latitude, longitude):
    lat_long = {"latitude": latitude, "longitude": longitude}
    try:
        validate(instance=lat_long, schema=schema)
    
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&daily=weather_code,apparent_temperature_max,apparent_temperature_min,sunshine_duration&timezone=auto").json()

        response_daily = response['daily']

        generatedEnergy = []

        installationPower = 2.5
        effectivness = 0.2

        for day in response_daily['sunshine_duration']:
            generatedEnergy.append(round(day / 3600 * installationPower * effectivness, 2))

        json_data = {}

        json_data['date'] = response_daily['time']
        json_data['weather_code'] = response_daily['weather_code']
        json_data['min_temp'] = response_daily['apparent_temperature_min']
        json_data['max_temp'] = response_daily['apparent_temperature_max']
        json_data['gen_energy'] = generatedEnergy

        return JsonResponse(json_data)

    except jsonschema.exceptions.ValidationError as e:
        
        json_data ={}
        json_data['error'] = str(e)
        
        return JsonResponse(json_data)
        


from django.shortcuts import render,redirect
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=bbe6ac641aa150d624288e8c8a67e705'
    
    has_message = False
    class_message = 'success'
    message = 'City successfully added'
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            newcity = form.cleaned_data['name']
            existing_count = City.objects.filter(name = newcity).count()
            has_message = True
            if existing_count == 0:
                r = requests.get(url.format(newcity)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    class_message = 'danger'
                    message = 'City does not exist'
            else:
                class_message = 'danger'
                message = 'City is already added'

    
    form = CityForm()
    
    
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city_name' : city.name,
            'city_temperature' : r['main']['temp'],
            'city_description' : r['weather'][0]['description'],
            'city_icon': r['weather'][0]['icon']
        }
        weather_data.append(city_weather)
    context = {
        'weather_data' : weather_data,
        'form' : form,
        'has_message' : has_message,
        'class_message' : class_message,
        'message' : message,
    }
    return render(request, 'weather/weather.html', context)


def delete(request, city_name):
    City.objects.get(name = city_name).delete()
    return redirect('home')
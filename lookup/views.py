from django.shortcuts import render

# Create your views here.

def home(request):
    import json
    import requests

    aqi_data = [
        {'Number':1,'AQI':'Good','Color':'Green','low_value':0,'high_value':50,'Description':'Air quality is satisfactory, and air pollution poses little or no risk.'},
        {'Number':2,'AQI':'Moderate','Color':'Yellow','low_value':51,'high_value':100,'Description':'Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.'},
        {'Number':3,'AQI':'Unhealthy for Sensitive Groups','Color':'Orange','low_value':101,'high_value':150,'Description':'Members of sensitive groups may experience health effects. The general public is less likely to be affected.'},
        {'Number':4,'AQI':'Unhealthy','Color':'Red','low_value':151,'high_value':200,'Description':'Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.'},
        {'Number':5,'AQI':'Very Unhealthy','Color':'Purple','low_value':201,'high_value':300,'Description':'Health alert: The risk of health effects is increased for everyone.'},
        {'Number':6,'AQI':'Hazardous','Color':'Maroon','low_value':301,'high_value':999,'Description':'Health warning of emergency conditions: everyone is more likely to be affected.'}
    ]

    if request.method == "POST":
        zipcode = request.POST['zipcode']
        print(zipcode)
        # Url passed  to requests.get() is From: https://docs.airnowapi.org/CurrentObservationsByZip/query
        api_request = requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=" + str(zipcode) + "&distance=5&API_KEY=D7F3F572-4152-4A31-9AA4-24206F905430")
        try:
            #json parses the request data into the api variable
            api = json.loads(api_request.content)
        except:
            api = "ERROR"

        for item in aqi_data:
            if api[0]['Category']['Number'] == item['Number']:
                category_description = item['Description']
                if item['AQI'] != "Unhealthy for Sensitive Groups":
                    category_color = strip_and_lower(item['AQI'])
                else:
                    category_color = 'usg'
                break
            else:
                category_color = "bg-warning"
                category_description = "ERROR"


        return render(request, 'home.html', {
        'api':api,
        'category_color':category_color,
        'category_description':category_description,
        'aqi_data':aqi_data
        })
    else:
        api = "UNSET"
        category_color = "bg-info"
        category_description = "UNSET"
        return render(request, 'home.html', {
        'api':api,
        'category_color':category_color,
        'category_description':category_description,
        'aqi_data':aqi_data
        })

def about(request):
    return render(request, 'about.html', {})



#-----UTILITIES-----
def strip_and_lower(humble):
    humble = str(humble)
    stripped = humble.replace(" ", "")
    lowered = stripped.lower()
    print(humble + " --> " + lowered)
    return lowered

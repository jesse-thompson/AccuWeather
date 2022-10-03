import requests
import configparser


# exception for when a location is unable to be retrieved from the API
class NoSuchLocation(Exception):
    pass


# exception for when a response from the API is unable to be parsed
class BadResponse(Exception):
    pass


def get_apikey():
    config = configparser.ConfigParser()
    config.read('app.config')
    apikey_from_file = config['secrets']['apikey']
    return apikey_from_file


# takes zipcode and returns location key to be used in other requests
# location key is used by API to fetch weather information for the given zipcode
def get_location():
    location = input("Please input a zip code: ")

    # puts zipcode into request to "Postal Code Search" API
    location_url = 'http://dataservice.accuweather.com/locations/v1/postalcodes/' \
                   'search?apikey={}={}'.format(get_apikey(), location)

    # sets response as variable to be used for extracting data
    response = requests.get(location_url)

    try:
        # sets key to the location key, extracted from response under 'Key'
        key = response.json()[0].get('Key')
    except IndexError:
        raise NoSuchLocation()
    except TypeError:
        raise BadResponse()
    return key


# gets the current temperature and conditions for the given zip code
def get_condition(key):
    # takes key and sends request via "Current Conditions" API
    conditions_url = 'http://dataservice.accuweather.com/currentconditions/v1/' \
                     '{}?apikey={}'.format(key, get_apikey())

    # takes response and formats into json object
    response = requests.get(conditions_url)
    json_condition = response.json()

    # prints the current temp and conditions
    try:
        print("Current Temperature: {}\n"
              "Current Conditions: {}".format(json_condition[0]['Temperature']['Imperial']['Value'],
                                              json_condition[0].get('WeatherText')))

    except IndexError:
        raise BadResponse()
    except TypeError:
        raise BadResponse()


# gets the 5-day forecast for the given zip code
def get_forecast(key):
    # takes key and sends request via "5 days of Daily Forecasts" API
    forecast_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + key + \
                   '?apikey={}'.format(get_apikey())

    # takes response and formats into json object
    response = requests.get(forecast_url)
    json_forecast = response.json()

    # prints 5-day forecast for min/max temp in imperial values
    # includes today, tomorrow, and then grabs dates for following 3 days
    try:
        print("5-Day Forecast\n"
              "Today's Low: {}\n"
              "Today's High: {}\n"
              "Tomorrow's Low: {}\n"
              "Tomorrow's High: {}\n"
              "{}'s Low: {}\n"
              "{}'s High: {}\n"
              "{}'s Low: {}\n"
              "{}'s High: {}\n"
              "{}'s Low: {}\n"
              "{}'s High: {}\n".format(json_forecast['DailyForecasts'][0]['Temperature']['Minimum']['Value'],
                                       json_forecast['DailyForecasts'][0]['Temperature']['Maximum']['Value'],
                                       json_forecast['DailyForecasts'][1]['Temperature']['Minimum']['Value'],
                                       json_forecast['DailyForecasts'][1]['Temperature']['Maximum']['Value'],
                                       json_forecast['DailyForecasts'][2]['Date'][5:10],
                                       json_forecast['DailyForecasts'][2]['Temperature']['Minimum']['Value'],
                                       json_forecast['DailyForecasts'][2]['Date'][5:10],
                                       json_forecast['DailyForecasts'][2]['Temperature']['Maximum']['Value'],
                                       json_forecast['DailyForecasts'][3]['Date'][5:10],
                                       json_forecast['DailyForecasts'][3]['Temperature']['Minimum']['Value'],
                                       json_forecast['DailyForecasts'][3]['Date'][5:10],
                                       json_forecast['DailyForecasts'][3]['Temperature']['Maximum']['Value'],
                                       json_forecast['DailyForecasts'][4]['Date'][5:10],
                                       json_forecast['DailyForecasts'][4]['Temperature']['Minimum']['Value'],
                                       json_forecast['DailyForecasts'][4]['Date'][5:10],
                                       json_forecast['DailyForecasts'][4]['Temperature']['Maximum']['Value'],
                                       ))
    except IndexError:
        raise BadResponse()
    except TypeError:
        raise BadResponse()


try:
    # get the apikey from app.config
    apikey = get_apikey()
    # get the location key for a zipcode
    location_key = get_location()
    # pass location key to get current conditions
    get_condition(location_key)
    # pass location key to get 5-day forecast with min/max temp
    get_forecast(location_key)

except NoSuchLocation:
    print("Unable to get the location")
except BadResponse:
    print("Invalid response received. Please try again")

pass

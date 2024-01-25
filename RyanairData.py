import datetime
from ryanair import Ryanair
from ryanair.types import Flight
import pandas as pd

# get_cheapest_flights(self, airport: str, 
#                            date_from: Union[datetime.datetime, datetime.date, str], 
#                            date_to: Union[datetime.datetime, datetime.date, str], 
#                            destination_country: Optional[str] = None, 
#                            custom_params: Optional[dict] = None, 
#                            departure_time_from: Union[str, datetime.time] = '00:00', 
#                            departure_time_to: Union[str, datetime.time] = '23:59', 
#                            max_price: Optional[int] = None, 
#                            destination_airport: Optional[str] = None)
    
# get_cheapest_return_flights(self, source_airport: str, 
#                                   date_from: Union[datetime.datetime, datetime.date, str], 
#                                   date_to: Union[datetime.datetime, datetime.date, str], 
#                                   return_date_from: Union[datetime.datetime, datetime.date, str], 
#                                   return_date_to: Union[datetime.datetime, datetime.date, str], 
#                                   destination_country: Optional[str] = None, 
#                                   custom_params: Optional[dict] = None, 
#                                   outbound_departure_time_from: Union[str, datetime.time] = '00:00', 
#                                   outbound_departure_time_to: Union[str, datetime.time] = '23:59', 
#                                   inbound_departure_time_from: Union[str, datetime.time] = '00:00', 
#                                   inbound_departure_time_to: Union[str, datetime.time] = '23:59', 
#                                   max_price: Optional[int] = None, 
#                                   destination_airport: Optional[str] = None)

api = Ryanair(currency="EUR")  # Euro currency, so could also be GBP etc. also

home_airports = ['LJU', 'KLU', 'TRS', 'ZAG', 'VCE', 'TSF']
trip1 = [datetime.datetime.strptime('1-7-2024', '%d-%m-%Y').date(), # first flight start outbound date
         datetime.datetime.strptime('5-7-2024', '%d-%m-%Y').date()] # first flight end outbound date
min_num_days = 3
max_num_days = 3
max_p = 50
two_cities = True

def flights_from_airports(airports, first_date, last_date, max_p):
    df_flights = pd.DataFrame(columns=['currency','departureTime','destination','destinationFull',
                                 'flightNumber','origin','originFull','price'])
    for i in range(len(airports)): # obtaining first flight flights
        flights = api.get_cheapest_flights(airports[i], first_date, last_date, max_price = max_p)
        #list_flights.append(flights)
        for flight in flights:
            row = {'currency' : flight.currency,'departureTime' : flight.departureTime,
                   'destination' : flight.destination,'destinationFull' : flight.destinationFull,
                   'flightNumber' : flight.flightNumber,'origin' : flight.origin,
                   'originFull' : flight.originFull,'price' : flight.price}
            df_flights = pd.concat([df_flights, pd.DataFrame([row])], ignore_index=True)
    return df_flights
      
def calculate_trips(home_airports, trip1, max_p):
    first_flight = flights_from_airports(home_airports, trip1[0], trip1[1], max_p).reset_index()
    second_flight = pd.DataFrame(columns=['currency','departureTime','destination','destinationFull',
                                              'flightNumber','origin','originFull','price'])
    for index, row in first_flight.iterrows():
        airport = row.destination
        first_date = row.departureTime.date() + datetime.timedelta(days = min_num_days)
        last_date = row.departureTime.date() + datetime.timedelta(days = max_num_days)
        #print(airport, first_date, last_date)
        d = flights_from_airports([airport], first_date, last_date, max_p)
        d['first_flight'] = index
        second_flight = pd.concat([second_flight, d], ignore_index=True)

    one_city_trip = second_flight[second_flight['destination'].isin(home_airports)]
    one_city_trip = one_city_trip.merge(first_flight, how='left',left_on=['first_flight'],right_on=['index']) 
    one_city_trip.columns = ['currency_2', 'departureTime_2', 'destination_2', 'destinationFull_2',
                        'flightNumber_2', 'origin_2', 'originFull_2', 'price_2', 'first_flight_2',
                        'index_1', 'currency_1', 'departureTime_1', 'destination_1',
                        'destinationFull_1', 'flightNumber_1', 'origin_1', 'originFull_1', 'price_1']
    
    if two_cities:
        second_flight_2 = second_flight[~second_flight['destination'].isin(home_airports)].reset_index(drop=True).reset_index()
        third_flight = pd.DataFrame(columns=['currency','departureTime','destination','destinationFull',
                                             'flightNumber','origin','originFull','price'])

        for index, row in second_flight_2.iterrows():
            airport = row.destination
            first_date = row.departureTime.date() + datetime.timedelta(days = min_num_days)
            last_date = row.departureTime.date() + datetime.timedelta(days = max_num_days)
            #print(airport, first_date, last_date)
            d = flights_from_airports([airport], first_date, last_date, max_p)
            d['second_flight'] = index
            third_flight = pd.concat([third_flight, d], ignore_index=True)

        two_city_trip = third_flight[third_flight['destination'].isin(home_airports)]
        two_city_trip = two_city_trip.merge(second_flight_2, how='left',left_on=['second_flight'],right_on=['index'])
        two_city_trip = two_city_trip.merge(first_flight, how='left',left_on=['first_flight'],right_on=['index'])
        two_city_trip.columns = ['currency_3', 'departureTime_3', 'destination_3', 'destinationFull_3',
                                 'flightNumber_3', 'origin_3', 'originFull_3', 'price_3',
                                 'second_flight_3', 'index_2', 'currency_2', 'departureTime_2',
                                 'destination_2', 'destinationFull_2', 'flightNumber_2', 'origin_2',
                                 'originFull_2', 'price_2', 'first_flight_2', 'index_1', 'currency_1',
                                 'departureTime_1', 'destination_1', 'destinationFull_1', 'flightNumber_1',
                                 'origin_1', 'originFull_1', 'price_1']
        return one_city_trip, two_city_trip
    else:
        return one_city_trip

time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M")


if two_cities:
    one_city, two_city = calculate_trips(home_airports, trip1, max_p)
    one_city['Price of flights'] = one_city['price_1'] + one_city['price_2']
    two_city['Price of flights'] = two_city['price_1'] + two_city['price_2'] + two_city['price_3']
    overview_one_city = one_city[['originFull_1', 'departureTime_1', 'destinationFull_1', 'departureTime_2', 'destinationFull_2', 'Price of flights']].sort_values(by = ['Price of flights'], ascending = [True])
    overview_one_city.columns = ['Starting location', 'departureTime_1', 'Visited city', 'departureTime_2', 'Ending location', 'Price of flights']
    overview_two_city = two_city[['originFull_1', 'departureTime_1', 'destinationFull_1', 'departureTime_2', 'destinationFull_2', 'departureTime_3', 'destinationFull_3', 'Price of flights']].sort_values(by = ['Price of flights'], ascending = [True])
    overview_two_city.columns = ['Starting location', 'departureTime_1', 'Visited city 1', 'departureTime_2', 'Visited city 2', 'departureTime_3', 'Ending location', 'Price of flights']
    overview_one_city.to_excel(f"one_city_trip {time}.xlsx")
    overview_two_city.to_excel(f"two_city_trip {time}.xlsx") 
else:
    one_city = calculate_trips(home_airports, trip1, max_p)
    one_city['Price of flights'] = one_city['price_1'] + one_city['price_2']
    overview_one_city = one_city[['originFull_1', 'departureTime_1', 'destinationFull_1', 'departureTime_2', 'destinationFull_2', 'Price of flights']].sort_values(by = ['Price of flights'], ascending = [True])
    overview_one_city.columns = ['Starting location', 'departureTime_1', 'Visited city', 'departureTime_2', 'Ending location', 'Price of flights']
    overview_one_city.to_excel("one_city_trip {time}.xlsx")
        

        
        
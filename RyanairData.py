from datetime import datetime, timedelta
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

home_airport = ['LJU', 'KLU', 'TRS', 'RJK', 'GRZ', 'ZAG', 'PUY', 'VCE', 'TSF']

trip1 = [datetime.strptime('25-1-2024', '%d-%m-%Y').date(), # first flight start outbound date
         datetime.strptime('26-1-2024', '%d-%m-%Y').date(), # first flight end outbound date
         datetime.strptime('10-2-2024', '%d-%m-%Y').date(), # second flight start outbound date
         datetime.strptime('15-2-2024', '%d-%m-%Y').date()] # second flight end outbound date

min_num_days = 4
max_num_days = 5

# first = pd.DataFrame(columns=['currency1','departureTime1','destination1','destinationFull1',
#                              'flightNumber1','origin1','originFull1','price1'])
# first_flight_flights = []

# second = pd.DataFrame(columns=['currency2','departureTime2','destination2','destinationFull2',
#                              'flightNumber2','origin2','originFull2','price2'])
# second_flight_flights = []

# third = pd.DataFrame(columns=['currency3','departureTime3','destination3','destinationFull3',
#                              'flightNumber3','origin3','originFull3','price3'])
# third_flight_flights = []


# for i in range(len(home_airport)): # obtaining first flight flights
#     first_flight_dep_airport = api.get_cheapest_flights(home_airport[i], trip1[0], trip1[1])
#     first_flight_flights.append(first_flight_dep_airport)
#     for flight in first_flight_dep_airport:
#         row = {'currency' : flight.currency,'departureTime' : flight.departureTime,
#                'destination1' : flight.destination,'destinationFull1' : flight.destinationFull,
#                'flightNumber' : flight.flightNumber,'origin1' : flight.origin,
#                'originFull1' : flight.originFull,'price' : flight.price}
#         first = pd.concat([first, pd.DataFrame([row])], ignore_index=True)
        
        
def flights_from_airports(airports, first_date, last_date):
    df_flights = pd.DataFrame(columns=['currency','departureTime','destination','destinationFull',
                                 'flightNumber','origin','originFull','price'])
    for i in range(len(airports)): # obtaining first flight flights
        flights = api.get_cheapest_flights(airports[i], first_date, last_date)
        #list_flights.append(flights)
        for flight in flights:
            row = {'currency' : flight.currency,'departureTime' : flight.departureTime,
                   'destination' : flight.destination,'destinationFull' : flight.destinationFull,
                   'flightNumber' : flight.flightNumber,'origin' : flight.origin,
                   'originFull' : flight.originFull,'price' : flight.price}
            df_flights = pd.concat([df_flights, pd.DataFrame([row])], ignore_index=True)
    return df_flights
            
first_flight = flights_from_airports(home_airport, trip1[0], trip1[1])
    

# first_flight_flights = [flight for airport_flights in first_flight_flights for flight in airport_flights]
# destination = list(set([x.destination for x in first_flight_flights]))

# for i in range(len(first_flight_flights)):
#     starting_airport = first_flight_flights[i].originFull
#     ending_airport = first_flight_flights[i].destinationFull
#     price = first_flight_flights[i].price
#     print(f"start: {starting_airport}, end: {ending_airport}, price: {price}")
#     print("")
    
# inbound_flights = []
# for i in range(len(destination)):
#     for j in range(len(home_airport)):
#         inbound_flights.append(api.get_cheapest_flights(destination[i], trip1[2], 
#                                                          trip1[3], destination_airport = home_airport[j]))
# inbound_flights = [flight for airport_flights in inbound_flights for flight in airport_flights]


        
        
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

trip1 = [datetime.strptime('25-1-2024', '%d-%m-%Y').date(), # first outbound date
         datetime.strptime('26-1-2024', '%d-%m-%Y').date(), # last outbound date
         datetime.strptime('10-2-2024', '%d-%m-%Y').date(), # first inbound date
         datetime.strptime('15-2-2024', '%d-%m-%Y').date()] # last inbound date

min_num_days = 4
ma_num_days = 6

outbound_flights = []
data = pd.DataFrame(columns=['currency','departureTime','destination1','destinationFull1',
                             'flightNumber','origin1','originFull1','price'])
for i in range(len(home_airport)): # obtaining outbound flights
    outbound_flights_airport = api.get_cheapest_flights(home_airport[i], trip1[0], trip1[1])
    outbound_flights.append(outbound_flights_airport)
    for flight in outbound_flights_airport:
        row = {'currency' : flight.currency,'departureTime' : flight.departureTime,
               'destination1' : flight.destination,'destinationFull1' : flight.destinationFull,
               'flightNumber' : flight.flightNumber,'origin1' : flight.origin,
               'originFull1' : flight.originFull,'price' : flight.price}
        data = pd.concat([data, pd.DataFrame([row])], ignore_index=True) 
    
    
outbound_flights = [flight for airport_flights in outbound_flights for flight in airport_flights]
destination = list(set([x.destination for x in outbound_flights]))

# for i in range(len(outbound_flights)):
#     starting_airport = outbound_flights[i].originFull
#     ending_airport = outbound_flights[i].destinationFull
#     price = outbound_flights[i].price
#     print(f"start: {starting_airport}, end: {ending_airport}, price: {price}")
#     print("")
    
inbound_flights = []
for i in range(len(destination)):
    for j in range(len(home_airport)):
        inbound_flights.append(api.get_cheapest_flights(destination[i], trip1[2], 
                                                         trip1[3], destination_airport = home_airport[j]))
inbound_flights = [flight for airport_flights in inbound_flights for flight in airport_flights]


        
        
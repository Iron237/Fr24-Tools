import json
import os
with open(f'dxb_arrivals_flights.json', 'r') as f:
    all_flights = json.load(f)
    for flight in all_flights:
        model_code = flight['flight']['aircraft']['model']['code']
        count = 0
        if model_code is None:
            count += 1
            print(model_code)
            print(count)
            

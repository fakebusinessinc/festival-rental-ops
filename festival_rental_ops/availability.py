import pandas as pd
from datetime import date, timedelta

items = ['radio', 'headset']

class ExistingRental:
    
    def __init__(self, item, requested_quantity, start_date, end_date, status):
        self.item = item
        self.requested_quantity = requested_quantity
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        
def check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals):

    # Checks if the item is actually present, which I added to the items list
    if item not in items:
        raise ValueError("Requested item was not found")
    
    # Checks if the requested_quantity is an integer or float
    if isinstance(requested_quantity, int):
        is_whole = True
    elif isinstance(requested_quantity, float):
        if not requested_quantity.is_integer():
            raise ValueError("Requested quantity must be a numeric whole number")
        else:
            requested_quantity = int(requested_quantity)
            is_whole = True
    else:
        raise ValueError("Requested quantity must be a numeric whole number")
    
    # Checks if the requested_quantity is a whole # greater than 0
    if not (is_whole and requested_quantity > 0):
        raise ValueError("Requested quantity must be a positive whole number")
    
    # Checks if the start date is the same or before the end date
    if start_date > end_date:
        raise ValueError("Start date cannot be after the end date")
    
    # Fail sooner if the total inventory is less than the request, regardless
    # of current rentals

    if inventory < requested_quantity:
        return False
    
    # Checks if there is overlap between another request and current request
    overlapping_rentals = []
    
    # Now we have a list with the existing rentals that overlap with the request
    for rental in existing_rentals:
        if rental.item == item:
            if start_date <= rental.end_date and rental.start_date <= end_date:
                overlapping_rentals.append(rental)
    
    # Now we have a list of days of the request
    # request_date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    # request_days_list = [d.date() for d in request_date_range]
    
    request_days_list = [start_date + timedelta(days = x) for x in range((end_date - start_date).days + 1)]
    
    # Loop through days
    for day in request_days_list:
        available_inventory = inventory
        # Within a day, loop through overlapping rentals and extract the days into a list
        for overlapping_rental in overlapping_rentals:
            # date_range = pd.date_range(start=overlapping_rental.start_date, end=overlapping_rental.end_date, freq='D')
            # days_list = [d.date() for d in date_range]
            days_list = [overlapping_rental.start_date + timedelta(days = x) for x in range((overlapping_rental.end_date - overlapping_rental.start_date).days + 1)]
            # If the day in the request list exists in the overlapping rentals list, reduce the available inventory by that amount
            if day in days_list:
                if overlapping_rental.status == "confirmed":
                    available_inventory -= overlapping_rental.requested_quantity
        if available_inventory >= requested_quantity:
            continue
        else:
            return False
                      
    return True
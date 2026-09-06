
class ExistingRental:
    
    def __init__(self, requested_quantity, start_date, end_date, status):
        self.requested_quantity = requested_quantity
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

def check_availability(inventory, requested_quantity, start_date, end_date, existing_rentals):

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
    
    # Checks if there is overlap between another request and current request
    available_inventory = inventory

    for request in existing_rentals:
        if start_date <= request.end_date and request.start_date <= end_date:
            if request.status == "confirmed":
                available_inventory -= request.requested_quantity
            
    # Checks if the inventory is greater or equal to the requested_quantity
    if available_inventory >= requested_quantity:
        return True
    else:
        return False
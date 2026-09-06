from festival_rental_ops.availability import ExistingRental, check_availability
from datetime import date
import pytest

def test_request_is_available_when_inventory_is_sufficent():
    item = "radio"
    inventory = 500
    requested_quantity = 400
    start_date = date(2025, 9, 1)
    end_date = date(2025, 9, 4)
    existing_rentals = []
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == True
    
def test_request_is_exact_inventory_quantity():
    item = "radio"
    inventory = 500
    requested_quantity = 500
    start_date = date(2025, 9, 1)
    end_date = date(2025, 9, 4)
    existing_rentals = []
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == True
    
def test_insufficient_inventory():
    item = "radio"
    inventory = 500
    requested_quantity = 600
    start_date = date(2025, 9, 1)
    end_date = date(2025, 9, 4)
    existing_rentals = []
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == False
    
def test_requested_quantity_is_zero():
    item = "radio"
    inventory = 100
    requested_quantity = 0
    start_date = date(2025, 9, 1)
    end_date = date(2025, 9, 4)
    existing_rentals = []
    
    with pytest.raises(ValueError) as exc_info:
        check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals)
    
    assert "Requested quantity must be a positive whole number" in str(exc_info.value)

def test_requested_quantity_is_negative():
    item = "radio"
    inventory = 100
    requested_quantity = -50
    start_date = date(2025, 9, 1)
    end_date = date(2025, 9, 4)
    existing_rentals = []
    
    with pytest.raises(ValueError) as exc_info:
        check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals)
    
    assert "Requested quantity must be a positive whole number" in str(exc_info.value)
    
def test_requested_quantity_is_not_whole_number():      
    item = "radio"
    inventory = 500
    requested_quantity = 8.7
    start_date = date(2025, 9, 1)
    end_date = date(2025, 9, 4)
    existing_rentals = []
    
    with pytest.raises(ValueError) as exc_info:
        check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals)
    
    assert "Requested quantity must be a numeric whole number" in str(exc_info.value)
    
def test_valid_multiday_request():
    item = "radio"
    inventory = 500
    requested_quantity = 300
    start_date = date(2025, 9, 1)
    end_date = date(2025, 9, 4)
    existing_rentals = []
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == True
    
def test_same_day_request():
    item = "radio"
    inventory = 500
    requested_quantity = 300
    start_date = date(2025, 9, 1)
    end_date = date(2025, 9, 1)
    existing_rentals = []
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == True
    
def test_end_date_before_start_date():
    item = "radio"
    inventory = 500
    requested_quantity = 300
    start_date = date(2025, 9, 3)
    end_date = date(2025, 9, 2)
    existing_rentals = []
    
    with pytest.raises(ValueError) as exc_info:
        check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals)
    
    assert "Start date cannot be after the end date" in str(exc_info.value)
    
def test_no_rental_overlap():
    item = "radio"
    inventory = 100
    requested_quantity = 80
    start_date = date(2025, 9, 10)
    end_date = date(2025, 9, 12)
    existing_rentals = [ExistingRental("radio", 80, date(2025, 9, 1), date(2025, 9, 3), "confirmed")]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == True
    
def test_rental_overlap_sufficient_inventory():
    item = "radio"
    inventory = 200
    requested_quantity = 100
    start_date = date(2025, 9, 11)
    end_date = date(2025, 9, 13)
    existing_rentals = [ExistingRental("radio", 50, date(2025, 9, 10), date(2025, 9, 14), "confirmed")]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == True
    
def test_rental_overlap_insufficient_inventory():
    item = "radio"
    inventory = 200
    requested_quantity = 100
    start_date = date(2025, 9, 11)
    end_date = date(2025, 9, 13)
    existing_rentals = [ExistingRental("radio", 150, date(2025, 9, 10), date(2025, 9, 14), "confirmed")]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == False
    
def test_canceled_overlapping_rental():
    item = "radio"
    inventory = 200
    requested_quantity = 100
    start_date = date(2025, 9, 11)
    end_date = date(2025, 9, 13)
    existing_rentals = [ExistingRental("radio", 180, date(2025, 9, 10), date(2025, 9, 14), "canceled")]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == True
    
def test_draft_overlapping_rental():
    item = "radio"
    inventory = 200
    requested_quantity = 100
    start_date = date(2025, 9, 11)
    end_date = date(2025, 9, 13)
    existing_rentals = [ExistingRental("radio", 180, date(2025, 9, 10), date(2025, 9, 14), "draft")]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == True

def test_confirmed_overlapping_rental():
    item = "radio"
    inventory = 200
    requested_quantity = 100
    start_date = date(2025, 9, 11)
    end_date = date(2025, 9, 13)
    existing_rentals = [ExistingRental("radio", 180, date(2025, 9, 10), date(2025, 9, 14), "confirmed")]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == False
    
def test_existing_rental_ends_on_new_start_date():
    item = "radio"
    inventory = 100
    requested_quantity = 50
    start_date = date(2025, 9, 12)
    end_date = date(2025, 9, 14)
    existing_rentals = [ExistingRental("radio", 60, date(2025, 9, 10), date(2025, 9, 12), "confirmed")]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == False
    
def test_existing_rental_starts_on_new_end_date():
    item = "radio"
    inventory = 100
    requested_quantity = 50
    start_date = date(2025, 9, 10)
    end_date = date(2025, 9, 12)
    existing_rentals = [ExistingRental("radio", 60, date(2025, 9, 12), date(2025, 9, 14), "confirmed")]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == False
    
def test_existing_rental_ends_day_before():
    item = "radio"
    inventory = 100
    requested_quantity = 80
    start_date = date(2025, 9, 12)
    end_date = date(2025, 9, 14)
    existing_rentals = [ExistingRental("radio", 80, date(2025, 9, 10), date(2025, 9, 11), "confirmed")]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == True
    
def test_multiple_rentals_insufficient_inventory():
    item = "radio"
    inventory = 500
    requested_quantity = 200
    start_date = date(2025, 9, 12)
    end_date = date(2025, 9, 12)
    existing_rentals = [
        ExistingRental("radio", 200, date(2025, 9, 10), date(2025, 9, 14), "confirmed"), 
        ExistingRental("radio", 150, date(2025, 9, 11), date(2025, 9, 13), "confirmed")
        ]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == False
    
def test_multiple_rentals_overlap_new_req_but_not_each_other():
    item = "radio"
    inventory = 500
    requested_quantity = 200
    start_date = date(2025, 9, 10)
    end_date = date(2025, 9, 14)
    existing_rentals = [
        ExistingRental("radio", 300, date(2025, 9, 10), date(2025, 9, 11), "confirmed"), 
        ExistingRental("radio", 300, date(2025, 9, 13), date(2025, 9, 14), "confirmed")
        ]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == True
    
def test_insufficient_inventory_one_day():
    item = "radio"
    inventory = 500
    requested_quantity = 200
    start_date = date(2025, 9, 10)
    end_date = date(2025, 9, 14)
    existing_rentals = [
        ExistingRental("radio", 100, date(2025, 9, 10), date(2025, 9, 14), "confirmed"), 
        ExistingRental("radio", 250, date(2025, 9, 12), date(2025, 9, 12), "confirmed")
        ]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == False
    
def test_rental_exists_for_other_item():
    item = "headset"
    inventory = 100
    requested_quantity = 80
    start_date = date(2025, 9, 10)
    end_date = date(2025, 9, 14)
    existing_rentals = [
        ExistingRental("radio", 80, date(2025, 9, 10), date(2025, 9, 14), "confirmed"), 
        ]
    
    assert check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals) == True
    
def test_requested_item_doesnt_exist():
    item = "speaker"
    inventory = 0
    requested_quantity = 5
    start_date = date(2025, 9, 10)
    end_date = date(2025, 9, 14)
    existing_rentals = []
    
    with pytest.raises(ValueError) as exc_info:
        check_availability(item, inventory, requested_quantity, start_date, end_date, existing_rentals)
    
    assert "Requested item was not found" in str(exc_info.value)



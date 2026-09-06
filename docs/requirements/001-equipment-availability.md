# Requirement 001 — Equipment Availability

## Problem

Sales currently determines equipment availability by manually reviewing inventory and rental spreadsheets.

This process becomes unreliable when multiple rentals overlap.

Sales needs a reliable way to answer:

> Can we provide a requested quantity of a product for a specified rental period?

## Inputs

- Product
- Requested quantity
- Rental start date
- Rental end date

## Expected Result

The system should determine:

- Quantity owned
- Quantity already committed during the requested period
- Lowest available quantity during the requested period
- Whether the requested quantity can be fulfilled
- Shortfall, if the request cannot be fulfilled

## Initial Business Rules

- Rental dates use calendar days.
- Start dates are inclusive.
- End dates are inclusive from the user's perspective.
- Requested quantity must be a positive integer.
- Confirmed rentals reduce availability.
- Canceled rentals do not reduce availability.
- Draft quotes do not reduce availability.
- Non-overlapping rentals do not affect one another.

## Explicitly Out of Scope

The first version will not account for:

- Broken equipment
- Missing equipment
- Serialized individual assets
- Equipment maintenance
- Multiple warehouses
- Transportation or delivery
- Pricing
- Payments
- Authentication
- Employee permissions

These limitations are intentional. They will be addressed only when business requirements justify additional complexity.

## Success Criteria

Given a product, quantity, start date, and end date, the system can reliably determine whether enough inventory remains available throughout the requested rental period.
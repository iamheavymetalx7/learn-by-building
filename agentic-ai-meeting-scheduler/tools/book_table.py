import csv
from datetime import datetime


def book_table(table_name: str, time: str, reservation_name: str) -> bool:
    # print(table_name, time, reservation_name)

    # Read the current bookings
    with open("data/bookings.csv", "r") as file:
        reader = csv.DictReader(file)
        bookings = list(reader)

    # Find the correct row and check if the slot is available
    for booking in bookings:
        # print(booking)
        # print(booking["time"],"before stripping")
        booking_time = booking["time"]
        # print(booking_time, "...",table_name,"inside the for",time, time== booking_time)
        for x in ['(2p)','(4p)']:
            upd_table_name = table_name + " "+x
            # print(upd_table_name,"upd table anme")
            if booking_time == time and upd_table_name in booking:
                # print("inside the if")
                if booking[upd_table_name] == '':
                    # The slot is available, update it
                    booking[upd_table_name] = reservation_name

                    # Write the updated bookings back to the CSV
                    with open("data/bookings.csv", "w", newline="") as file:
                        fieldnames = reader.fieldnames
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(bookings)

                    return (
                        f"✅ Booking Success: {table_name} at {time} for {reservation_name}"
                    )
                else:
                    return f"❌ Booking Failed: {table_name} at {time} is already booked"

    return f"❌ Booking Failed: {table_name} at {time} not found"
import DB_access
import validators
import Room_Avaliability
import pricing
from datetime import datetime
 
from models import Guest,Booking
def create_booking():
    result=Room_Avaliability.room_availability()
    if result is None:
        return
    room,guests,check_in,check_out=result
    try:
        name=input("Enter guest name: ")
        name=validators.validate_name(name)
 
        mobile=input("Enter mobile number: ")
        mobile=validators.validate_mobile_number(mobile)
 
        email=input("Enter email address: ")
        email=validators.validate_email(email)
 
        if room.room_type=="Standard":
            breakfast=input("Do you want breakfast? (yes/no): ").strip().lower()
 
            if breakfast not in ["yes","no"]:
                raise ValueError("Enter yes or no")
 
            breakfast=breakfast=="yes"
 
        else:
            breakfast=True
            print("Breakfast is included in this room.")
 
        guest=Guest(name,mobile,email)
 
        booking=Booking(
            guest,
            room,
            check_in,
            check_out,
            guests,
            breakfast
        )
 
        completed_stays=DB_access.get_completed_stays(mobile)
 
        amount_details=pricing.calculate_total_amount(
            booking,
            completed_stays
        )
 
        print("\nBooking Summary")
        print("----------------------")
        print("Booking ID:",booking.booking_id)
        print("Guest Name:",guest.name)
        print("Mobile:",guest.mobile)
        print("Room:",room.room_type)
        print("Room Number:",room.room_number)
        print("Guests:",guests)
        print("Check-in:",check_in)
        print("Check-out:",check_out)
 
        print("\nPayment Details")
        print("----------------------")
 
        for key,value in amount_details.items():
            print(key,": ₹",round(value,2))
 
        payment=input("\nConfirm full payment and booking? (yes/no): ").strip().lower()
 
        if payment=="yes":
 
            DB_access.create_booking(booking)
 
            print("\nPayment successful!")
            print("Booking confirmed successfully.")
            print("Your Booking ID:",booking.booking_id)
 
        else:
            print("Booking cancelled by user.")
 
    except ValueError as e:
        print("Error:",e)
 
    except Exception as e:
        print("Booking failed:",e)
 
from datetime import date
 
 
def check_in():
 
    booking_id=input("Enter Booking ID: ").strip()
 
    try:
        booking_details=DB_access.get_booking_details(booking_id)
 
        if booking_details is None:
            print("Booking not found.")
            return
 
        check_in_date=booking_details[7]
        status=booking_details[11]
 
        if status!="CONFIRMED":
            print("Invalid booking status. Check-in is not allowed.")
            return
 
        today=date.today().strftime("%Y-%m-%d")
 
        if today<check_in_date:
            print("Check-in date has not arrived yet.")
            return
 
        if today>check_in_date:
            print("Check-in date has already passed.")
            return
 
        updated=DB_access.update_booking_status(
            booking_id,
            "CHECKED_IN"
        )
 
        if updated:
            print("Check-in successful!")
            print("Booking ID:",booking_id)
            print("Guest Name:",booking_details[1])
            print("Room Number:",booking_details[4])
            print("Status: CHECKED_IN")
 
    except Exception as e:
        print("Check-in failed:",e)
 
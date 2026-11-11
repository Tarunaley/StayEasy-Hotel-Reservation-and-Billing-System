from datetime import datetime,date
import DB_access
def room_availability():
    while True:
        room_type=input("Enter room_type:").strip()
        no_of_guests=input("Enter number of guests:").strip()
        check_in=input("Enter check-in date:").strip()
        check_out=input("Enter check-out date:").strip()
        isvalid_entry=True
        if room_type.lower() not in ['standard','deluxe','suite']:
            print("Enter valid room-type")
            isvalid_entry=False
        if not(no_of_guests.isdigit() and int(no_of_guests)>0):
            print("Enter valid number of guests")
            isvalid_entry=False
        if no_of_guests.isdigit() and int(no_of_guests)>0:
            guests=int(no_of_guests)
            if room_type.lower()=='standard' and guests>2:
                print("For standard type number of guests exceeded")
                isvalid_entry=False
            if room_type.lower()=='deluxe' and guests>3:
                print("For deluxe type number of guests exceeded")
                isvalid_entry=False
            if room_type.lower()=='suite' and guests>4:
                print("For suite type number of guests exceeded")
                isvalid_entry=False
        try:
            check_in=datetime.strptime(check_in,"%d/%m/%Y").date()
            if check_in<date.today():
                print("Check-in date cannot be in the past")
                isvalid_entry=False
        except ValueError:
            print("Check-in date is invalid")
            isvalid_entry=False
        try:
            check_out=datetime.strptime(check_out,"%d/%m/%Y").date()
        except ValueError:
            print("Check-out date is invalid")
            isvalid_entry=False
        if check_in>=check_out:
            print("Check-out date must be after check-in date")
            isvalid_entry=False
        if not isvalid_entry:
            print("Re-enter the details")
            continue
        break
    available_room=DB_access.get_available_rooms(room_type.lower(),check_in.strftime("%Y-%m-%d"),check_out.strftime("%Y-%m-%d"))

    if not available_room:
        print("No rooms available for the requested dates")
        return None

    
    # room_details=[room_type.lower(),guests,check_in,check_out]
    # return room_details
    return available_room,room_type.lower(),guests,check_in,check_out
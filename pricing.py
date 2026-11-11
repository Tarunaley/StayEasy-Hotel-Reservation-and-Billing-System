from datetime import timedelta
def calculate_room_charges(booking): 
    room=booking.room
    check_in=booking.check_in
    check_out=booking.check_out
    total_room_charges=0
    current_date=check_in
    while current_date<check_out:
        daily_tariff=room.tariff()
        if current_date.weekday() in [4,5]:
            daily_tariff=daily_tariff+(daily_tariff*20/100)
        total_room_charges+=daily_tariff
        current_date=current_date+timedelta(days=1)
    return total_room_charges
def calculate_extra_guest_charges(booking):
    if booking.room.room_type=="Standard":
        return 0
    extra_guests=booking.guests_count-2
    if extra_guests<=0:
        return 0
    no_of_nights=(booking.check_out-booking.check_in).days
    return extra_guests*booking.room.extra_guest_charges()*no_of_nights

def calculate_breakfast_charges(booking): 
    if booking.room.room_type!="Standard":
        return 0
    if not booking.breakfast:
        return 0
    no_of_nights=(booking.check_out-booking.check_in).days
    return booking.guests_count*booking.room.breakfast_fee()*no_of_nights
def calculate_total_amount(booking,completed_stays=0):
    room_charges=calculate_room_charges(booking)
    extra_guest_charges=calculate_extra_guest_charges(booking)
    breakfast_charges=calculate_breakfast_charges(booking)
    discount=0
    if (booking.check_out-booking.check_in).days>=7:
        discount=discount+(room_charges*10/100)
    if completed_stays>=3:
        discount=discount+(room_charges*5/100)
    total_before_gst=room_charges+extra_guest_charges+breakfast_charges-discount
    if booking.room.tariff()>7500:
        gst=total_before_gst*18/100
    else:
        gst=total_before_gst*12/100
    final_amount=total_before_gst+gst
 
    return {
        "room_charges":room_charges,
        "extra_guest_charges":extra_guest_charges,
        "breakfast_charges":breakfast_charges,
        "discount":discount,
        "gst":gst,
        "total_amount":final_amount
    }
 
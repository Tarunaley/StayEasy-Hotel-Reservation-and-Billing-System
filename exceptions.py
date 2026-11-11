class StayEasyException(Exception):
    pass 
class InvalidBookingError(StayEasyException):
    pass
class RoomNotAvailableError(StayEasyException):
    pass
class InvalidDateError(StayEasyException):
    pass
class InvalidStatusError(StayEasyException):
    pass
class BookingNotFoundError(StayEasyException):
    pass
 
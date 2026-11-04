import csv
from abc import ABC,abstractmethod
from datetime import datetime,date,timedelta
rooms_data=[]
with open("rooms.csv","r") as file:
    reader=csv.DictReader(file)
    for row in reader:
        rooms_data.append(row)
seen_ids=set()
with open("app.log","w") as file:
    try:
        for row in rooms_data:
            if row['room_no']=="" or row['room_type']=="" or row['floor']=="":
                file.write("Values cannot be null")
                continue
            if row['room_no'] in seen_ids:
                file.write(f"{row['room_no']} duplicate room found")
                continue
            if row['room_type'].lower() not in ['standard','deluxe','suite']:
                file.write(f"{row['room_no']} room_type is invalid\n")
                continue
            if not (row['floor'].isdigit() and int(row['floor'])>0):
                file.write(f"{row['room_no']} floor is in-valid\n")
                continue
            seen_ids.add(row['room_no'])
    except ValueError as e:
        print(e)
class Room(ABC):
    def __init__(self,room_no,room_type,floor):
        self.room_no=room_no
        self.room_type=room_type
        self.floor=floor
    @abstractmethod
    def tariff(self,day):
        pass
    @abstractmethod
    def extra_guest_charges(self):
        pass
    @abstractmethod
    def breakfast(self):
        pass
class Standard_Room(Room):
    def __init__(self,room_no,room_type,floor,check_in,check_out,number_of_guests,Is_loyal):
        super().__init__(room_no,room_type,floor)
        self.check_in=check_in
        self.check_out=check_out
        self.number_of_guests=number_of_guests
        self.Is_loyal=Is_loyal
        self.cost=0
        self.base_price=2500
        self.extra_guest_charge=0
        self.breakfast_charge=350
        
    def tariff(self):
        number_of_stays=(self.check_out-self.check_in).days
        day_names=[]
        for i in number_of_stays:
             current_date=self.check_in+timedelta(days=i)
             day_name=(current_date.strftime("%A"))
             if day_name.lower() not in ['friday','saturday']:
                  self.cost+=self.base_price
             else:
                  self.cost+=self.base_price+((20/100)*self.base_price)
            
    def extra_guest_charges(self):
        return self.extra_guest_charge
    def breakfast(self):
        return self.breakfast_charge
class Deluxe_Room(Room):
     def __init__(self,room_no,room_type,floor):
        super().__init__(room_no,room_type,floor)
        self.cost=0
        self.base_price=4000
        self.extra_guest_charge=800
        self.breakfast_charge=0
     def tariff(self):
            return self.base_price
     def extra_guest_charges(self):
            return self.extra_guest_charge
     def breakfast(self):
            return self.breakfast_charge
class Suite_room(Room):
     def __init__(self,room_no,room_type,floor):
            super().__init__(room_no,room_type,floor)
            self.cost=0
            self.base_price=7500
            self.extra_guest_charge=800
            self.breakfast_charge=0
     def tariff(self):
            return self.base_price
     def extra_guest_charges(self):
            return self.extra_guest_charge
     def breakfast(self):
            return self.breakfast_charge
class Guest:
     def __init__(self,name,mobile_number,email_address):
          self.name=name
          self.mobile_number=mobile_number
          self.email_address=email_address
     @property
     def name(self):
          return self.name
     @name.setter
     def name(self,value):
          self.name=validators.validate_name(value)
     @property
     def mobile_number(self):
          return self.mobile_number
     @mobile_number.setter
     def mobile_number(self,value):
          self.mobile_number=validators.validate_mobile_number(value)
     @property
     def email_address(self):
          return self.email_address
     @email_address.setter
     def email_address(self,value):
          self.email_address=validators.validate(value)
# class Booking:
    #  def __init__(self,check_in,check_out):
    #       self.check_in=check_in
    #       self.check_out=check_out

          
     


        


        

     

def validate_name(name):
    if name is None:
        raise ValueError("Name cannot be null")
    name = name.strip()
    if name == "":
        raise ValueError("Name cannot be empty")
    return name
def validate_mobile_number(mobile_number):
    mobile_number=mobile_number.strip().split()
    if len(mobile_number)!=10:
        raise ValueError("mobile number is not valid")
    if mobile_number[0] not in ['6','7','8','9']:
        raise ValueError("Mobile number should start with 6/7/8/9")
    return mobile_number
def validate_email(email_address):
    email_address=email_address.strip().split()
    if not '@' in email_address:
        raise ValueError("Invalid email-address")
    return email_address  
    
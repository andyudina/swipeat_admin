from os import urandom

def to_boolean(value):
    if value is None:
        return False
    return (value == 'on')
  
       
def generate_password(length=8):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join([chars[ord(c) % len(chars)] for c in urandom(length)])    

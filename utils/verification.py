import math, random
 
def generate_verification_code() :
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    length = len(string)
    
    code = ""
    for i in range(6) :
        code += string[math.floor(random.random() * length)]
 
    return code

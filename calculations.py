def LCM(self, Num1, Num2):
    if Num1 >= Num2:
        Greater = Num1
    else:
        Greater = Num2
    
    while True:
        if((Greater % Num1 == 0) and (Greater % Num2 == 0)):
            LCM = Greater
            break
        Greater += 1
    return LCM
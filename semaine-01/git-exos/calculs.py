def add (a, b):
    """ Addition de deux nombres"""
    return (a + b)

def multiply (a,b) :
    return (a * b)

def subtract (a , b) :
    return ( a - b)
def divide (a, b) :
    if b <= 0 :
        print ("erreur: impossible de diviser un nombre par 0")
    else :
        return (a/b) 
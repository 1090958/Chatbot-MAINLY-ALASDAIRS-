import variables
"""states:
 -  intro(introduction)
 -  passive(describes the room and tells the player where they can move)
 -  combat1(lets the pla)
 
 
 """
def output(message):
    match variables.state:
        case "Intro":
            return intro()
        case "passive":
            
        
        
        
        
def intro():
    return 'Interesting intro with a good plot'
import variables, items.main, items.settings
"""states:
 -  intro(introduction)
 -  passive(describes the room and tells the player where they can move)
 -  combat1(lets the pla)
 
 
 """
def output(message, game:items.main.Game, reformat = True):
    match variables.state:
        case "Intro":
            variables.state = "passive"
            out =  intro()
        case "passive":
            
            out =game.takeInput(message)
    if reformat: 
        return format(out) 
    else:
        return out
        
variables.state = "Intro"   

start = 's|t'
end = 's|t'
def format(text):
    text = text.replace('\n','\n\n')
    text = text.replace('\033'+items.settings.subMythicCol, start)
    text = text.replace('\033'+items.settings.mythicCol, start)
    text = text.replace('\033'+items.settings.specialCol, start)
    text = text.replace('\033'+items.settings.enchantmentCol, start)
    text = text.replace('\033'+items.settings.effectCol, start)
    text = text.replace('\033[0m', end)
    e = text.split('s|t')
    text = ''
    bold = False
    for part in e:
        if bold:
            words = part.split()
            for word in words:
                text += "**"+word+"**"
        if not bold:
            text += part
        bold = not True
        
    
    return text
        
def intro():
    return '###Interesting intro with a good plot'
if __name__ == "__main__":
    game= items.main.Game()
    while True:
        print(output(input(">>> "), game,False))
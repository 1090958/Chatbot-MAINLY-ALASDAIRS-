from bardapi import Bard

token='Wwh87sYn2QNDb_6wQebii1SDMYe_tTTGaFdUvlFbvPBW-u_R_bx8STYThDs2GBodI92urw.'

bard=Bard(token=token)

def generate_input(inputs,held,items,enemies,Allies):
    return f'''
The generator is a computer that returns a function given : 
an input(input), 
the currently equiped weapon(held), 
a list of all items(items),
a list of enemies' names(enemies) 
and a list of allies' names(allies). 
The function it returns can be hit(enemy, weapon, time) or heal(ally)

In example, when input = 'I will hit Jeff with my Axe', held='Axe', items=['Axe'], enemies=['Gerald', 'Joe'], Allies=[]

The generator would return the following:
hit('Jeff', 'Axe')

This is because the input indicates that the user wants to hit Jeff with an axe, and the held weapon is an axe. The items list only contains an axe, so there are no other weapons that the user could use. The enemies list contains two enemies, Gerald and Joe, but only Jeff is mentioned in the input. Therefore, the generator will assume that the user wants to hit Jeff. The allies list is empty, so there are no allies that the user could heal.
Here is a more detailed explanation of how the generator arrives at this conclusion:
* The input "I will hit Jeff with my Axe" indicates that the user wants to hit Jeff with an axe.
* The held weapon is an axe, so the user has the means to carry out their desired action.
* If the held weapon is the weapon desired time = 1, else it is 2
* The items list only contains an axe, so there are no other weapons that the user could use.
* The enemies list contains two enemies, Gerald and Joe, but only Jeff is mentioned in the input. Therefore, the generator will assume that the user wants to hit Joe, as he is closer to Jeff.
* The allies list is empty, so there are no allies that the user could heal.
* There is no such thing as a healig item so healing can be called anytime


secondly when input = 'I will heal at Bob with my axe', held='Axe', items=['Sword', 'Axe', 'dagger'], enemies=['Timothy','Gerald'], Allies=['Bob']
The generator would return the following:
heal('Bob')
this is tricky as the input talks about an axe, luckily the generator knows that the user wants to heal, it ignores the axe entirely, 

finally when input = 'I will heal at Bob with my knife', held='Axe', items=['Sword', 'Axe', 'dagger'], enemies=['Timothy','Gerald'], Allies=['John']
The generator would return the following:
heal('John')
This is resulting as Bob is not an ally, the generator, if no target is shown chooses a possible intended target of the input, for this case John






Pretend you're the generator what would the generator return when input = '{inputs}', held={held}, items={items}, enemies={enemies}, Allies={Allies}

only give the output of the generator as an answer, do not surround the answer in quotation marks
'''
def hit(target, weapon, damage):
    print(f"{target} was hit with {weapon} for {damage} damage.")
def heal(target):
    print(f"{target} was healed.")

def generate(inputs = '', held='', items=[''], enemies=[], Allies=[]):
    print('go')
    inputinfo=(generate_input(inputs,held,items,enemies,Allies))
    string = bard.get_answer(inputinfo)['content'].split('\n')
    for line in string:
        try:
            #check if the line can be run as a function
            # if it can, return the line
            # if it can't, try the next line
            exec(line)
            #print('success')
            break
        except:
            pass
            #print('failed line')
    
        #print('failed line')
#print('\n'.join(string))
if __name__ == '__main__':
    print(generate(inputs = 'I will hit Timothy', held='Axe', items=['Sword', 'Axe', 'Dagger'], enemies=['Timothy','Gerald'], Allies=['Mary Poppins']))

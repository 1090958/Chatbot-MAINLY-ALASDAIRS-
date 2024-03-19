
class roomtype:
    class library:
        def describe()->str:
            return  'knowlage flows from the walls, the library expands around you. '
        def getitems():
            return  {2:'books', 5:'explosives'}
        def getenimies():
            return ['jeff the goblin']

    class regular:
        def describe()->str:
            return  'stupid room'
        def getitems():
            return  {2:'cokeaddicts', 5:'explosives'}
        def getenimies():
            return ['jeff the goblin']
"""   items and actual monsters should be added in, then advanced d gen should str the objects to print them.  """

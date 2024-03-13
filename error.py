class error_Thrower(Exception):
    "generic error"
    pass
class invalid_Attribute_Type(Exception):
    "Raised when the attribute of a weapon is not an correct"
    def __init__(self, attribute, expected:type|tuple, message=None):
        if message == None:
            if type(expected) != tuple:
                message = f"An attribute of a weapon was not of the correct type, it was of the type, {str(type(attribute))[7:-1]}, the type {str(expected)[7:-1]}, was expected"
            elif type(expected) == tuple:
                message = f"An attribute of a weapon was not of the correct type, it was of the type, {str(type(attribute))[7:-1]}, the types of {', '.join([str(_)[7:-1] for _ in expected[:-1]])+f' or {str(expected[-1])[7:-1]}'} were expected"
        super().__init__(message)
        
class invalid_character(Exception):
    "Raised when an input character"
    def __init__(self, character, message=None):
        if message == None:
            message = f"An input character was not correct, it was of the type, {str(type(character))} not of <class 'character.character'>"
        super().__init__(message)
        
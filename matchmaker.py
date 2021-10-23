def isNotAnInt(input):
    return not isinstance(input, int)

def isPositive(input):
    try:
        if isNotAnInt(input):
            raise TypeError('Should be an integer')
        return input > 0
    except TypeError as err:
        raise err

def isPositiveInt(input):
    if isNotAnInt(input):
        raise TypeError('Should be an integer')
    if not isPositive(input):
        raise ValueError('Value should be positive int')
    return True

def isRoundOne(round):
    try:
        if isPositiveInt(round):
            return round == 1
    except (TypeError, ValueError, Exception) as err:
        print(repr(err))

def isEven(i):
    try:
        if isPositiveInt(i):
            return i % 2 == 0
    except (TypeError, ValueError, Exception) as err:
        print(repr(err))

def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def generate_first_round_matches(first_list, second_list):
    return list(map(lambda a,b: (a,b), first_list, second_list))

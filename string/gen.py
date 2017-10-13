from random import randint


def get_letter():
    return chr(randint(97, 122))


def get_word(max_length=9):
    num_char = randint(2, max_length)
    word = ""
    for i in xrange(num_char):
        word += get_letter()
    return word


def get_digit():
    return randint(0, 9)


def two_pairs():
    """returns (input, output) pair"""
    category = randint(1, 15)

    # extracts first name
    if category == 1:
        first, last = get_word(), get_word()
        return first + ' ' + last, first
    # extracts last name
    elif category == 2:
        first, last = get_word(), get_word()
        return first + ' ' + last, last
    # extracts initials
    elif category == 3:
        first, last = get_word(), get_word()
        return first + ' ' + last, first[0] + ' ' + last[0]

    # first name and initial of last
    elif category == 4:
        first, last = get_word(), get_word()
        return first + ' ' + last, first + ' ' + last[0]

    # gets part before @
    elif category == 5:
        first = get_word()
        email = '{}@{}.{}'.format(first, get_word(5), get_word(3))
        return email, first

    # reformats phone number 111-222-3333 -> (111)-222-3333
    elif category == 6:
        num = ''.join([str(get_digit()) for i in xrange(10)])
        num = num[:3] + '-' + num[3:6] + '-' + num[6:]
        return num, '(' + num[:3] + ')' + num[3:]

    # concats words
    elif category == 7:
        words = [get_word(4) for i in xrange(3)]
        return ' '.join(words), ''.join(words)

    # extract year from date
    elif category == 8:
        year = randint(1, 9999)
        date = '{}/{}/{}'.format(randint(1, 12), randint(1, 30), year)
        return date, year

    # extract day from date
    elif category == 9:
        day = randint(1, 30)
        date = '{}/{}/{}'.format(randint(1, 12), day, randint(1, 9999))
        return date, day

    # extract month from date
    elif category == 10:
        month = randint(1, 12)
        date = '{}/{}/{}'.format(month, randint(1, 30), randint(1, 9999))
        return date, month

    # reverse words
    elif category == 11:
        words = ' '.join([get_word(6) for i in xrange(3)])
        return words, words[::-1]

    # names in different format Bob Smith -> Smith, Bob
    elif category == 12:
        first, last = get_word(), get_word()
        return first + ' ' + last, last + ', ' + first

    # more phone number formatting 2223334444 -> 222-333-4444
    elif category == 13:
        num = ''.join([str(get_digit()) for i in xrange(10)])
        return num, num[:3] + '-' + num[3:6] + '-' + num[6:]

    # extracts dollar amount
    elif category == 14:
        num = '{}.{}'.format(randint(0, 99999999), randint(10, 99))
        return num, num[:-3]

    # extracts cents
    elif category == 15:
        num = '{}.{}'.format(randint(0, 99999999), randint(10, 99))
        return num, num[-2:]

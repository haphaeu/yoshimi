# problem17.py
"""
Find the solution to `Problem 17`_ at `Project Euler`_.

.. _Problem 17: http://projecteuler.net/index.php?section=problems&id=17
.. _Project Euler: http://projecteuler.net/
"""
__docformat__ = "restructuredtext en"

import re

_NUMBER_NAMES = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
                6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
                11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
                15: "fifteen", 16: "sixteen", 17: "seventeen",
                18: "eighteen", 19: "nineteen", 20: "twenty",
                21: "twenty-one", 22: "twenty-two", 23: "twenty-three",
                24: "twenty-four", 25: "twenty-five", 26: "twenty-six",
                27: "twenty-seven", 28: "twenty-eight", 29: "twenty-nine",
                30: "thirty", 31: "thirty-one", 32: "thirty-two",
                33: "thirty-three", 34: "thirty-four", 35: "thirty-five",
                36: "thirty-six", 37: "thirty-seven", 38: "thirty-eight",
                39: "thirty-nine", 40: "forty", 41: "forty-one",
                42: "forty-two", 43: "forty-three", 44: "forty-four",
                45: "forty-five", 46: "forty-six", 47: "forty-seven",
                48: "forty-eight", 49: "forty-nine", 50: "fifty",
                51: "fifty-one", 52: "fifty-two", 53: "fifty-three",
                54: "fifty-four", 55: "fifty-five", 56: "fifty-six",
                57: "fifty-seven", 58: "fifty-eight", 59: "fifty-nine",
                60: "sixty", 61: "sixty-one", 62: "sixty-two",
                63: "sixty-three", 64: "sixty-four", 65: "sixty-five",
                66: "sixty-six", 67: "sixty-seven", 68: "sixty-eight",
                69: "sixty-nine", 70: "seventy", 71: "seventy-one",
                72: "seventy-two", 73: "seventy-three", 74: "seventy-four",
                75: "seventy-five", 76: "seventy-six", 77: "seventy-seven",
                78: "seventy-eight", 79: "seventy-nine", 80: "eighty",
                81: "eighty-one", 82: "eighty-two", 83: "eighty-three",
                84: "eighty-four", 85: "eighty-five", 86: "eighty-six",
                87: "eighty-seven", 88: "eighty-eight", 89: "eighty-nine",
                90: "ninety", 91: "ninety-one", 92: "ninety-two",
                93: "ninety-three", 94: "ninety-four", 95: "ninety-five",
                96: "ninety-six", 97: "ninety-seven", 98: "ninety-eight",
                99: "ninety-nine"}

_CHARACTERS_WE_CARE_ABOUT = re.compile("\w")

def _words_from_num(num):
    """
    Convert ``num`` to its (British) English phrase equivalent.

    If ``num`` is greater than 9,999 then raise an ``Exception``.
    >>> _words_from_num(115)
    'one hundred and fifteen'
    """
    if num >= 10000:
        raise Exception, 'This function only supports numbers less than 10000.'

    parts_list = []
    if num >= 1000:
        thousands = num // 1000
        parts_list.append(_NUMBER_NAMES[thousands])
        parts_list.append(" thousand")
        num -= thousands * 1000
    if num >= 100:
        hundreds = num // 100
        parts_list.append(_NUMBER_NAMES[hundreds])
        parts_list.append(" hundred")
        num -= hundreds * 100
    if num:
        if parts_list:
            parts_list.append(" and")
        parts_list.extend([" ", _NUMBER_NAMES[num]])

    return "".join(parts_list)

def _count_characters_we_care_about(string_to_count):
    """
    Count the characters in ``string_to_count``, excluding things like hyphens and spaces.

    >>> _count_characters_we_care_about("one hundred and twenty-three")
    24
    """
    return len(_CHARACTERS_WE_CARE_ABOUT.findall(string_to_count))

def problem_17(upper_bound = 1000):
    """
    Find the solution to `Problem 17`_ at `Project Euler`_.

    .. _Problem 17: http://projecteuler.net/index.php?section=problems&id=17
    .. _Project Euler: http://projecteuler.net/

    >>> problem_17(2)
    6
    """
    converted_nums = (_words_from_num(num) for num in xrange(1, upper_bound + 1))
    lengths = (_count_characters_we_care_about(phrase) for phrase in converted_nums)
    return sum(lengths)

if __name__ == '__main__':
    print problem_17()

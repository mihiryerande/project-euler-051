# Problem 51:
#     Prime Digit Replacements
#
# Description:
#     By replacing the 1st digit of the 2-digit number _3,
#       it turns out that six of the nine possible values: 13, 23, 43, 53, 73, and 83, are all prime.
#
#     By replacing the 3rd and 4th digits of 56__3 with the same digit,
#       this 5-digit number is the first example having seven primes among the ten generated numbers,
#       yielding the family:
#         56003, 56113, 56333, 56443, 56663, 56773, and 56993.
#     Consequently 56003, being the first member of this family, is the smallest prime with this property.
#
#     Find the smallest prime which,
#       by replacing part of the number (not necessarily adjacent digits) with the same digit,
#       is part of an eight prime value family.

from collections import defaultdict
from itertools import product
from math import floor, sqrt
from typing import List, Tuple

# Global variables to keep track of primes as they are found
PRIME_LIST = []
PRIME_SET = set()
HIGHEST_CHECKED = 1


def is_prime(x: int) -> bool:
    """
    Returns True iff `x` is prime.
    Keeps track of known primes up to highest `x` ever given to function, to avoid redundant calls.
    If a new `x` is out of range of numbers checked so far,
      figure out all results up to and including `x`, for future usage.

    Args:
        x (int): Integer

    Returns:
        (bool): True iff `x` is prime
    """
    global PRIME_LIST
    global PRIME_SET
    global HIGHEST_CHECKED

    if x < 2:
        # Negatives, 0, and 1 not considered prime
        return False
    else:
        if x > HIGHEST_CHECKED:
            # Not yet checked, so check all numbers until x (inclusive)
            for y in range(HIGHEST_CHECKED+1, x+1):
                include_y = True
                y_mid = floor(sqrt(y)) + 1
                i = 0
                while i < len(PRIME_LIST) and PRIME_LIST[i] < y_mid:
                    p = PRIME_LIST[i]
                    if y % p == 0:
                        include_y = False
                        break
                    i += 1
                if include_y:
                    PRIME_LIST.append(y)
                    PRIME_SET.add(y)
            HIGHEST_CHECKED = x
        return x in PRIME_SET


def main(n: int) -> Tuple[str, List[int]]:
    """
    Returns the first digit-family
      (set of natural numbers all matching a digit-template),
      having at least `n` prime members.
    Also returns the ordered list of those members.

    Args:
        n (int): Natural number in range [2, 10]

    Returns:
        (Tuple[str, List[int]]):
            Tuple of ...
              * String template for the digit-family
              * Prime members of the digit-family, as an ordered list

    Raises:
        AssertError: if incorrect args are given
    """
    # Maximum number of digit candidates is 10 (0 through 9)
    # n = 1 is trivial, as any prime would match this
    assert type(n) == int and 2 <= n <= 10

    # Idea:
    #     Iterate `d` upwards, considering numbers having `d` digits.
    #     Only need to consider primes within one such range at a time,
    #       as numbers of different digits can't be in the same digit-family.
    #
    #     Within that range, find all the primes.
    #     For each prime encountered,
    #       keep track of what digit-families it fits into,
    #       and also the sizes of those families.
    #
    #     Whenever a digit-family obtains `n` members,
    #       compare it against any previously seen family
    #       by their least elements.

    d = 0  # Size of numbers in consideration (as count of their digits)
    x = 2  # Numbers to prime-check
    while True:
        d += 1
        digit_families = defaultdict(lambda: [])

        # Find all the primes having `d` digits, and keep track of their families
        member_least = t_least = None
        while x < 10 ** d:
            if is_prime(x):
                # Count digits and occurrences in `x`,
                #   to figure out which digit-families contain `x`
                xs = str(x)
                digit_counts = defaultdict(lambda: 0)
                for c in xs:
                    digit_counts[c] += 1

                # Add the prime to any of the 10 relevant digit families
                # Figure out templates of digit-families by considering each digit in the number
                for digit, count in digit_counts.items():
                    # Optimization to avoid families where 'ones' digit is wild card,
                    #   since primes only end in 1, 3, 7, and 9 above 10
                    skip_ones = (n > 4 and xs[-1] == digit)
                    count = count-1 if skip_ones else count  # Don't consider the 'ones' digit to be replaceable

                    # Iterate through which of the occurrences of `digit` to be replaceable ('empty')
                    for empties in product([False, True], repeat=count):
                        # Optimization to avoid some families, due to pigeonholing with multiples of 3
                        if n > 7 and sum(empties) % 3 != 0:
                            continue

                        empties = list(empties)
                        if skip_ones:
                            empties.insert(0, False)

                        # Create the relevant template
                        xt = list(xs)
                        for i, c in enumerate(xt):
                            if c == digit and empties.pop():  # Popping from back, but doesn't really matter
                                xt[i] = '_'
                            else:
                                continue
                        xt = ''.join(xt)

                        # Add `x` to the digit-family defined by template `xt`
                        digit_families[xt].append(x)

                        # Check if this digit-family should be considered,
                        #   and compare with previous,
                        #   based on the least element of the families.
                        if len(digit_families[xt]) == n:
                            if member_least is None or digit_families[xt][0] < member_least:
                                member_least = digit_families[xt][0]
                                t_least = xt
                    else:
                        continue
            else:
                pass
            x += 1

        if t_least is not None:
            # Found at least one family having at least `n` members
            # Return such digit-family having the least member
            return t_least, digit_families[t_least]
        else:
            # No families had at least `n` members, so continue
            continue


if __name__ == '__main__':
    prime_family_size = int(input('Enter a natural number (2 ≤ n ≤ 10): '))
    prime_template, prime_family = main(prime_family_size)
    print('First prime family containing at least {} members:'.format(prime_family_size))
    print('  Template = {}'.format(prime_template))
    print('  Members:')
    for prime_family_member in prime_family:
        print('    {}'.format(prime_family_member))

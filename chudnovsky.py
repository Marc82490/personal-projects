# Author: Marc Zalik
# Date: 2020-10-15
# Description: Uses the Chudnovsky algorithm to compute an estimation of pi using of arbitrary precision. Credit to
#              Nick Craig-Wood for the algorithm: https://www.craig-wood.com/nick/articles/pi-chudnovsky/

import math
from decimal import Decimal, getcontext
import sys

def handle_exit(pi):
    """
    At program exit, write current value of pi to a file in the local directory.
    :param pi: The estimated value of pi at time of program ending.
    """
    print("Writing pi to file...")
    filename = "pi.txt"
    file = open(filename, 'w')
    file.write(str(pi))
    file.close()
    sys.exit()

def chudnvosky(precision):
    """
    Uses the Chudnovsky algorithm to quickly calculate an estimation of pi to arbitrary precision. Note that the last
    2 digits are not guaranteed to be accurate.
    :param precision: Determines the precision of the resulting estimation, and is used to determine how many times to
                      loop through the summation portion of the algorithm.
    """
    getcontext().prec = precision + 1   # Sets the precision of the decimal type variables
    k = 0
    # Algorithm computes ~14 digits of pi per loop, so only need to loop 1/14 as many times as the precision
    iterations = precision // 14
    # Initialize variables as decimal types
    a_sum = Decimal(0)
    b_sum = Decimal(0)
    numerator = Decimal(0)
    denominator = Decimal(0)

    for iter in range(iterations):
        try:
            numerator = Decimal(math.factorial(6 * k) * ((-1) ** k))
            denominator = Decimal(math.factorial(3 * k) * (math.factorial(k) ** 3) * ((640320) ** (3 * k)))
            a_k = Decimal(numerator / denominator)
            b_k = a_k * k
            a_sum += a_k
            b_sum += b_k
            k += 1
            # Print current status for long precisions
            if iter % 100 == 0:
                print("Loop:", iter)
        except KeyboardInterrupt:
            # Handle early stopping and still write the value of pi
            pi = combine(a_sum, b_sum)
            handle_exit(pi)

    pi = combine(a_sum, b_sum)
    # If program finishes completely, write the value of pi
    handle_exit(pi)

def combine(a, b):
    """
    Takes the A term and B term and combines them with the constant term to return the final estimated value of pi.
    :param a: The A term according to Craig-Wood version of Chudnovsky.
    :param b: The B term according to Craig-Wood version of Chudnovsky.
    :return: The final estimation of pi.
    """
    sum = Decimal(0)
    constant = Decimal(426880 * Decimal(10005).sqrt())
    sum = (13591409 * a) + (545140134 * b)
    pi = constant / sum
    return pi

if __name__ == "__main__":
    chudnvosky(20000)

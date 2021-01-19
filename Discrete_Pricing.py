###############################################################################
# Asset Pricing in Discrete Time
# Description: This file contains code to price single state processes
# Author: Pranay Gundam
###############################################################################

import Options

# This function calculates all the possible prices of the security over time.
# Future changes can be made to optimize time based on only the moment in time
# that is required. 
def pricingCalc(option):
    N = option.getMaturity()
    p, q, domain = option.domainCalc(N)
    rng = [0] * (N+1)

    if option.isSingleState():
        rng[N] = {state: option.finalEval(state[1]) for state in domain[N]}
        for n in range(N-1, -1, -1):
                rng[n] = {state : option.rollback1(p, q, n, state[1], rng, state[0]) for state in domain[n]}

    elif option.isDoubleState():
        rng[N] = {state: option.finalEval(state[1], state[2]) for state in domain[N]}
        for n in range(N-1, -1, -1):
                rng[n] = {state: option.rollback(p, q, n, state[1], rng, state[2], state[0]) for state in domain[n]}
    return rng





    
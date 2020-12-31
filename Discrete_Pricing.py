###############################################################################
# Asset Pricing in Discrete Time
# Description: This file contains code to price single state processes
# Author: Pranay Gundam
###############################################################################

import Options

# This function calculates all the possible prices of the security over time.
# Future changes can be made to optimize time based on only the moment in time
# that is required. 
def pricingCalcSingle(option, u, d, r, N, S_0, K):
    p, q, domain = option.domainCalc(u, d, r, S_0, N)
    rng = [0] * (N+1)

    if option.isSingleState():
        rng[N] = {s: option.finalEval(s) for s in domain[N]}
        for n in range(N-1, -1, -1):
            for s in domain[n]:
                rng[n] = {s : option.rollback1(u, d, r, p, q, n, s, rng) for s
                in domain[n]}

    elif option.isDoubleState():
        rng[N] = {(s,m): option.finalEval(s,m) for (s,m) in domain[N]}
        for n in range(N-1, -1, -1):
            for s in domain[n]:
                rng[n] = {(s,m): option.rollback(u, d, r, p, q, n, s, rng, m) 
                          for (s,m) in domain[n]}
    return rng





    
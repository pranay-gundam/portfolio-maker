###############################################################################
# Asset Pricing in Discrete Time
# Description: This file contains code to price single state processes
# Author: Pranay Gundam
###############################################################################

# Note for later: we can define classes for each option type and then
# do the generic functions like that


# In discrete time we have equations for the pricing of options that are
# recursive, and as such we have to calculate the possible stock prices at each
#  time.
def domainCalc(u, d, r, S_0, N):
    p = ((1+r)-d)/(u-d)
    q = (u - (1+r))/(u-d)

    domain = [0] * (N+1)
    domain[0] = set( [S_0] )
    for n in range(N):
        domain[n+1] = set()
        for s in domain[n]:
            domain[n+1].add(u*s)
            domain[n+1].add(d*s)
    return p, q, domain

# Generic function for all the pricing methods

def valfunc(u, d, r, p, q, n, s, rng, K, otype):
    if otype == "Euro":
        return euroOption(u,d,r,p,q,n,s,rng)
    elif otype == "amerCall":
        return amerCall(u, d, r, p, q, n, s, rng, K)
    elif otype == "amerPut":
        return amerPut(u, d, r, p, q, n, s, rng, K)
    elif otype == "amerStraddle":
        return amerStraddle(u, d, r, p, q, n, s, rng, K)
    return 0

# Pricing all european options given a stock price and time
def euroOption(u, d, r, p, q, n, s, rng):
    return (p*rng[n+1][u*s] + q*rng[n+1][d*s])/(1+r)

# Pricing an american call option at a given stock price and time
def amerCall(u, d, r, p, q, n, s, rng, K):
    rnmValue = (p*rng[n+1][u*s] + q*rng[n+1][d*s])/(1+r)
    currval = max(s-K, 0)
    return [rnmValue if rnmValue > currval else currval]

# Pricing an american put option at a given stock price and time
def amerPut(u, d, r, p, q, n, s, rng, K):
    rnmValue = (p*rng[n+1][u*s] + q*rng[n+1][d*s])/(1+r)
    currval = max(K-s, 0)
    return [rnmValue if rnmValue > currval else currval]

# Pricing an american stadle option at a given stock price and time
def amerStraddle(u, d, r, p, q, n, s, rng, K):
    rnmValue = (p*rng[n+1][u*s] + q*rng[n+1][d*s])/(1+r)
    return [rnmValue if rnmValue > abs(K-s) else abs(K-s)]


# This function calculates all the possible prices of the security over time.
# Future changes can be made to optimize time based on only the moment in time
# that is required. 
def pricingCalcSingle(option, u, d, r, N, S_0, K):
    p, q, domain = domainCalc(u, d, r, S_0, N)
    rng = [0] * (N+1)

    if option == "Euro Put":
        rng[N] = {s: ((K-s) if (K-s) > 0 else 0) for s in domain[N]}
        for n in range(N-1, -1, -1):
            for s in domain[n]:
                rng[n] = {s : euroOption(u, d, r, p, q, n, s, rng) for s in 
                            domain[n]}
    elif option == "Euro Call":
        rng[N] = {s: ((s-K) if (s-K) > 0 else 0) for s in domain[N]}
        for n in range(N-1, -1, -1):
            for s in domain[n]:
                rng[n] = {s : euroOption(u, d, r, p, q, n, s, rng) for s in 
                            domain[n]}
    elif option == "Euro Straddle":
        rng[N] = {s: abs(s-K) for s in domain[N]}
        for n in range(N-1, -1, -1):
            for s in domain[n]:
                rng[n] = {s : euroOption(u, d, r, p, q, n, s, rng) for s in 
                            domain[n]}
    elif option == "Amer Put":
        rng[N] = {s: ((K-s) if (K-s) > 0 else 0) for s in domain[N]}
        for n in range(N-1, -1, -1):
            for s in domain[n]:
                rng[n] = {s : amerPut(u, d, r, p, q, n, s, rng, K) for s in 
                            domain[n]}
    elif option == "Amer Call":
        rng[N] = {s: ((s-K) if (s-K) > 0 else 0) for s in domain[N]}
        for n in range(N-1, -1, -1):
            for s in domain[n]:
                rng[n] = {s : amerCall(u, d, r, p, q, n, s, rng, K) for s in 
                            domain[n]}
    elif option == "Amer Straddle":
        rng[N] = {s: abs(s-K) for s in domain[N]}
        for n in range(N-1, -1, -1):
            for s in domain[n]:
                rng[n] = {s : amerStraddle(u, d, r, p, q, n, s, rng, K) for s in 
                            domain[n]}






    
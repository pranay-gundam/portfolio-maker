###############################################################################
# Asset Pricing in Discrete Time
# Description: This file contains code to price single state processes
# Author: Pranay Gundam
###############################################################################
import Discrete_Single_State



# Note for later: can maybe generalize this to make it to include rebates. Where
# the pricing I have right now is just knock-in/knock-out option that has a
# rebate of 0.

# In discrete time we can calculate the domain for the possible stock prices. 
# Since, however, we are using a state process that keeps track of two things,
# there are different domains for the up and down options. This one keeps a 
# running track of the min stock price.
def downDomain(u, d, r, S_0, N):
    p = ((1+r)-d)/(u-d)
    q = (u - (1+r))/(u-d)

    domain = [0] * (N+1)
    domain[0] = set( [(S_0, S_0)] )
    for n in range(N):
        domain[n+1] = set()
        for s in domain[n]:
            domain[n+1].add( (u*s, m) for (s,m) in domain[n] )
            domain[n+1].add( (d*s, min(d*s, m)) for (s,m) in domain[n] )
    return p, q, domain

# In discrete time we can calculate the domain for the possible stock prices. 
# Since, however, we are using a state process that keeps track of two things,
# there are different domains for the up and down options. This one keeps a 
# running track of the max stock price.
def upDomain(u, d, r, S_0, N):
    p = ((1+r)-d)/(u-d)
    q = (u - (1+r))/(u-d)

    domain = [0] * (N+1)
    domain[0] = set( [(S_0, S_0)] )
    for n in range(N):
        domain[n+1] = set()
        for s in domain[n]:
            domain[n+1].add( (u*s, max(u*s, m)) for (s,m) in domain[n] )
            domain[n+1].add( (d*s, m) for (s,m) in domain[n] )
    return p, q, domain



# All of the function below are the rollback operators that are used at each
# step of evaluation.
def downAndOut(u, d, r, p, q, n, s, rng, m, D, K):
    rnmValue = (p*rng[n+1][(u*s, m)] + q*rng[n+1][(d*s, min(d*s, m))])/(1+r)
    return rnmValue if m <= D else 0

def upAndOut(u, d, r, p, q, n, s, rng, m, U, K):
    rnmValue = (p*rng[n+1][(u*s, max(u*s,m))] + q*rng[n+1][(d*s, m)])/(1+r)
    return rnmValue if m >= U else 0

def downAndIn(u, d, r, p, q, n, s, rng, m, D, K):
    rnmValue = (p*rng[n+1][(u*s, m)] + q*rng[n+1][(d*s, min(d*s, m))])/(1+r)
    return 0 if m > D else rnmValue

def upAndIn(u, d, r, p, q, n, s, rng, m, U, K):
    rnmValue = (p*rng[n+1][(u*s, max(u*s,m))] + q*rng[n+1][(d*s, m)])/(1+r)
    return 0 if m < U else rnmValue


def pricingCalcBarrier(option, u, d, r, N, S_0, K):
    return 0
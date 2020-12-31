###############################################################################
# Asset Pricing in Discrete Time
# Description: This file contains code that defines each type of option as a
# class. This is done so that generalization is easier later down the road and 
# so that implementing the app is easier as well.
# Author: Pranay Gundam
###############################################################################

# In discrete time we have equations for the pricing of options that are
# recursive, and as such we have to calculate the possible stock prices at each
#  time.
def domainCalc_1(u, d, r, S_0, N):
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


# In discrete time we can calculate the domain for the possible stock prices. 
# Since, however, we are using a state process that keeps track of two things,
# there are different domains for the up and down options. This one keeps a 
# running track of the min stock price.
def downDomain_2(u, d, r, S_0, N):
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
def upDomain_2(u, d, r, S_0, N):
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


# This super class is just here in case we may need it in our implementation
# later on at some point
class Option(object):
    def __init__(self):
        pass

# A european put is an option that give the owner the right to exercise at a 
# certain point (that we denote as the exercise time). The value of a european 
# put at its excersize time is typically (K-S_N)^+ where S_N is the value of 
# underlying at the exercise time and K is some predetermined "strike price".
class EuroPut(Option):
    def __init__(self, K, N):
        self.strike = K
        self.maturity = N
    
    def getStrike(self):
        return self.strike

    def getMaturity(self):
        return self.maturity
    
    def isSingleState(self):
        return True
    
    def isDoubleState(self):
        return False

    def domainCalc(u, d, r, S_0, N):
        return domainCalc_1(u, d, r, S_0, N)

    def rollback1(u, d, r, p, q, n, s, rng):
        return (p*rng[n+1][u*s] + q*rng[n+1][d*s])/(1+r)

    def rollback2d(self, u, d, r, p, q, n, s, rng, m):
        return (p*rng[n+1][(u*s,m)] + q*rng[n+1][(d*s,min(d*s,m))])/(1+r)

    def rollback2u(self, u, d, r, p, q, n, s, rng, m):
        return (p*rng[n+1][(u*s,max(u*s,m))] + q*rng[n+1][(d*s,m)])/(1+r)

    def finalEval(self, s):
        return self.getStrike()-s if self.getStrike()-s > 0 else 0

# A european call is an option that give the owner the right to exercise at a 
# certain point (that we denote as the exercise time). The value of a european 
# call at its excersize time is typically (S_N-K)^+ where S_N is the value of 
# underlying at the exercise time and K is some predetermined "strike price".
class EuroCall(Option):
    def __init__(self, K, N):
        self.strike = K
        self.maturity = N
    
    def getStrike(self):
        return self.strike

    def getMaturity(self):
        return self.maturity

    def isSingleState(self):
        return True
    
    def isDoubleState(self):
        return False

    def domainCalc(u, d, r, S_0, N):
        return domainCalc_1(u, d, r, S_0, N)

    def rollback1(u, d, r, p, q, n, s, rng):
        return (p*rng[n+1][u*s] + q*rng[n+1][d*s])/(1+r)
    
    def rollback2d(self, u, d, r, p, q, n, s, rng, m):
        return (p*rng[n+1][(u*s,m)] + q*rng[n+1][(d*s,min(d*s,m))])/(1+r)

    def rollback2u(self, u, d, r, p, q, n, s, rng, m):
        return (p*rng[n+1][(u*s,max(u*s,m))] + q*rng[n+1][(d*s,m)])/(1+r)

    def finalEval(self, s):
        return s-self.getStrike() if s-self.getStrike() > 0 else 0

# A european straddle is an option that give the owner the right to exercise at a 
# certain point (that we denote as the exercise time). The value of a european 
# straddle at its excersize time is typically |S_N-K| where S_N is the value of 
# underlying at the exercise time and K is some predetermined "strike price".
class EuroStraddle(Option):
    def __init__(self, K, N):
        self.strike = K
        self.maturity = N
    
    def getStrike(self):
        return self.strike

    def getMaturity(self):
        return self.maturity

    def isSingleState(self):
        return True
    
    def isDoubleState(self):
        return False

    def domainCalc(u, d, r, S_0, N):
        return domainCalc_1(u, d, r, S_0, N)

    def rollback1(u, d, r, p, q, n, s, rng):
        return (p*rng[n+1][u*s] + q*rng[n+1][d*s])/(1+r)

    def rollback2d(self, u, d, r, p, q, n, s, rng, m):
        return (p*rng[n+1][(u*s,m)] + q*rng[n+1][(d*s,min(d*s,m))])/(1+r)

    def rollback2u(self, u, d, r, p, q, n, s, rng, m):
        return (p*rng[n+1][(u*s,max(u*s,m))] + q*rng[n+1][(d*s,m)])/(1+r)
        
    def finalEval(self, s):
        return abs(s - self.getStrike())


class AmerPut(Option):
    def __init__(self, K, N):
        self.strike = K
        self.maturity = N
    
    def getStrike(self):
        return self.strike

    def getMaturity(self):
        return self.maturity

    def isSingleState(self):
        return True
    
    def isDoubleState(self):
        return False

    def domainCalc(u, d, r, S_0, N):
        return domainCalc_1(u, d, r, S_0, N)

    def rollback1(self, u, d, r, p, q, n, s, rng):
        rnmValue = (p*rng[n+1][u*s] + q*rng[n+1][d*s])/(1+r)
        currval = max(self.getStrike()-s, 0)
        return rnmValue if rnmValue > currval else currval

    def rollback2d(self, u, d, r, p, q, n, s, rng, m):
        rnmValue = (p*rng[n+1][(u*s,m)] + q*rng[n+1][(d*s,min(d*s,m))])/(1+r)
        currval = max(self.getStrike() - s, 0)
        return rnmValue if rnmValue > currval else currval
    
    def rollback2u(self, u, d, r, p, q, n, s, rng, m):
        rnmValue = (p*rng[n+1][(u*s,max(u*s,m))] + q*rng[n+1][(d*s,m)])/(1+r)
        currval = max(self.getStrike() - s, 0)
        return rnmValue if rnmValue > currval else currval

    def currEval(self, s):
        return self.getStrike() - s if self.getStrike() - s  > 0 else 0
    
    def finalEval(self, s):
        return self.getStrike() - s if self.getStrike() - s  > 0 else 0


class AmerCall(Option):
    def __init__(self, K, N):
        self.strike = K
        self.maturity = N
    
    def getStrike(self):
        return self.strike

    def getMaturity(self):
        return self.maturity

    def isSingleState(self):
        return True
    
    def isDoubleState(self):
        return False

    def domainCalc(u, d, r, S_0, N):
        return domainCalc_1(u, d, r, S_0, N)

    def rollback1(self, u, d, r, p, q, n, s, rng):
        rnmValue = (p*rng[n+1][u*s] + q*rng[n+1][d*s])/(1+r)
        currval = max(s-self.getStrike(), 0)
        return rnmValue if rnmValue > currval else currval

    def rollback2d(self, u, d, r, p, q, n, s, rng, m):
        rnmValue = (p*rng[n+1][(u*s,m)] + q*rng[n+1][(d*s,min(d*s,m))])/(1+r)
        currval = max(s-self.getStrike(), 0)
        return rnmValue if rnmValue > currval else currval

    def rollback2u(self, u, d, r, p, q, n, s, rng, m):
        rnmValue = (p*rng[n+1][(u*s,max(u*s, m))] + q*rng[n+1][(d*s,m)])/(1+r)
        currval = max(s-self.getStrike(), 0)
        return rnmValue if rnmValue > currval else currval

    def currEval(self, s):
        return s - self.getStrike() if s - self.getStrike() > 0 else 0
    
    def finalEval(self, s):
        return s - self.getStrike() if s - self.getStrike() > 0 else 0


class AmerStraddle(Option):
    def __init__(self, K, N):
        self.strike = K
        self.maturity = N
    
    def getStrike(self):
        return self.strike

    def getMaturity(self):
        return self.maturity

    def isSingleState(self):
        return True
    
    def isDoubleState(self):
        return False

    def domainCalc(u, d, r, S_0, N):
        return domainCalc_1(u, d, r, S_0, N)

    def rollback1(self, u, d, r, p, q, n, s, rng):
        rnmValue = (p*rng[n+1][u*s] + q*rng[n+1][d*s])/(1+r)
        return rnmValue if rnmValue > abs(self.getStrike()-s) else abs(self.getStrike()-s)
    
    def rollback2d(self, u, d, r, p, q, n, s, rng, m):
        rnmValue = (p*rng[n+1][(u*s,m)] + q*rng[n+1][(d*s,min(d*s,m))])/(1+r)
        return rnmValue if rnmValue > abs(self.getStrike()-s) else abs(self.getStrike()-s)

    def rollback2u(self, u, d, r, p, q, n, s, rng, m):
        rnmValue = (p*rng[n+1][(u*s,max(u*s, m))] + q*rng[n+1][(d*s,m)])/(1+r)
        return rnmValue if rnmValue > abs(self.getStrike()-s) else abs(self.getStrike()-s)

    def currEval(self, s):
        return abs(s - self.getStrike())
    
    def finalEval(self, s):
        return abs(s - self.getStrike())


# Note for later: can maybe generalize to make it to include rebates. Where
# the pricing I have right now is just knock-in/knock-out option that has a
# rebate of 0.

class Down_Out_Barrier(Option):
    def __init__(self, underlying, D):
        self.underlying = underlying
        self.downBarrier = D
    
    def getStrike(self):
        return self.underlying.getStrike()
    
    def getMaturity(self):
        return self.underlying.getMaturity()

    def getBarrier(self):
        return self.downBarrier

    def isSingleState(self):
        return False
    
    def isDoubleState(self):
        return True

    def domainCalc(u, d, r, S_0, N):
        return downDomain_2(u, d, r, S_0, N)

    def rollback(self, u, d, r, p, q, n, s, rng, m):
        rnmValue = self.underlying.rollback2d(u, d, r, p, q, n, s, rng, m)
        return rnmValue if m >= self.getBarrier else 0

    def currEval(self, s):
        return self.underlying.currEval(s)
    
    def finalEval(self, s, m):
        return self.underlying.finalEval(s) if m >= self.getBarrier else 0


class Up_Out_Barrier(Option):
    def __init__(self, underlying, U):
        self.underlying = underlying
        self.upBarrier = U
    
    def getStrike(self):
        return self.underlying.getStrike()
    
    def getMaturity(self):
        return self.underlying.getMaturity()

    def getBarrier(self):
        return self.upBarrier

    def isSingleState(self):
        return False
    
    def isDoubleState(self):
        return True

    def domainCalc(u, d, r, S_0, N):
        return upDomain_2(u, d, r, S_0, N)

    def rollback(self, u, d, r, p, q, n, s, rng, m):
        rnmValue = self.underlying.rollback2u(u, d, r, p, q, n, s, rng, m)
        return rnmValue if m <= self.getBarrier else 0

    def currEval(self, s):
        return self.underlying.currEval(s)
    
    def finalEval(self, s, m):
        return self.underlying.finalEval(s) if m <= self.getBarrier else 0


class Down_In_Barrier(Option):
    def __init__(self, underlying, D):
        self.underlying = underlying
        self.downBarrier = D
    
    def getStrike(self):
        return self.underlying.getStrike()
    
    def getMaturity(self):
        return self.underlying.getMaturity()

    def getBarrier(self):
        return self.downBarrier

    def isSingleState(self):
        return False
    
    def isDoubleState(self):
        return True

    def domainCalc(u, d, r, S_0, N):
        return downDomain_2(u, d, r, S_0, N)

    def rollback(self, u, d, r, p, q, n, s, rng, m):
        rnmValue = self.underlying.rollback2d(u, d, r, p, q, n, s, rng, m)
        return rnmValue if m <= self.getBarrier else 0

    def currEval(self, s):
        return self.underlying.currEval(s)
    
    def finalEval(self, s, m):
        return self.underlying.finalEval(s) if m <= self.getBarrier else 0


class Up_In_Barrier(Option):
    def __init__(self, underlying, U):
        self.underlying = underlying
        self.upBarrier = U
    
    def getStrike(self):
        return self.underlying.getStrike()
    
    def getMaturity(self):
        return self.underlying.getMaturity()

    def getBarrier(self):
        return self.upBarrier

    def isSingleState(self):
        return False
    
    def isDoubleState(self):
        return True

    def domainCalc(u, d, r, S_0, N):
        return upDomain_2(u, d, r, S_0, N)

    def rollback(self, u, d, r, p, q, n, s, rng, m):
        rnmValue = self.underlying.rollback2u(u, d, r, p, q, n, s, rng, m)
        return rnmValue if m >= self.getBarrier else 0

    def currEval(self, s):
        return self.underlying.currEval(s)
    
    def finalEval(self, s, m):
        return self.underlying.finalEval(s) if m >= self.getBarrier else 0

          
###############################################################################
# Asset Pricing in Discrete Time
# Description: This file contains code that defines each type of option as a
# class. This is done so that generalization is easier later down the road and 
# so that implementing the app is easier as well.
# Author: Pranay Gundam
###############################################################################

# Create a bank with an interest rate that is represented as an array so that
# we can have a different interest at each time n.
class Bank(object):
    def __init__(self, r):
        self.interest = r
        self.finTime = len(r)
    
    def __str__(self):
        return f"BANK\nFinal Time: {self.finTime}\nInterest Rate: {self.interest}"

    def getFinTime(self):
        return self.finTime

    def getInterest(self):
        return self.interest

    def getMaturity(self):
        return self.finTime

    def isSame(self, other):
        if not isinstance(self, other): return False
        if (self.getFinTime() == other.getFinTime() and 
            self.getInterest() == other.getInterest()):
            return True
        return False

    def getInterestn(self, n):
        if (n >= self.getFinTime()):
            print("our interest array is not long enough\n")
            return
        else:
            return self.interest[n]

# Basic stock with an initial price and up and down factors that can change
# based on n.
class Stock(object):
    def __init__(self, u, d, S_0):
        self.price0 = S_0
        self.up = u
        self.down = d
        # add safety check here that u and d are the same length
    
    def __str__(self):
        return f"STOCK\nInitial Price: {self.price0}\nUp Factors: {self.up}\nDownFactors: {self.down}"

    def getUpFactor(self):
        return self.up
    
    def getDownFactor(self):
        return self.down

    def getUpFactorn(self, n):
        return self.up[n]
    
    def getDownFactorn(self, n):
        return self.down[n]

    def getInitPrice(self):
        return self.price0
    
    def getMaturity(self):
        return len(self.getUpFactor())

    def isSame(self, other):
        if not isinstance(self, other): return False
        init1 = self.getInitPrice()
        init2 = other.getInitPrice()
        u1 = self.getUpFactor()
        d1 = self.getDownFactor()
        u2 = other.getUpFactor()
        d2 = other.getDownFactor()
        if init1 == init2 and u1 == u2 and d1 == d2:
            return True
        return False

    def getPrice(self, event):
        final = self.getInitPrice()
        for i in range(len(event)):
            final = (final*self.getUpFactorn(i) if event[i] == "u" 
                     else final*self.getDownFactorn(i))
        return final

# In discrete time we have equations for the pricing of options that are
# recursive, and as such we have to calculate the possible stock prices at each
#  time.
def domainCalc_1(bank, asset, N):
    d = asset.getDownFactor()
    u = asset.getUpFactor()
    r = bank.getInterest()
    p = [((1+r[i]) - d[i])/(u[i]-d[i]) for i in range(len(r))]
    q = [(u[i] - (1+r[i]))/(u[i]-d[i]) for i in range(len(r))]

    domain = [0] * (N+1)
    domain[0] = set([("", asset.getInitPrice())] )
    for n in range(N):
        domain[n+1] = set()
        for prev in domain[n]:
            domain[n+1].add(("u" + prev[0], u[n]*prev[1]))
            domain[n+1].add((prev[0] + "d", d[n]*prev[1]))
    return p, q, domain


# In discrete time we can calculate the domain for the possible stock prices. 
# Since, however, we are using a state process that keeps track of two things,
# there are different domains for the up and down options. This one keeps a 
# running track of the min stock price.
def downDomain_2(bank, asset, N):
    d = asset.getDownFactor()
    u = asset.getUpFactor()
    r = bank.getInterest()
    p = [((1+r[i]) - d[i])/(u[i]-d[i]) for i in range(len(r))]
    q = [(u[i] - (1+r[i]))/(u[i]-d[i]) for i in range(len(r))]

    domain = [0] * (N+1)
    domain[0] = set( [("", asset.getInitPrice(), asset.getInitPrice())] )
    for n in range(N):
        domain[n+1] = set()
        for prev in domain[n]:
            domain[n+1].add( ("u" + prev[0], u[n]*prev[1], prev[2]))
            domain[n+1].add( (prev[0] + "d", d[n]*prev[1], min(d[n]*prev[1], prev[2])))
    return p, q, domain

# In discrete time we can calculate the domain for the possible stock prices. 
# Since, however, we are using a state process that keeps track of two things,
# there are different domains for the up and down options. This one keeps a 
# running track of the max stock price.
def upDomain_2(bank, asset, N):
    d = asset.getDownFactor()
    u = asset.getUpFactor()
    r = bank.getInterest()
    p = [((1+r[i]) - d[i])/(u[i]-d[i]) for i in range(len(r))]
    q = [(u[i] - (1+r[i]))/(u[i]-d[i]) for i in range(len(r))]


    domain = [0] * (N+1)
    domain[0] = set( [("", asset.getInitPrice(), asset.getInitPrice())] )
    for n in range(N):
        domain[n+1] = set()
        for prev in domain[n]:
            domain[n+1].add( ("u" + prev[0], u[n]*prev[1], max(u[n]*prev[1], prev[2])))
            domain[n+1].add( (prev[0] + "d", d[n]*prev[1], prev[2]) )
    return p, q, domain


# This super class is just here in case we may need it in our implementation
# later on at some point
class Option(object):
    pass

# A european put is an option that give the owner the right to exercise at a 
# certain point (that we denote as the exercise time). The value of a european 
# put at its excersize time is typically (K-S_N)^+ where S_N is the value of 
# underlying at the exercise time and K is some predetermined "strike price".
class EuroPut(Option):
    def __init__(self, K, N, underlying, bank):
        self.strike = K
        self.maturity = N
        self.underlying = underlying
        self.bank = bank
    
    def __str__(self):
        return f"EUROPEAN PUT\nStrike Price: {self.strike}\nMaturity: {self.maturity}\nBank: {str(self.bank)}\nUnderlying: {str(self.underlying)}"

    def getStrike(self):
        return self.strike

    def getMaturity(self):
        return self.maturity
    
    def isSingleState(self):
        return True
    
    def isDoubleState(self):
        return False

    def getUnderlying(self):
        return self.underlying
    
    def getBank(self):
        return self.bank

    def isSame(self, other):
        if not isinstance(self, other): return False
        bank1 = self.getBank()
        bank2 = other.getBank()
        if self.getStrike() != other.getStrike(): return False
        if self.getMaturity() != other.getMaturity(): return False
        if not bank1.isSame(bank2): return False
        if not self.getUnderlying().isSame(other.getUnderlying()): return False
        return True

    def domainCalc(self, N):
        return domainCalc_1(self.getBank(), self.getUnderlying(), N)

    def rollback1(self, p, q, n, s, rng, state):
        return (p[n]*rng[n+1][("u"+state, self.getUnderlying().getUpFactorn(n)*s)] + 
                q[n]*rng[n+1][(state+"d", self.getUnderlying().getDownFactorn(n)*s)])/(1+
                self.getBank().getInterestn(n))

    def rollback2d(self, p, q, n, s, rng, m, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactor(n)
        r = self.getBank().getInterestn(n)
        return (p[n]*rng[n+1][("u"+state,u*s,m)] + q[n]*rng[n+1][(state+"d",d*s,min(d*s,m))])/(1+r)

    def rollback2u(self, p, q, n, s, rng, m, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactor(n)
        r = self.getBank().getInterestn(n)
        return (p[n]*rng[n+1][("u"+state,u*s,max(u*s,m))] + q[n]*rng[n+1][(state+"d",d*s,m)])/(1+r)

    def finalEval(self, s):
        return self.getStrike()-s if self.getStrike()-s > 0 else 0

# A european call is an option that give the owner the right to exercise at a 
# certain point (that we denote as the exercise time). The value of a european 
# call at its excersize time is typically (S_N-K)^+ where S_N is the value of 
# underlying at the exercise time and K is some predetermined "strike price".
class EuroCall(Option):
    def __init__(self, K, N, underlying, bank):
        self.strike = K
        self.maturity = N
        self.underlying = underlying
        self.bank = bank

    def __str__(self):
        return f"EUROPEAN CALL\nStrike Price: {self.strike}\nMaturity: {self.maturity}\nBank: {str(self.bank)}\nUnderlying: {str(self.underlying)}"

    def getUnderlying(self):
        return self.underlying
    
    def getBank(self):
        return self.bank

    def getStrike(self):
        return self.strike

    def getMaturity(self):
        return self.maturity

    def isSingleState(self):
        return True
    
    def isDoubleState(self):
        return False

    def isSame(self, other):
        if not isinstance(self, other): return False
        bank1 = self.getBank()
        bank2 = other.getBank()
        if self.getStrike() != other.getStrike(): return False
        if self.getMaturity() != other.getMaturity(): return False
        if not bank1.isSame(bank2): return False
        if not self.getUnderlying().isSame(other.getUnderlying()): return False
        return True

    def domainCalc(self, N):
        return domainCalc_1(self.getBank(), self.getUnderlying(), N)

    def rollback1(self, p, q, n, s, rng, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)
        return (p[n]*rng[n+1][("u"+state,u*s)] + q[n]*rng[n+1][(state+"d",d*s)])/(1+r)
    
    def rollback2d(self, p, q, n, s, rng, m, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)
        return (p[n]*rng[n+1][("u"+state,u*s,m)] + q[n]*rng[n+1][(state+"d",d*s,min(d*s,m))])/(1+r)

    def rollback2u(self, u, d, r, p, q, n, s, rng, m, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)
        return (p[n]*rng[n+1][("u"+state,u*s,max(u*s,m))] + q[n]*rng[n+1][(state+"d",d*s,m)])/(1+r)

    def finalEval(self, s):
        return s-self.getStrike() if s-self.getStrike() > 0 else 0

# A european straddle is an option that give the owner the right to exercise at a 
# certain point (that we denote as the exercise time). The value of a european 
# straddle at its excersize time is typically |S_N-K| where S_N is the value of 
# underlying at the exercise time and K is some predetermined "strike price".
class EuroStraddle(Option):
    def __init__(self, K, N, underlying, bank):
        self.strike = K
        self.maturity = N
        self.underlying = underlying
        self.bank = bank
    
    def __str__(self):
        return f"EUROPEAN STRADDLE\nStrike Price: {self.strike}\nMaturity: {self.maturity}\nBank: {str(self.bank)}\nUnderlying: {str(self.underlying)}"

    def getUnderlying(self):
        return self.underlying
    
    def getBank(self):
        return self.bank
    
    def getStrike(self):
        return self.strike

    def getMaturity(self):
        return self.maturity

    def isSingleState(self):
        return True
    
    def isDoubleState(self):
        return False

    def isSame(self, other):
        if not isinstance(self, other): return False
        bank1 = self.getBank()
        bank2 = other.getBank()
        if self.getStrike() != other.getStrike(): return False
        if self.getMaturity() != other.getMaturity(): return False
        if not bank1.isSame(bank2): return False
        if not self.getUnderlying().isSame(other.getUnderlying()): return False
        return True

    def domainCalc(self, N):
        return domainCalc_1(self.getBank(), self.getUnderlying(), N)

    def rollback1(self, p, q, n, s, rng, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)
        return (p[n]*rng[n+1][("u"+state,u*s)] + q[n]*rng[n+1][(state+"d",d*s)])/(1+r)
    
    def rollback2d(self, p, q, n, s, rng, m, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)
        return (p[n]*rng[n+1][("u"+state,u*s,m)] + q[n]*rng[n+1][(state+"d",d*s,min(d*s,m))])/(1+r)

    def rollback2u(self, u, d, r, p, q, n, s, rng, m, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)
        return (p[n]*rng[n+1][("u"+state,u*s,max(u*s,m))] + q[n]*rng[n+1][(state+"d",d*s,m)])/(1+r)
        
    def finalEval(self, s):
        return abs(s - self.getStrike())


class AmerPut(Option):
    def __init__(self, K, N, underlying, bank):
        self.strike = K
        self.maturity = N
        self.underlying = underlying
        self.bank = bank

    def __str__(self):
        return f"AMERICAN PUT\nStrike Price: {self.strike}\nMaturity: {self.maturity}\nBank: {str(self.bank)}\nUnderlying: {str(self.underlying)}"

    def getUnderlying(self):
        return self.underlying

    def getBank(self):
        return self.bank

    def getStrike(self):
        return self.strike

    def getMaturity(self):
        return self.maturity

    def isSingleState(self):
        return True
    
    def isDoubleState(self):
        return False

    def isSame(self, other):
        if not isinstance(self, other): return False
        bank1 = self.getBank()
        bank2 = other.getBank()
        if self.getStrike() != other.getStrike(): return False
        if self.getMaturity() != other.getMaturity(): return False
        if not bank1.isSame(bank2): return False
        if not self.getUnderlying().isSame(other.getUnderlying()): return False
        return True

    def domainCalc(self, N):
        return domainCalc_1(self.getBank(), self.getUnderlying(), N)

    def rollback1(self, p, q, n, s, rng, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)

        rnmValue = (p[n]*rng[n+1][("u"+state,u*s)] + q[n]*rng[n+1][(state+"d",d*s)])/(1+r)
        currval = max(self.getStrike()-s, 0)
        return rnmValue if rnmValue > currval else currval

    def rollback2d(self, p, q, n, s, rng, m, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)

        rnmValue = (p[n]*rng[n+1][("u"+state,u*s,m)] + q[n]*rng[n+1][(state+"d",d*s,min(d*s,m))])/(1+r)
        currval = max(self.getStrike() - s, 0)
        return rnmValue if rnmValue > currval else currval
    
    def rollback2u(self, u, d, r, p, q, n, s, rng, m, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)

        rnmValue = (p[n]*rng[n+1][("u"+state,u*s,max(u*s,m))] + q[n]*rng[n+1][(state+"d",d*s,m)])/(1+r)
        currval = max(self.getStrike() - s, 0)
        return rnmValue if rnmValue > currval else currval

    def currEval(self, s):
        return self.getStrike() - s if self.getStrike() - s  > 0 else 0
    
    def finalEval(self, s):
        return self.getStrike() - s if self.getStrike() - s  > 0 else 0


class AmerCall(Option):
    def __init__(self, K, N, underlying, bank):
        self.strike = K
        self.maturity = N
        self.underlying = underlying
        self.bank = bank

    def __str__(self):
        return f"AMERICAN CALL\nStrike Price: {self.strike}\nMaturity: {self.maturity}\nBank: {str(self.bank)}\nUnderlying: {str(self.underlying)}"

    def getUnderlying(self):
        return self.underlying

    def getBank(self):
        return self.bank

    def getStrike(self):
        return self.strike

    def getMaturity(self):
        return self.maturity

    def isSingleState(self):
        return True
    
    def isDoubleState(self):
        return False

    def isSame(self, other):
        if not isinstance(self, other): return False
        bank1 = self.getBank()
        bank2 = other.getBank()
        if self.getStrike() != other.getStrike(): return False
        if self.getMaturity() != other.getMaturity(): return False
        if not bank1.isSame(bank2): return False
        if not self.getUnderlying().isSame(other.getUnderlying()): return False
        return True

    def domainCalc(self, N):
        return domainCalc_1(self.getBank(), self.getUnderlying(), N)

    def rollback1(self, p, q, n, s, rng, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)

        rnmValue = (p[n]*rng[n+1][("u"+state,u*s)] + q[n]*rng[n+1][(state+"d",d*s)])/(1+r)
        currval = max(s-self.getStrike(), 0)
        return rnmValue if rnmValue > currval else currval

    def rollback2d(self, p, q, n, s, rng, m, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)

        rnmValue = (p[n]*rng[n+1][("u"+state,u*s,m)] + q[n]*rng[n+1][(state+"d",d*s,min(d*s,m))])/(1+r)
        currval = max(s-self.getStrike(), 0)
        return rnmValue if rnmValue > currval else currval

    def rollback2u(self, p, q, n, s, rng, m, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)

        rnmValue = (p[n]*rng[n+1][("u"+state,u*s,max(u*s,m))] + q[n]*rng[n+1][(state+"d",d*s,m)])/(1+r)
        currval = max(s-self.getStrike(), 0)
        return rnmValue if rnmValue > currval else currval

    def currEval(self, s):
        return s - self.getStrike() if s - self.getStrike() > 0 else 0
    
    def finalEval(self, s):
        return s - self.getStrike() if s - self.getStrike() > 0 else 0


class AmerStraddle(Option):
    def __init__(self, K, N, underlying, bank):
        self.strike = K
        self.maturity = N
        self.underlying = underlying
        self.bank = bank

    def __str__(self):
        return f"AMERICAN STRADDLE\nStrike Price: {self.strike}\nMaturity: {self.maturity}\nBank: {str(self.bank)}\nUnderlying: {str(self.underlying)}"

    def getUnderlying(self):
        return self.underlying

    def getBank(self):
        return self.bank

    def getStrike(self):
        return self.strike

    def getMaturity(self):
        return self.maturity

    def isSingleState(self):
        return True
    
    def isDoubleState(self):
        return False

    def isSame(self, other):
        if not isinstance(self, other): return False
        bank1 = self.getBank()
        bank2 = other.getBank()
        if self.getStrike() != other.getStrike(): return False
        if self.getMaturity() != other.getMaturity(): return False
        if not bank1.isSame(bank2): return False
        if not self.getUnderlying().isSame(other.getUnderlying()): return False
        return True

    def domainCalc(self, N):
        return domainCalc_1(self.getBank(), self.getUnderlying(), N)

    def rollback1(self, p, q, n, s, rng, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)

        rnmValue = (p[n]*rng[n+1][("u"+state,u*s)] + q[n]*rng[n+1][(state+"d",d*s)])/(1+r)
        return rnmValue if rnmValue > abs(self.getStrike()-s) else abs(self.getStrike()-s)
    
    def rollback2d(self, p, q, n, s, rng, m, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)

        rnmValue = (p[n]*rng[n+1][("u"+state,u*s,m)] + q[n]*rng[n+1][(state+"d",d*s,min(d*s,m))])/(1+r)
        return rnmValue if rnmValue > abs(self.getStrike()-s) else abs(self.getStrike()-s)

    def rollback2u(self, p, q, n, s, rng, m, state):
        u = self.getUnderlying().getUpFactorn(n)
        d = self.getUnderlying().getDownFactorn(n)
        r = self.getBank().getInterestn(n)

        rnmValue = (p[n]*rng[n+1][("u"+state,u*s,max(u*s,m))] + q[n]*rng[n+1][(state+"d",d*s,m)])/(1+r)
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

    def __str__(self):
        return f"DOWN AND OUT BARRIER\nBarrier: {self.downBarrier}\n Underlying: {str(self.underlying)}"

    def getUnderlying(self):
        return self.underlying

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

    def isSame(self, other):
        if not isinstance(self, other): return False
        if self.getBarrier() != other.getBarrier(): return False
        if not self.getUnderlying().isSame(other.getUnderlying()): return False
        return True

    def domainCalc(self, N):
        underly = self.getUnderlying()
        return downDomain_2(underly.getBank(), underly.getUnderlying(), N)

    def rollback(self, p, q, n, s, rng, m, state):
        rnmValue = self.underlying.rollback2d(p, q, n, s, rng, m, state)
        return rnmValue if m >= self.getBarrier() else 0

    def currEval(self, s):
        return self.underlying.currEval(s)
    
    def finalEval(self, s, m):
        return self.underlying.finalEval(s) if m >= self.getBarrier() else 0


class Up_Out_Barrier(Option):
    def __init__(self, underlying, U):
        self.underlying = underlying
        self.upBarrier = U
    
    def __str__(self):
        return f"UP AND OUT BARRIER\nBarrier: {self.upBarrier}\n Underlying: {str(self.underlying)}"

    def getUnderlying(self):
        return self.underlying

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

    def isSame(self, other):
        if not isinstance(self, other): return False
        if self.getBarrier() != other.getBarrier(): return False
        if not self.getUnderlying().isSame(other.getUnderlying()): return False
        return True

    def domainCalc(self, N):
        underly = self.getUnderlying()
        return upDomain_2(underly.getBank(), underly.getUnderlying(), N)

    def rollback(self, p, q, n, s, rng, m, state):
        rnmValue = self.underlying.rollback2u(p, q, n, s, rng, m, state)
        return rnmValue if m <= self.getBarrier() else 0

    def currEval(self, s):
        return self.underlying.currEval(s)
    
    def finalEval(self, s, m):
        return self.underlying.finalEval(s) if m <= self.getBarrier() else 0


class Down_In_Barrier(Option):
    def __init__(self, underlying, D):
        self.underlying = underlying
        self.downBarrier = D

    def __str__(self):
        return f"DOWN AND IN BARRIER\nBarrier: {self.downBarrier}\n Underlying: {str(self.underlying)}"

    def getUnderlying(self):
        return self.underlying

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

    def isSame(self, other):
        if not isinstance(self, other): return False
        if self.getBarrier() != other.getBarrier(): return False
        if not self.getUnderlying().isSame(other.getUnderlying()): return False
        return True

    def domainCalc(self, N):
        underly = self.getUnderlying()
        return downDomain_2(underly.getBank(), underly.getUnderlying(), N)

    def rollback(self, p, q, n, s, rng, m, state):
        rnmValue = self.underlying.rollback2d(p, q, n, s, rng, m, state)
        return rnmValue if m <= self.getBarrier() else 0

    def currEval(self, s):
        return self.underlying.currEval(s)
    
    def finalEval(self, s, m):
        return self.underlying.finalEval(s) if m <= self.getBarrier() else 0


class Up_In_Barrier(Option):
    def __init__(self, underlying, U):
        self.underlying = underlying
        self.upBarrier = U

    def __str__(self):
        return f"UP AND IN BARRIER\nBarrier: {self.upBarrier}\n Underlying: {str(self.underlying)}"

    def getUnderlying(self):
        return self.underlying

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

    def isSame(self, other):
        if not isinstance(self, other): return False
        if self.getBarrier() != other.getBarrier(): return False
        if not self.getUnderlying().isSame(other.getUnderlying()): return False
        return True

    def domainCalc(self, N):
        underly = self.getUnderlying()
        return upDomain_2(underly.getBank(), underly.getUnderlying(), N)

    def rollback(self, p, q, n, s, rng, m, state):
        rnmValue = self.underlying.rollback2u(p, q, n, s, rng, m, state)
        return rnmValue if m >= self.getBarrier() else 0

    def currEval(self, s):
        return self.underlying.currEval(s)
    
    def finalEval(self, s, m):
        return self.underlying.finalEval(s) if m >= self.getBarrier() else 0

          
from math import pi, atan, log, cosh, sinh, sqrt
# =============================================================================
# =============================================================================
def MainCalc(V, H, L, tol=1e-4, maxIter=1000):
    #check L
    minL = sqrt(H**2 + V**2)
    if L < minL:
        print "Error. L must be at least Sqr(H^2+V^2)=%.2f." % minL
        return False

    #retval(7)= MBR, TA1, TA2, L1, L2, MaxD, solverOutput
    retval = CalculateDoubleCatenary(V, H, L, tol, maxIter)
    MBR = retval[0]
    TA1 = retval[1]
    TA2 = retval[2]
    L1 = retval[3]
    L2 = retval[4]
    MaxD = retval[5]
    solverOutput = retval[6]

    #PRINT VALUES
    print "Vertical \t%.2fm" % V
    print "Horizontal \t%.2fm" % H
    print "Length of Line\t%.2fm" % L
    print "Lower Top Angle\t%.2fdeg" % TA1
    print "Upper Top Angle\t%.2fdeg" % TA2
    #apply correction if catenary is taut or otherwise
    if TA1 <= 90:
        print "Maximum depth\t%.2fm" % MaxD
        print "MBR        \t%.2fm" % MBR
        print "Lower Length\t%.2fm" % L1
        print "Upper Length\t%.2fm" % L2
    else:
        print "Maximum depth\t%.2fm" % V
        print "MBR          \tTaut" % MBR
        print "Lower Length\tTaut" % L1
        print "Upper Length\tTaut" % L2
    #print "Solver output \t%.2e" % solverOutput
    if solverOutput >= tol:
        print "WARNING: Solver not converged. Try increasing max. number of iterations or tolerance."
    #Return something?
# =============================================================================
# =============================================================================
def CalcTA(V, H, TA, flagLowerTA, tol=1e-4, maxIter=1000):
    '''
    TA2 - upper end
    TA1 - lower end
    '''
    #check inpu top angle
    #number must be positive and smaller than 
    #the straight line angle 
    #1deg extra is added to avoid numeric error
    LimTA = 180.0 / pi * atan(1.0*V/H) #make sure is a float: *1.0
    
    if flagLowerTA: LimTA = LimTA + 90 - 1
    else:           LimTA = 90 - LimTA - 1
    
    
    if TA > LimTA or TA <= 0:
        print "Error: top angle must be greater than 0.00deg and smaller then %.2fdeg" % LimTA
        return False

    #note that tol is divided and MaxIter multiiplied by 100 
        #this is because results are very sensitive to TA
    L = AdjustTopAngle(TA, H, V, tol / 100.0, maxIter * 100, flagLowerTA)
    MainCalc(V, H, L, tol, maxIter)
    #Return something?
# =============================================================================
# =============================================================================
def AdjustTopAngle(TA, H, V, tol, maxIter, flagLowerTA):
    '''this function iterates the catenray solver to adjust the top angle
    at the point with higher elevation (vessel)
    this function returns the required length'''

    #solver parameters
    erro = 999
    deltaL = 30
    #set initial guess for L
    L = H + V
    #calculate catenary for initial L
    retval = CalculateDoubleCatenary(V, H, L, tol, maxIter)
    #get top angle - checking if TA1 or TA2 is being adjusted
    if flagLowerTA: TAindex = 1
    else:           TAindex = 2
    retTA = retval[TAindex]

    if retTA < TA: deltaL = -deltaL
    else:          deltaL = deltaL
    i=0
    while erro>tol and i<maxIter:
        i +=  1
        L += deltaL
        retval = CalculateDoubleCatenary(V, H, L, tol, maxIter)
        retTA = retval[TAindex]
        if not (((retTA < TA) and (deltaL < 0)) or ((retTA > TA) and (deltaL > 0))):
            deltaL *= -0.5
        erro = abs(retTA - TA)
    return L
# =============================================================================
# =============================================================================
def CalculateDoubleCatenary( V,  H,  L,  tol,  maxIter):
    #call function to solve catenary factor (MBR)
    retval = SolveCatenaryFactor(V, H, L, tol, maxIter)
    a = retval[0]
    solverOutput = retval[1]
    #calculate catenary parameters
    #x values
    x1 = 0.5 * (a * log(1.0*(L + V) / (L - V)) - H) #make sure is a float: *1.0
    x2 = 0.5 * (a * log(1.0*(L + V) / (L - V)) + H)
    #y values
    y1 = a * cosh(x1 / a)
    y2 = a * cosh(x2 / a)
    # lengths
    L1 = -a * sinh(x1 / a)
    L2 = a * sinh(x2 / a)
    #top angles
    TA1 = 90 + 180 / pi * atan(sinh(x1 / a)) # lower end
    TA2 = 90 - 180 / pi * atan(sinh(x2 / a)) # upper end
    #maximum depth
    MaxD = max(y1, y2) - a

    return [a, TA1, TA2, L1, L2, MaxD, solverOutput]
# =============================================================================
# =============================================================================
def SolveCatenaryFactor(V, H, L, tol, maxIter):
    '''this function implements a Netwon-Raphson method to find roots of equations
    this is used to find the catenary parameter a'''

    #initial guess of catenary parameter
    a = 10.0
    i = 0; fa=999.9
    while  i < maxIter and abs(fa) > tol:
        i+=1
        fa = 2 * a * sinh(H / 2 / a) - sqrt(L**2 - V**2)
        dfa = 2 * sinh(H / 2 / a) - H / a * cosh(H / 2 / a)
        a = abs(a - fa / dfa)
    #return catenary factor and solver final error
    return [a, abs(fa)]
# =============================================================================
# =============================================================================
# oookkk... good to go... MAIN SCRIPT STARTS HERE
# =============================================================================
# =============================================================================
V=250
H=400
L=700
print "=== Typical use ==="
MainCalc(V, H, L)
print "=== Adjust Top Angle Mode ==="
TA=20
flagLowerTA=False
CalcTA(V, H, TA, flagLowerTA)

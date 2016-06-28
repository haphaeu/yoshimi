def LinearInterpolation(knownX,knownY,newX):
    #this function performs a linear interpolation
    #knownX and knownY shall be a list with 2 elements
    #newX shall be a single number
    #
    # !!! no error check implemented !!!
    #
    return knownY[0]+(newX-knownX[0])*(knownY[1]-knownY[0])/(knownX[1]-knownX[0])

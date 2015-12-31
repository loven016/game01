
import math as m

class VectorMath:

    def magnitude(vec):

        someSum = 0
        for x in vec:
            someSum += x*x

        #use max to prevent division by 0
        return max(1,m.sqrt(someSum))

    def mult(vec, n):
        outVec = []
        for x in vec:
            outVec += [x*n]

        return outVec
    
    def normalize(vec):

        vecMag = VectorMath.magnitude(vec)
        return VectorMath.mult(vec,(1/vecMag))

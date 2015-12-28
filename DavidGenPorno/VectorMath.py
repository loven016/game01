
import math as m

class VectorMath:

    def magnitude(vec):

        someSum = 0
        for x in vec:
            someSum += x*x

        return m.sqrt(someSum)

    def mult(vec, n):
        outVec = []
        for x in vec:
            outVec += [x*n]

        return outVec
    
    def normalize(vec):

        vecMag = VectorMath.magnitude(vec)
        return VectorMath.mult(vec,(1/vecMag))

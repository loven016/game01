
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

    def rotate(vec, degrees):
        radians = degrees*0.0174533

        output = [0,0]
        output[0] = vec[0] * m.cos(radians) - vec[1] * m.sin(radians)
        output[1] = vec[0] * m.sin(radians) + vec[1] * m.cos(radians)
        #round if vector is to be applied directly, i.e. not a unit vector
        if VectorMath.magnitude(vec) > 2:
            output = [round(x) for x in output]

        return output

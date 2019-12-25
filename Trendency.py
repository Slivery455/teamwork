from Error import *
#This class is used to store result after user finished the questionare.
class Trend:
    def __init__(self,keylist,valuelist):
        if (isinstance(keylist, list) == False or isinstance(valuelist, list) == False ):
            raise ParamError('Error Param for initializing Trendency.')
            return
        length = 0
        maxlength = 0
        self.weight = {}
        if  keylist.__len__() < valuelist.__len__():
            length = keylist.__len__()
            maxlength = valuelist.__len__()
            #Ingore excrescent key.
            print("Waring: Symmetry is broken for Trendency initialization.")
        elif  keylist.__len__() > valuelist.__len__():
            length = valuelist.__len__()
            maxlength = keylist.__len__()
            # Set 0 if some value lost.
            for i in range(length, maxlength):
                self.weight.setdefault(keylist[i], 0)
            print("Waring: Symmetry is broken for Trendency initialization.")

        self.length = valuelist.__len__()
        for i in range(0, length):
            if ((isinstance(valuelist[i], float) == False) and (isinstance(valuelist[i], int) == False)):
                raise ParamError('Error Param(', valuelist[i], type(valuelist[i]), ') for Fruit!(', i, ')')
                return
        for i in range(0,length):
            self.weight.setdefault(keylist[i],valuelist[i])


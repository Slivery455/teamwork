from Trendency import Trend
from Error import ParamError

#This class is for fruit.It has method that construction a default object by Fruit().
#Besides,the name of method says all.

class Food:



    def __init__(self,name,nutrition):
        if name == None and nutrition == None:
            self = self.Pretend()
            return
        self.__error = False
        if(isinstance(nutrition, dict)== False):
            self.__error = True
            raise ParamError('Error Param for initializing Fruit.')
        self.attr = {'name':name,'nutrition': {}, 'score':0,'worked':False}
        #for i in nutrition.keys():
            #print(float(nutrition.get(i)))
            #if((isinstance(nutrition.get(i), float) == False) and (isinstance(nutrition.get(i), int) == False)):
            #    raise ParamError('Error Param('+str(nutrition.get(i))+str(type(nutrition.get(i)))+') for Fruit!('+i+')')
        self.attr['name'] = name
        self.attr['nutrition'] = nutrition

    def Pretend(self):
        self.attr = {}
        self.attr.setdefault('name','Apple')
        self.attr.setdefault('nutrition', {})
        self.attr['nutrition'].setdefault('VA', 0.4)
        self.attr['nutrition'].setdefault('VB', 0.7)
        self.attr['nutrition'].setdefault('VC', 1)
        self.attr['nutrition'].setdefault('VD', 0.1)
        self.attr['nutrition'].setdefault('Sugar', 0.5)
        self.attr['nutrition'].setdefault('Protein', 0.1)
        self.attr['nutrition'].setdefault('Fibre', 0.9)
        self.attr.setdefault('score',20)

    def Calculate(self,trend):
        if isinstance(trend, Trend) == False:
            raise ParamError("Error Param for Food::Calculate().")
        #Calculating the score each kind of fruit with collected trendency
        self.attr['score'] = 0
        for i in self.attr['nutrition'].keys():
            if(trend.weight.get(i) == None):
                raise BaseException('Default value:',i)
                self.attr['score'] = -9999
                return -9999;
            self.attr['score'] +=  float(trend.weight.get(i)) * float(self.attr['nutrition'].get(i))
        self.attr['worked'] = True
        return self.attr['score']

    def Print(self):
        print('<CLASS Food> ',self.attr)

    def ToString(self):
        return '<CLASS Food> ' + str(self.attr)

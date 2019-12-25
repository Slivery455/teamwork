from Food import Food
from Error import ParamError
class Store:
    weight = {'price': -0.2, 'like': 0.2, 'sale': 1, 'fruit': 0.2}
    def __init__(self, name, price, like, sale, food, url):
        self.error = False
        if(isinstance(name, str) == False):
            self.error = True
            raise ParamError('attribute \'name\' must be \'str\'!')
        if(isinstance(price, float) == False) and (isinstance(price, int) == False):
            self.error = True
            raise ParamError('attribute \'price\' must be \'float\' or \'int\'!')
        if(isinstance(like, int) == False):
            self.error = True
            raise ParamError('attribute \'like\' must be \'int\'!')
        if(isinstance(sale, int) == False):
            self.error = True
            raise ParamError('attribute \'sale\' must be \'int\'!')
        if(isinstance(food, Food) == False):
            self.error = True
            raise ParamError('attribute \'food\' must be \'Food\'!')
        if (isinstance(url, str) == False):
            self.error = True
            raise ParamError('attribute \'url\' must be \'str\'!')
        self.attr = {'name': name,'Performance':{}, 'score': 0,'url' : url}
        self.attr['Performance'] = {'price':price,'like' : like,'sale' : sale}
        self.fruit = food
        # Assess the shop
        for i in self.attr['Performance'].keys():
            if (Store.weight.get(i) == None):
                print('Default value:', i)
                return;
            self.attr['score'] += Store.weight.get(i) * self.attr['Performance'].get(i)
        if(self.fruit.attr['worked'] == False):
            print('Warning:This Store contains uninitialized data.')
        self.attr['score'] += self.fruit.attr['score']

    def Print(self):
        if(self.error == False):
            print('<CLASS Store> ',self.attr)
            print(" attr->'Fruit': " +self.fruit.ToString())
        return self.error

    def Calculate(self):
        if(self.error == True):
            print('Error instance!')
            return
        self.attr['score'] = 0
        for i in self.attr['Performance'].keys():
            if (Store.weight.get(i) == None):
                print('Default value:', i)
                self.attr['score'] = -9999
                return -9999;
            self.attr['score'] += Store.weight.get(i) * self.attr['Performance'].get(i)
        if(self.fruit.attr['score'] == 0):
            print('Warning:This Store contains uninitialized data.')
        self.attr['score'] += self.fruit.attr['score']
        return self.attr['score']


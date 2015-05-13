import wx

"""
Our entire world
"""
class City(object):
    
    def __init__(self, size=20, price=250):
        self.size = size
        self.__number_of_houses = size * size
        self.houses = [[price, None] for _ in range(self.__number_of_houses)]
        
    def get_house_price(self, x, y):
        if (x >= 0 and x < self.size) and (y >= 0 and y < self.size):
            return self.houses[y * self.size + x][0]
        else:
            # If outside the city, the price is zero
            return 0
    
    def set_house_price(self, x, y, price):
        if (x >= 0 and x < self.size) and (y >= 0 and y < self.size):
            self.houses[y * self.size + x][0] = price
            
    def get_house_occupant(self, x, y):
        if (x >= 0 and x < self.size) and (y >= 0 and y < self.size):
            return self.houses[y * self.size + x][1]
        else:
            return None
    
    def set_house_occupant(self, x, y, person):
        if (x >= 0 and x < self.size) and (y >= 0 and y < self.size):
            self.houses[y * self.size + x][1] = person
    
    @property
    def number_of_houses(self):
        return self.__number_of_houses

"""
Manages everyone living in our city
"""
class Population(object):
    def __init__(self, size, city):
        self.__size = size
        self.__current_step = 0
        self.city = city
        self.people = [Person() for _ in range(self.__size)]
        
        #Occupy the houses randomly
        for person in self.people:
            self.city.size
    
    @property
    def size(self):
        return self.__size
    
    def step(self):
        self.__current_step += 1
        

"""
A person living in our city
"""
class Person(object):
    def __init__(self):
        self.rent_history = []
        self.last_moved = 0
        self.current_x = -1
        self.current_y = -1
        
    
    def can_move(self, step):
        if (step - self.last_moved) in [6, 12, 18] or (step - self.last_moved) >= 24:
            return True
        return False
    
    def move(self, step, x, y):
        if (step - self.last_moved) in [6, 12, 18] or (step - self.last_moved) >= 24:
            return True
        return False
    

"""
Outputs our city
"""
class CityPrinter(object):
    
    def __init__(self, city, population):
        self.city = city
        self.population = population
    
    """
    Write the city to standard out
    """
    def __str__(self):
        output = ""
        for y in range(self.city.size):
            row = ""
            for x in range(self.city.size):
                occupied_string = "_" if self.city.get_house_occupant(x, y) == None else "X"
                row += str("%3d%s " % (self.city.get_house_price(x, y), occupied_string))
            output += row + "\n"
        return output
    

if __name__=='__main__':
    #TODO: Get these from command line arguments
    citysize = 20
    price = 250
    citypopulation = 300
    
    city = City(citysize, price)
    population = Population(citypopulation, city)
    cityprinter = CityPrinter(city, population)
    
    
    print("Starting Simulation")
    print("")
    print("Number of Houses: " + str(city.number_of_houses))
    print("Population: " + str(population.size))
    print("")
    print("Initial City")
    print(cityprinter)






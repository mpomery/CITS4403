import wx
import random

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
    
    def get_empty_houses(self):
        empty = []
        for x in range(self.size):
            for y in range(self.size):
                if self.get_house_occupant(x, y) == None:
                    empty.append((x, y))
        return empty
        
    
    @property
    def number_of_houses(self):
        return self.__number_of_houses

"""
Manages everyone living in our city
"""
class Population(object):
    def __init__(self, city, size=300):
        self.__size = size
        self.__current_step = 0
        self.city = city
        self.people = [Person() for _ in range(self.__size)]
        
        #Occupy the houses randomly
        homes = []
        for x in range(self.city.size):
            for y in range(self.city.size):
                homes.insert(random.randint(0, len(homes)), (x,y))
        for person in self.people:
            home = homes.pop(0)
            self.move_person(person, home[0], home[1])
    
    @property
    def size(self):
        return self.__size
    
    def step(self):
        self.__current_step += 1
        empty_houses = self.city.get_empty_houses()
        people_to_move = self.get_people_to_move()
        print("End of Month " + str(self.__current_step))
        print("People Who Can Move: " + str(len(people_to_move)))
        
        
    
    def get_people_to_move(self):
        can_move = []
        for person in self.people:
            if person.can_move(self.__current_step):
                can_move.append(person)
        return can_move
    
    def move_person(self, person, x, y):
        self.city.set_house_occupant(x, y, person)
        person.move(0, x, y, self.city.get_house_price(x, y))

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
    
    def move(self, step, x, y, price):
        self.rent_history.append(price)
        self.last_moved = step
        self.current_x = x
        self.current_y = y
    

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
    citypopulation = 200
    
    city = City(citysize, price)
    population = Population(city, citypopulation)
    cityprinter = CityPrinter(city, population)
    
    
    print("Starting Simulation")
    print("")
    print("Number of Houses: " + str(city.number_of_houses))
    print("Population: " + str(population.size))
    print("")
    print("Initial City")
    print(cityprinter)
    for _ in range(3):
        for __ in range(12):
            population.step()
        print(cityprinter)
        print("A Year Goes By")






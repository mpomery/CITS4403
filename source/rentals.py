import wx
import random
import collections

# Named tuples are gret if we want an object as a data structure that we interact with
# That doesn't need its own function
Coordinates = collections.namedtuple('Coordinates', 'x y')
House = collections.namedtuple('House', 'location price')

"""
Our world. Holds all the houses.
"""
class City(object):
    
    def __init__(self, size=20, price=250):
        self.size = size
        self.__number_of_houses = size * size
        self.houses = [[price, None] for _ in range(self.__number_of_houses)]
        
    def get_house_price(self, coords):
        if 0 <= coords.x < self.size and 0 <= coords.y < self.size:
            return self.houses[coords.y * self.size + coords.x][0]
        return 0
    
    def set_house_price(self, coords, price):
        if 0 <= coords.x < self.size and 0 <= coords.y < self.size:
            self.houses[coords.y * self.size + coords.x][0] = price
    
    def get_house_occupant(self, coords):
        if 0 <= coords.x < self.size and 0 <= coords.y < self.size:
            return self.houses[coords.y * self.size + coords.x][1]
        return None
    
    def set_house_occupant(self, coords, person):
        if 0 <= coords.x < self.size and 0 <= coords.y < self.size:
            self.houses[coords.y * self.size + coords.x][1] = person
    
    @property
    def empty_houses(self):
        empty = []
        for x in range(self.size):
            for y in range(self.size):
                coords = Coordinates(x=x, y=y)
                if self.get_house_occupant(coords) == None:
                    empty.append(coords)
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
                coords = Coordinates(x=x, y=y)
                homes.insert(random.randint(0, len(homes)), coords)
        for person in self.people:
            home = homes.pop(0)
            self.move_person(person, home)
    
    @property
    def size(self):
        return self.__size
    
    def step(self):
        self.__current_step += 1
        empty_houses = self.city.empty_houses
        people_to_move = self.get_people_to_move()
        #print("End of Month " + str(self.__current_step))
        #print("People Who Can Move: " + str(len(people_to_move)))
        #print("Houses to Move Into: " + str(len(empty_houses)))
        for house in empty_houses:
            houseprice = self.city.get_house_price(house)
            houseprice = houseprice - 5
            self.city.set_house_price(house, houseprice)
    
    def get_people_to_move(self):
        can_move = []
        for person in self.people:
            if person.can_move(self.__current_step):
                can_move.append(person)
        return can_move
    
    # TODO: Check this works
    def move_person(self, person, coords):
        self.city.set_house_occupant(coords, person)
        person.move(0, coords, self.city.get_house_price(coords))

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
    
    def move(self, step, coords, price):
        self.rent_history.append(price)
        self.last_moved = step
        self.current_x = coords.x
        self.current_y = coords.y
    

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
                coords = Coordinates(x=x, y=y)
                occupied_string = "_" if self.city.get_house_occupant(coords) == None else "X"
                row += str("%3d%s " % (self.city.get_house_price(coords), occupied_string))
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
        print("End Of Year " + str(_ + 1))
        for __ in range(12):
            population.step()
        print(cityprinter)






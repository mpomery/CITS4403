import wx
import random
import collections

# Named tuples are gret if we want an object as a data structure that we interact with that doesn't
# need its own function, and won't need changing. Therefore they are only good for passing information
# around, and not for passing around values that need changing.
Coordinates = collections.namedtuple('Coordinates', 'x y')
#House = collections.namedtuple('House', 'price occupant')
# House can't be a named tuple as we change values in house and can not change values in tuples.

class House(object):
    def __init__(self, price, occupant = None):
        self.__price = price
        self.__occupant = occupant
    
    @property
    def price(self):
        return self.__price
    
    @property
    def occupant(self):
        return self.__occupant
    
    @price.setter
    def price(self, new):
        self.__price = new
        
    @occupant.setter
    def occupant(self, new):
        self.__occupant = new

"""
Our world. Holds all the houses.
"""
class City(object):
    
    def __init__(self, size=20, price=250):
        self.size = size
        self.__number_of_houses = size * size
        self.houses = [House(0) for _ in range(self.__number_of_houses)]
        for house in self.houses:
            house.price = price
    
    def get_house(self, coords):
        if self.within_city(coords):
            return self.houses[self.coords_to_index(coords)]
        return None
    
    def coords_to_index(self, coords):
        return coords.y * self.size + coords.x
    
    def within_city(self, coords):
        return (0 <= coords.x < self.size and 0 <= coords.y < self.size)
    
    @property
    def empty_houses(self):
        empty = []
        for x in range(self.size):
            for y in range(self.size):
                coords = Coordinates(x=x, y=y)
                if self.get_house(coords).occupant == None:
                    empty.append(coords)
        return empty
        
    @property
    def occupied_houses(self):
        occupied = []
        for x in range(self.size):
            for y in range(self.size):
                coords = Coordinates(x=x, y=y)
                if self.get_house(coords).occupant != None:
                    occupied.append(coords)
        return occupied
    
    @property
    def number_of_houses(self):
        return self.__number_of_houses
    
    @property
    def max_price(self):
        return max(self.houses, key=lambda h: h.price).price
    
    @property
    def min_price(self):
        return min(self.houses, key=lambda h: h.price).price

"""
Manages everyone living in our city
"""
class Population(object):
    def __init__(self, city, size=300):
        self.__size = size
        self.__current_step = 0
        self.city = city
        self.people = [Person(city) for _ in range(self.__size)]
        
        #Occupy the houses randomly
        homes = []
        for x in range(self.city.size):
            for y in range(self.city.size):
                coords = Coordinates(x=x, y=y)
                homes.insert(random.randint(0, len(homes)), coords)
        for person in self.people:
            home = homes.pop(0)
            person.move(self.__current_step, home)
    
    def step(self):
        self.__current_step += 1
        
        empty_houses = self.city.empty_houses
        occupied_houses = self.city.occupied_houses
        people_to_move = self.people_to_move
        
        self.update_rent(empty_houses)
        self.move_people(people_to_move)
        self.update_rent(occupied_houses)
        
        
    def update_rent(self, houses_coords):
        # Figure out new prices and store them in a list
        new_prices = []
        for coords in houses_coords:
            # TODO: Update price depending on surrounding prices
            #average_neighbour_price = 0
            house = self.city.get_house(coords)
            new_price = house.price
            if house.occupant == None:
                new_price = house.price - 5
            elif house.occupant.can_move(self.__current_step):
                new_price = house.price + 5
            
            new_prices.append((coords, new_price))
                
        
        # Update all the prices at once so that we don't have race conditions
        for price in new_prices:
            self.city.get_house(price[0]).price = price[1]
    
    @property
    def people_to_move(self):
        can_move = []
        for person in self.people:
            if person.can_move(self.__current_step):
                can_move.append(person)
        return can_move
    
    # TODO: Implement This
    def move_people(self, people):
        pass
    
    @property
    def size(self):
        return self.__size

"""
A person living in our city
"""
class Person(object):
    def __init__(self, city):
        self.rent_history = []
        self.last_moved = 0
        self.current_location = Coordinates(-1, -1)
        self.city = city
    
    def can_move(self, step):
        return (step - self.last_moved) in [6, 12, 18] or (step - self.last_moved) >= 24
    
    def move(self, step, coords):
        self.city.get_house(coords).occupant = self
        self.rent_history.append(self.city.get_house(coords).price)
        self.last_moved = step
        self.current_location = coords

"""
Outputs our city
"""
class CityPrinter(object):
    
    def __init__(self, city, population):
        self.city = city
        self.population = population
    
    def create_heatmap(self, occupied_only = False):
        print("Cheapest Place: " + str(self.city.min_price))
        print("Most Expensive Place: " + str(self.city.max_price))
    
    """
    Write the city to standard out for quick testing and debugging.
    """
    def __str__(self):
        output = ""
        for y in range(self.city.size):
            row = ""
            for x in range(self.city.size):
                coords = Coordinates(x=x, y=y)
                occupied_string = "_" if self.city.get_house(coords).occupant == None else "X"
                row += str("%3d%s " % (self.city.get_house(coords).price, occupied_string))
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
    cityprinter.create_heatmap()





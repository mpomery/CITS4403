import wx
from wx.lib.floatcanvas.FloatCanvas import FloatCanvas
import random
import collections
import time

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
        self.__size = size
        self.__number_of_houses = size * size
        self.__houses = [House(0) for _ in range(self.__number_of_houses)]
        for house in self.__houses:
            house.price = price
    
    def get_house(self, coords):
        if self.within_city(coords):
            return self.__houses[self.coords_to_index(coords)]
        return None
    
    def coords_to_index(self, coords):
        return coords.y * self.__size + coords.x
    
    def within_city(self, coords):
        return (0 <= coords.x < self.__size and 0 <= coords.y < self.__size)
    
    @property
    def empty_houses(self):
        empty = []
        for x in range(self.__size):
            for y in range(self.__size):
                coords = Coordinates(x=x, y=y)
                if self.get_house(coords).occupant == None:
                    empty.append(coords)
        return empty
    
    @property
    def houses(self):
        houses = []
        for x in range(self.__size):
            for y in range(self.__size):
                coords = Coordinates(x=x, y=y)
                houses.append(coords)
        return houses
    
    @property
    def occupied_houses(self):
        occupied = []
        for x in range(self.__size):
            for y in range(self.__size):
                coords = Coordinates(x=x, y=y)
                if self.get_house(coords).occupant != None:
                    occupied.append(coords)
        return occupied
    
    @property
    def number_of_houses(self):
        return self.__number_of_houses
    
    @property
    def max_price(self):
        return max(self.__houses, key=lambda h: h.price).price
    
    @property
    def min_price(self):
        return min(self.__houses, key=lambda h: h.price).price
    
    @property
    def size(self):
        return self.__size

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
    
    # TODO: Move people to houses better suited to them
    # better value with similar neighbours
    # more neighbours but slightly more expensive
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
        
        self.app = wx.PySimpleApp()
        self.w = self.city.size + 100
        self.h = self.city.size + 100
        self.frame = wx.Frame(None, -1, 'Occupied Houses', size=(self.w, self.h))
        self.canvas = FloatCanvas(self.frame, -1)
    
    def create_heatmap(self, occupied_only = False):
        #print("Cheapest Place: " + str(self.city.min_price))
        #print("Most Expensive Place: " + str(self.city.max_price))
        time1 = time.time()
        min_price = self.city.min_price
        max_price = self.city.max_price
        
        for house in self.city.houses:
            x = house.x - self.city.size / 2
            y = house.y - self.city.size / 2
            col = self.color(house, min_price, max_price)
            self.canvas.AddPoint((x, y), Color = col)
            #print(str((x, y)))
        #self.canvas.AddPoint((0, 0))
        time2 = time.time()
        print('Generating Image took %0.3f ms' % ((time2-time1) * 1000.0))
        self.frame.Show()
        self.app.MainLoop()
    
    # TODO: Check that colors are distinct enough to see gradients
    def color(self, house, min_price, max_price):
        #print("Colouring In")
        price = self.city.get_house(house).price
        
        if self.city.get_house(house).occupant != None:
            # Generating http://geog.uoregon.edu/datagraphics/color/Bu_10.txt on the fly
            red_range = (0, 0.9)
            green_range = (0.25, 1.0)
            blue_range = (1.0, 1.0)
        else:
            red_range = (1.0, 1.0)
            green_range = (0, 0)
            blue_range = (0, 0)
        
        percentage_of_range = 1 - (price - min_price)/(max_price - min_price)
        
        red = (((red_range[1] - red_range[0]) * percentage_of_range) + red_range[0]) * 255
        green = (((green_range[1] - green_range[0]) * percentage_of_range) + green_range[0]) * 255
        blue = (((blue_range[1] - blue_range[0]) * percentage_of_range) + blue_range[0]) * 255
        
        return wx.Colour(red, green, blue, 1)
    
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
    citysize = 100
    price = 250
    citypopulation = int(citysize*citysize*0.8)
    
    time1 = time.time()
    city = City(citysize, price)
    population = Population(city, citypopulation)
    cityprinter = CityPrinter(city, population)
    
    
    print("Starting Simulation")
    print("")
    print("Number of Houses: " + str(city.number_of_houses))
    print("Population: " + str(population.size))
    print("")
    print("Initial City")
    #print(cityprinter)
    for _ in range(3):
        #print("End Of Year " + str(_ + 1))
        for __ in range(12):
            population.step()
        #print(cityprinter)
    print("Generating Image")
    time2 = time.time()
    print('Simulation took %0.3f ms' % ((time2-time1) * 1000.0))
    cityprinter.create_heatmap()













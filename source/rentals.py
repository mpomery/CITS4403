from __future__ import division
import wx
from wx.lib.floatcanvas.FloatCanvas import FloatCanvas
import random
import collections
import time
import sys

# Named tuples are gret if we want an object as a data structure that we interact with that doesn't
# need its own function, and won't need changing. Therefore they are only good for passing information
# around, and not for passing around values that need changing.
Coordinates = collections.namedtuple('Coordinates', 'x y')
#House = collections.namedtuple('House', 'price occupant')
# House can't be a named tuple as we change values in house and can not change values in tuples.

class House(object):
    def __init__(self, price):
        self.__price = price
        self.__occupant = None
    
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
    
    def __init__(self, size, neighbourhood_size=3):
        self.neighbourhood_size = neighbourhood_size
        self.__size = size
        self.__number_of_houses = size * size
        self.__houses = [House(0) for _ in range(self.__number_of_houses)]
        for house in self.__houses:
            house.price = 250
    
    def get_house(self, coords):
        if self.within_city(coords):
            return self.__houses[self.coords_to_index(coords)]
        return None
    
    def get_neighbourhood(self, coords):
        neighbours = []
        for x in range(coords.x - self.neighbourhood_size, coords.x + self.neighbourhood_size + 1):
            for y in range(coords.y - self.neighbourhood_size, coords.y + self.neighbourhood_size + 1):
                if coords.x != x and coords.y != y:
                    neighbour_coords = Coordinates(x, y)
                    neighbour = self.get_house(neighbour_coords)
                    if neighbour != None:
                        neighbours.append(neighbour)
        return neighbours
    
    def coords_to_index(self, coords):
        return coords.y * self.__size + coords.x
    
    def within_city(self, coords):
        return (0 <= coords.x < self.__size and 0 <= coords.y < self.__size)
    
    def update_rent(self, houses_coords, step):
        # Figure out new prices and store them in a list
        new_prices = []
        for coords in houses_coords:
            # TODO: Check this works with moving people
            house = self.get_house(coords)
            new_price = house.price
            
            neighbourhood = self.get_neighbourhood(coords)
            
            num_neighbours = len(neighbourhood)
            num_occupied = sum(int(h.occupant != None) for h in neighbourhood)
            num_unoccupied = num_neighbours - num_occupied
            
            average_rent = sum(h.price for h in neighbourhood)/len(neighbourhood)
            if num_occupied != 0:
                average_occupied = sum(h.price if h.occupant != None else 0 for h in neighbourhood)/num_occupied
            else:
                average_occupied = 0
            if num_unoccupied != 0:
                average_unoccupied = sum(h.price if h.occupant == None else 0 for h in neighbourhood)/num_unoccupied
            else:
                average_unoccupied = 0
            
            if house.occupant == None:
                if house.price >= average_occupied:
                    new_price = house.price * 0.95
                elif house.price > average_unoccupied:
                    new_price = house.price * 0.95
                elif house.price >= average_rent:
                    new_price = house.price * 0.99
                else:
                    new_price = house.price * 1.01
            elif house.occupant.time_at_house(step) % 6 == 0:
                new_price = house.price + 5
            
            new_prices.append((coords, int(new_price)))
        
        # Update all the prices at once so that we don't have race conditions
        for price in new_prices:
            self.get_house(price[0]).price = price[1]
    
    @property
    def empty_houses(self):
        empty = []
        for x in range(self.__size):
            for y in range(self.__size):
                coords = Coordinates(x, y)
                if self.get_house(coords).occupant == None:
                    empty.append(coords)
        return empty
    
    @property
    def houses(self):
        houses = []
        for x in range(self.__size):
            for y in range(self.__size):
                coords = Coordinates(x, y)
                houses.append(coords)
        return houses
    
    @property
    def occupied_houses(self):
        occupied = []
        for x in range(self.__size):
            for y in range(self.__size):
                coords = Coordinates(x, y)
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
    def __init__(self, city, size):
        self.__size = size
        self.__current_step = 0
        self.city = city
        self.people = [Person(city) for _ in range(self.__size)]
        
        #Occupy the houses randomly
        homes = []
        for x in range(self.city.size):
            for y in range(self.city.size):
                coords = Coordinates(x, y)
                homes.insert(random.randint(0, len(homes)), coords)
        for person in self.people:
            home = homes.pop(0)
            person.move(self.__current_step, home)
    
    def step(self):
        self.__current_step += 1
        
        empty_houses = self.city.empty_houses
        occupied_houses = self.city.occupied_houses
        people_to_move = self.people_to_move
        
        self.city.update_rent(empty_houses, self.__current_step)
        self.move_people(people_to_move, empty_houses)
        self.city.update_rent(occupied_houses, self.__current_step)
    
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
    def move_people(self, people, empty_houses):
        #print("Moving People")
        people.sort(key=lambda p: p.income)
        empty_houses.sort(key=lambda h: self.city.get_house(h).price)
        if len(people) > 0:
            moves = []
            #print("Number of people to move: " + str(len(people)))
            #print(people[0].income)
            #print(self.city.get_house(empty_houses[0]).price)
            for person in people:
                if person.is_happy:
                    continue
                if len(empty_houses) > 0:
                    moves.append((person, empty_houses[0]))
                    empty_houses.pop(0)
            
            # Update all the prices at once so that we don't have race conditions
            for m in moves:
                #print(m[0])
                m[0].move(self.__current_step, m[1])
            
    
    @property
    def size(self):
        return self.__size
        
    @property
    def min_income(self):
        return min(self.people, key=lambda p: p.income).income
        
    @property
    def max_income(self):
        return max(self.people, key=lambda p: p.income).income

"""
A person living in our city
"""
class Person(object):
    def __init__(self, city, income = None):
        self.__rent_history = []
        self.last_moved = 0
        self.current_location = Coordinates(-1, -1)
        self.city = city
        if income == None:
            self.__income = random.randint(270, 600)
        else:
            self.__income = income
    
    def can_move(self, step):
        # Lived somewhere for 6 or 18 months, or there between 2 and 4 years or there for n years
        return (step - self.last_moved) in [6, 18] or 24 >= (step - self.last_moved) >=48 \
                or (step - self.last_moved) % 12 == 0
    
    def time_at_house(self, step):
        return (step - self.last_moved)
    
    def move(self, step, coords):
        self.city.get_house(coords).occupant = self
        if self.current_location != Coordinates(-1, -1):
            self.city.get_house(self.current_location).occupant = None
        self.__rent_history.append(self.city.get_house(coords).price)
        self.last_moved = step
        self.current_location = coords
    
    @property
    def is_happy(self):
        return self.calculate_happiness(self.current_location) >= 0.75
    
    """
    A number between 0 and 1, where 0 is on the verge of tears and 1 is extatic about everything
    """
    def calculate_happiness(self, house):
        return self.city.get_house(house).price <= (0.8  * self.income)
    
    @property
    def income(self):
        return self.__income
        
    @property
    def rent_history(self):
        return self.__rent_history

"""
Outputs our city
"""
class CityPrinter(object):
    
    def __init__(self, city, population):
        self.city = city
        self.population = population
        
        self.app = wx.App(False)
        self.w = self.city.size + 100
        self.h = self.city.size + 120
        self.frame_rent = wx.Frame(None, -1, 'Rent Map', size=(self.w, self.h))
        self.frame_income = wx.Frame(None, -1, 'Income Map', size=(self.w, self.h))
        self.canvas_rent = FloatCanvas(self.frame_rent, -1)
        self.canvas_income = FloatCanvas(self.frame_income, -1)
    
    def create_heatmaps(self):
        self.create_rent_map()
        self.create_income_map()
        self.app.MainLoop()
    
    def create_rent_map(self):
        print("Lowest Rent: " + str(self.city.min_price))
        print("Highest Rent: " + str(self.city.max_price))
        min_price = self.city.min_price
        max_price = self.city.max_price

        time1 = time.time()
        print("Generating Rent Map")
        
        for house in self.city.houses:
            x = house.x - self.city.size / 2
            y = house.y - self.city.size / 2
            col = self.color(self.city.get_house(house).price, min_price, max_price, \
                    self.city.get_house(house).occupant == None)
            self.canvas_rent.AddPoint((x, y), Color = col)
        
        time2 = time.time()
        print('Generating Image took %0.3f ms' % ((time2-time1) * 1000.0))
        
        self.frame_rent.Show()
    
    def create_income_map(self):
        print("Lowest Income: " + str(self.population.min_income))
        print("Highest Income: " + str(self.population.max_income))
        min_income = self.population.min_income
        max_income = self.population.max_income

        time1 = time.time()
        print("Generating Income Map")
        
        for house in self.city.houses:
            x = house.x - self.city.size / 2
            y = house.y - self.city.size / 2
            person = self.city.get_house(house).occupant
            if person != None:
                col = self.color(person.income, min_income, max_income)
                self.canvas_income.AddPoint((x, y), Color = col)
        
        time2 = time.time()
        print('Generating Image took %0.3f ms' % ((time2-time1) * 1000.0))
        
        self.frame_income.Show()
    
    def color(self, value, min, max, red=False):
        #print("Colouring In")
        
        if not red:
            # Approximating http://geog.uoregon.edu/datagraphics/color/Bu_10.txt on the fly
            red_range = (0, 0.9)
            green_range = (0.25, 1.0)
            blue_range = (1.0, 1.0)
        else:
            # Colour Shifting it to red
            red_range = (1.0, 1.0)
            green_range = (0, 0.9)
            blue_range = (0.25, 1.0)
        
        percentage_of_range = 1 - (value - min)/(max - min)
        
        red = (((red_range[1] - red_range[0]) * percentage_of_range) + red_range[0]) * 255
        green = (((green_range[1] - green_range[0]) * percentage_of_range) + green_range[0]) * 255
        blue = (((blue_range[1] - blue_range[0]) * percentage_of_range) + blue_range[0]) * 255
        
        return wx.Colour(red, green, blue, 1)
    
    """
    Write the city to standard out for quick testing and debugging.
    """
    def __str__(self):
        output = ""
        output += "Cheapest Place: " + str(self.city.min_price) + "\n"
        output += "Most Expensive Place: " + str(self.city.max_price) + "\n"
        output += "\n"
        for y in range(self.city.size):
            row = ""
            for x in range(self.city.size):
                coords = Coordinates(x, y)
                occupied_string = "_" if self.city.get_house(coords).occupant == None else "X"
                row += str("%3d%s " % (self.city.get_house(coords).price, occupied_string))
            output += row + "\n"
        return output

def print_argument_options():
    print("Command Line Arguments:")
    print("\trentals.py [city size] [population] [neighbourhood]")
    print("")
    print("\tcity size:     How many rows/columns the city should have.")
    print("\t               The city is always square. Defaults to 20")
    print("")
    print("\tpopulation:    How many people live in the city. Defaults to 75% city size.")
    print("\t               Leave as 0 if you want it to default.")
    print("")
    print("\tneighbourhood: How far a person looks for neighbours. Default is 3.")
    print("")
    print("")

def print_info():
    print("")
    print("Rental Price Simulation")
    print("Program By Mitchell Pomery")
    print("")
    print("Agent Based Simulation of changing rental prices given People moving around" + \
            "the city trying to be happy and living within their means.")
    print("")
    print("")

if __name__=='__main__':
    print_info()
    print_argument_options()
    
    # Get experiment variables from command line arguments
    if len(sys.argv) > 1:
        citysize = int(sys.argv[1])
    else:
        citysize = 20
    if len(sys.argv) > 2:
        citypopulation = int(sys.argv[2])
        if citypopulation >= (citysize*citysize - 1) or citypopulation <= 0:
            print("Population Invalid. Defaulting to 75% of city size.")
            citypopulation = int(citysize * citysize * 0.75)
    else:
        citypopulation = int(citysize * citysize * 0.75)
    if len(sys.argv) > 3:
        neighbourhood_size = int(sys.argv[3])
    else:
        neighbourhood_size = 3
    
    time1 = time.time()
    
    city = City(citysize, neighbourhood_size)
    population = Population(city, citypopulation)
    cityprinter = CityPrinter(city, population)
    
    print("Starting Simulation")
    print("Number of Houses: " + str(city.number_of_houses))
    print("Population: " + str(population.size))
    print("")
    for _ in range(10): # Years
        for __ in range(12): # Months
            population.step()
    if citysize <= 25:
        print(cityprinter)
    
    time2 = time.time()
    print('Simulation took %0.3f ms' % ((time2-time1) * 1000.0))
    
    print("Generating Image")
    cityprinter.create_heatmaps()













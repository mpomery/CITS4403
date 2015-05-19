from __future__ import division
import wx
from wx.lib.floatcanvas.FloatCanvas import FloatCanvas
import random
import collections
import time
import sys
import math

# Named tuples are gret if we want an object as a data structure that we interact with that doesn't
# need its own function, and won't need changing. Therefore they are only good for passing information
# around, and not for passing around values that need changing.
Coordinates = collections.namedtuple('Coordinates', 'x y')

"""
Our world.
"""
class City(object):
    
    def __init__(self, size, neighbourhood_size=3):
        self.neighbourhood_size = neighbourhood_size
        self.__size = size
        self.__number_of_houses = size * size
        self.__houses = [None for _ in range(self.__number_of_houses)]
    
    def get_house(self, coords):
        if self.within_city(coords):
            return self.__houses[self.coords_to_index(coords)]
        return None
        
    def set_house(self, coords, occupant):
        if self.within_city(coords):
            self.__houses[self.coords_to_index(coords)] = occupant
    
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
    
    @property
    def empty_houses(self):
        empty = []
        for x in range(self.__size):
            for y in range(self.__size):
                coords = Coordinates(x, y)
                if self.get_house(coords) == None:
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
    def number_of_houses(self):
        return self.__number_of_houses
    
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
        people_to_move = self.people_to_move
        
        self.move_people(people_to_move, empty_houses)
    
    @property
    def people_to_move(self):
        move = []
        for person in self.people:
            if person.wants_to_move(self.__current_step):
                move.append(person)
        return move
    
    def move_people(self, people, empty_houses):
        if len(people) > 0:
            moves = []
            for person in people:
                if len(empty_houses) > 0:
                    new = random.randint(0, len(empty_houses) - 1)
                    moves.append([person, empty_houses[new]])
                    empty_houses.pop(new)
            
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
    def __init__(self, city):
        self.current_location = Coordinates(-1, -1)
        self.city = city
        self.__income = random.randint(250, 750)
    
    def wants_to_move(self, step):
        # Income not in the approximately equal to suppounding incomes
        neighbours = self.city.get_neighbourhood(self.current_location)
        cumulative_income = sum([p.income for p in neighbours])
        average = cumulative_income / len(neighbours)
        return abs(average - self.income) > self.income * 0.25
    
    def move(self, step, coords):
        self.city.set_house(coords, self)
        if self.current_location != Coordinates(-1, -1):
            self.city.set_house(self.current_location, None)
        self.current_location = coords
    
    @property
    def income(self):
        return self.__income
    
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
        self.frame = wx.Frame(None, -1, 'Income Map', size=(self.w, self.h))
        self.canvas = FloatCanvas(self.frame, -1)
    
    def create_heatmap(self):
        min_income = self.population.min_income
        max_income = self.population.max_income
        print("Lowest Income: " + str(min_income))
        print("Highest Income: " + str(max_income))
        
        for house in self.city.houses:
            x = house.x - self.city.size / 2
            y = house.y - self.city.size / 2
            person = self.city.get_house(house)
            if person != None:
                col = self.color(person.income, min_income, max_income)
                self.canvas.AddPoint((x, y), Color = col)
        
        self.frame.Show()
        self.app.MainLoop()
    
    def color(self, value, min_val, max_val):
        # Approximating http://geog.uoregon.edu/datagraphics/color/Bu_10.txt on the fly
        red_range = (0, 0.9)
        green_range = (0.25, 1.0)
        blue_range = (1.0, 1.0)
        
        percentage_of_range = 1 - (value - min_val)/(max_val - min_val)
        
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
                coords = Coordinates(x, y)
                occupied = self.city.get_house(coords) != None
                if occupied:
                    row += str("%3d " % (self.city.get_house(coords).income))
                else:
                    row += str("    ")
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
    print("Income Simulation")
    print("Program By Mitchell Pomery")
    print("")
    print("")

if __name__=='__main__':
    print_info()
    print_argument_options()
    
    # Get experiment variables from command line arguments
    if len(sys.argv) > 1:
        citysize = int(sys.argv[1])
    else:
        citysize = 10
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
    print(cityprinter)
    for _ in range(1000):
        population.step()
    
    time2 = time.time()
    print('Simulation took %0.3f ms' % ((time2-time1) * 1000.0))
    
    print("Generating Image")
    cityprinter.create_heatmap()


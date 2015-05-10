
BIKE = 1
CAR = 2
TRUCK = 3


class Vehicle(object):
    def __init__(self, type=CAR, follow_distance=2, merge_distance=2, aggressiveness=0):
        self.type = type
        self.follow_distance = follow_distance
        self.merge_distance = merge_distance
        self.aggressiveness = aggressiveness
        self.lane = 0
        self.position = 0
    
    

class VehicleFactory(object)
    def car()
        return Vehicle()

class VehicleManager(object):
    def __init__(self, road, vehicles=[])
        self.vehicles = vehicles
        
    def step(self):
        pass
    
    def add(self, vehicles):
        if type(vehicles) == list:
            for vehicle in vehicles:
                self.vehicles.append(vehicle)
        elif type(vehicles) == Vehicle:
            self.vehicles.append(vehicles)
        else:
            raise TypeError("Expecting a list ot a Vehicle")
    


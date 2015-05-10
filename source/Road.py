class Road(object):
    """
    
    """
    def __init__(self, lanes):
        self.lanes = lanes
        self.roadend = max([_.laneend for _ in self.lanes])
        print([_.laneend for _ in self.lanes])
        print(self.roadend)
    
    def get_remaining_road(self, lane, location):
        pass
        
    def get_speed(self, lane, location):
        return self.lanes[lane].get_speed(location)
        
    def to_string(self):
        for i in range(self.roadend):
            toprint = str(i) + "\t"
            for j in range(len(self.lanes)):
                toprint += str(self.get_speed(j, i)) + "\t"
            print(toprint)

class Lane(object):
    """
    Create a new lane.
    sections is a list of tuples stating start and end points of the lane.
    speeds is a list of speeds for each section
    """
    def __init__(self, sections, speeds):
        if len(sections) != len(speeds):
            raise AttributeError("lengths of speed and sections are different")
        elif 0 in speeds:
            raise AttributeError("There is no need to specify zero speed areas")
        else:
            # Sort the two lists together
            combined = [(sections[_], speeds[_]) for _ in range(len(sections))]
            combined.sort(key=lambda tup: tup[0][0])
            # Split the combined list back out
            self.sections = [combined[_][0] for _ in range(len(combined))]
            self.speeds = [combined[_][1] for _ in range(len(combined))]
            # Check that sections don't overlap
            previous_end = 0
            for section in self.sections:
                if section[0] < previous_end:
                    raise ValueError("Section cannot start before another ends")
                elif section[0] >= section[1]:
                    raise ValueError("Section cannot stop before it has started")
                previous_end = section[1]
            # The end of the road
            self.laneend = previous_end
    
    """
    Get the speed of the lane at a certain location
    """
    def get_speed(self, location):
        search_result = [self.speeds[_] for _ in range(len(self.sections))
                if location >= self.sections[_][0] and location < self.sections[_][1]]
        return (search_result[0] if len(search_result) > 0 else 0)
    
    """
    Get the speed of the lane at a certain location
    """
    def remaining(self, location):
        #TODO: Impliment this
        pass
    



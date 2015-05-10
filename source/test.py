import Road

sections1 = [(0,10),(100,200),(10,100)]
speeds1 = [5,10,7]
lane1 = Road.Lane(sections1, speeds1)

sections2 = [(0,10),(10,100)]
speeds2 = [5,7]
lane2 = Road.Lane(sections2, speeds2)
speed1 = lane2.get_speed(5)
print("speed1 " + str(speed1))
speed2 = lane2.get_speed(10)
print("speed2 " + str(speed2))
speed3 = lane2.get_speed(101)
print("speed3 " + str(speed3))

sections3 = [(0,10),(9,100)]
speeds3 = [5,10]
try:
    lane3 = Road.Lane(sections3, speeds3)
except:
    print("lane3 failed as expected")

sections4 = [(0,10),(9,100)]
speeds4 = [5,10,100]
try:
    lane4 = Road.Lane(sections4, speeds4)
except:
    print("lane4 failed as expected")

sections5 = [(0,10),(11,11)]
speeds5 = [5,10]
try:
    lane5 = Road.Lane(sections5, speeds5)
except:
    print("lane5 failed as expected")

road1 = Road.Road([lane1, lane2])
road1.to_string()

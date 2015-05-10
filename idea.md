#Merging Traffic

##Intro
- Why is merging so hard
- whats the best way to merge
- what mistakes to people make

##Modelling Vehicles
- Give them an ID
- length as a unit
  - bike = 1
  - car = 2
  - truck = 3
- preferred distance behind
- preferred distance ahead of vehicles
- aggressiveness = how likely to change lanes

###Simplification

- All vehicles are cars (length 2)
- All 

##Modelling Roads
- Number lanes
- Each lane has a starting point and end point
- lanes have a speed limit
- Load road, then load cars
- Random selection of cars on road
- OR place them on road in order 

##Car Behaviour
- New lane starts = might swap
- Lane ending, only lane to right, merge right
- Lane ending, only lane to left, merge left
- Lane ending, lane to left and right, choose
- Lane to left/right going faster, choose depending on aggressiveness
 
##Step Behaviour
Cars move, frontmost cars get to move first



"""
Class that contains our entire world
"""
class City(object):
    def __init__(self, blocks_wide=3, blocks_high=3):
        self.blocks_wide = blocks_wide
        self.blocks_high = blocks_high
        self.blocks = [None for _ in range(blocks_wide * blocks_high)]
    
    def set_block(self, x, y, block):
        #print("Setting: " + str(y * self.blocks_high + x))
        self.blocks[y * self.blocks_high + x] = block
        
    def get_block(self, x, y):
        #print("Getting: " + str(y * self.blocks_high + x))
        return self.blocks[y * self.blocks_high + x]
    
    def print_city(self, blocks=False):
        if blocks:
            #TODO: Print Every House on Block
            printblocks = [None for _ in range(self.blocks_wide * self.blocks_high)]
            for y in range(self.blocks_high):
                for x in range(self.blocks_wide):
                    block = self.get_block(x, y)
                    printblocks[y * self.blocks_high + x] = block.to_string()
            overall = "-" * 111 + "\n"
            for y in range(self.blocks_high):
                for i in range(5):
                    toprint = ""
                    for x in range(self.blocks_wide):
                        toprint += printblocks[y * self.blocks_high + x].split("\n")[i]
                    overall += toprint + "|\n"
                overall += "-" * 111 + "\n"
            print(overall)
        else:
            # Print block averages
            for y in range(self.blocks_high):
                toprint = ""
                for x in range(self.blocks_wide):
                    block = self.get_block(x, y)
                    toprint += str(block.average_value()) + "\t"
                print(toprint)
    

class Block(object):
    def __init__(self, value=250):
        self.houses_wide = 5
        self.houses_high = 5
        self.houses = [value for _ in range(self.houses_wide * self.houses_high)]
    
    def average_value(self):
        numhouses = self.houses_wide * self.houses_high
        cumulative = sum(self.houses)
        return cumulative/numhouses
        
    def get_value(self, x, y):
        return self.houses[y * self.houses_high + x]
        
    def set_value(self, x, y, value):
        self.houses[y * self.houses_high + x] = value
    
    def to_string(self):
        lines = ""
        for y in range(self.houses_high):
            toprint = "| "
            for x in range(self.houses_wide):
                toprint += str("%3d " % self.get_value(x,y))
            lines += toprint + "\n"
        return lines

if __name__=='__main__':
    width = 5
    height = width
    city = City(width, height)
    for y in range(height):
        for x in range(width):
            block = Block(200 + x * 50 - 30 * y)
            city.set_block(x, y, block)
    city.print_city()
    city.print_city(True)
    
    




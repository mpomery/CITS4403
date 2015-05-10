import sys
import Vehicle
import Road

if __name__ == "__main__":
    road = Road.Road()
    manager = Vehicle.VehicleManager()
    try:
        try:
        timesteps = int(sys.argv[1])
    except:
        sys.stderr.write("Usage: python ants.py [timesteps]\n")
        sys.exit(1)

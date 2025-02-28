# Truck class to represent each delivery truck
class Truck:
    def __init__(self, packages=None, depart_time=None, capacity=16, speed=18, mileage=0.0, address="4001 South 700 East"):
        """
        Initialize a Truck object with its details.
        """
        self.capacity = capacity
        self.speed = speed
        self.load = 0  # Default load is 0 when initialized
        self.packages = packages if packages is not None else []
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        """
        Return a string representation of the truck's current state.
        """
        return f"Capacity: {self.capacity}, Speed: {self.speed} mph, Load: {self.load}, Mileage: {self.mileage} miles, Address: {self.address}, Departure Time: {self.depart_time}, Current Time: {self.time}"
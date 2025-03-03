#Salvador Amaya; 010348952
import csv
from datetime import timedelta
from HashTable import HashTable
from Package import Package
from Truck import Truck

# Load distance and address data
with open("data/distance-matrix.csv") as dist, open("data/address-table.csv") as addy:
    distance_csv = list(csv.reader(dist))
    address_csv = list(csv.reader(addy))

# Read and create Package objects, then load them into the hash table
with open("data/package-file.csv") as pkg:
    pkg_hash = HashTable()
    for package in (Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], "at the hub")
                    for row in csv.reader(pkg)):
        pkg_hash.insert(package.package_id, package)

# Function to get distance between two addresses
def get_distance(addy1, addy2):
    """
    Get the distance between two addresses.
    If the direct distance is not found, check the reverse.
    """
    distance = distance_csv[addy1][addy2] or distance_csv[addy2][addy1]
    return float(distance)
    
def get_index(address):
    """
    Extract the address index from the string literal of an address.
    Returns the index (as an integer) if found, otherwise returns None.
    """
    for row in address_csv:
        if address in row[2]:
            return int(row[0])
    return None

# Initialize truck objects
truck1 = Truck([1, 2, 4, 5, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], timedelta(hours=8))
truck2 = Truck([3, 6, 18, 25, 28, 32, 36, 38], timedelta(hours=9, minutes=5))
truck3 = Truck([7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27, 33, 35, 39], timedelta(hours=10, minutes=20))
trucks = [truck1, truck2, truck3]

def nearest_neighbor(truck):
    """
    Orders packages on a given truck using the nearest neighbor algorithm.
    Also calculates the distance the truck drives once the packages are sorted.
    """
    not_delivered = [pkg_hash.lookup(pkg_id) for pkg_id in truck.packages] # Collect packages to deliver

    truck.packages.clear() # Clear the truck's package list

    while not_delivered:
        next_package = None
        next_address = float('inf')
        
        # Find the nearest package to the current location
        for package in not_delivered:
            distance = get_distance(get_index(truck.address), get_index(package.address))
    
            if distance <= next_address:
                next_address = distance
                next_package = package
                
        # Update truck and package information
        truck.packages.append(next_package.package_id)
        not_delivered.remove(next_package)
        truck.mileage += next_address
        truck.address = next_package.address
        truck.time += timedelta(hours=next_address / truck.speed)

        # Update package delivery and departure times
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time

# Function to update the address for package #9
def update_package_address(pkg_id):
    if pkg_id == 9:
        pkg = pkg_hash.lookup(pkg_id)
        if pkg:
            pkg.address = "410 S. State St., Salt Lake City, UT 84111"  # Correct address
            print(f"Package {pkg_id} address corrected at 10:20 a.m. to: {pkg.address}")

# Execute nearest neighbor algorithm for truck routing
nearest_neighbor(truck1)
nearest_neighbor(truck2)

# Ensure truck 3 departs after the first two trucks have finished
truck3.depart_time = min(truck1.time, truck2.time)
nearest_neighbor(truck3)

class Main:
    '''
    Interactive user interface for the WGUPS routing program.
    Shows package details and total mileage.
    '''
    def __init__(self):
        print("Welcome to the WGUPS Routing Program")
        self.main_menu()

    def main_menu(self):
        start_input = input("Please type 'start' to begin: ").lower()
        if start_input == "start":
            self.show_menu()
        else:
            self.exit_program("Invalid entry; exiting the program.")

    def show_menu(self):
        print("Enter '1' to view package details")
        print("Enter '2' to view total mileage")
        print("Enter '3' to exit the program")
        
        choice = input("Select an option: ")
        if choice == "1":
            self.view_package_details()
        elif choice == "2":
            self.view_total_mileage()
        elif choice == "3":
            self.exit_program("Goodbye!")
        else:
            print("Invalid option; please try again.")
            self.show_menu()

    def view_package_details(self):
        try:
            time_input = input("At what time do you want to view the delivery status? (HH:MM or EOD) ")
            convert_time = self.time_input_to_timedelta(time_input)
            if convert_time is None:
                return

            # Update package address if it's 10:20 AM
            if convert_time == timedelta(hours=10, minutes=20):
                update_package_address(9)  # Correct address for package #9

            pkg_input = input("Type 'all' to view every package or 'one' for a single package: ").lower()
            if pkg_input == "one":
                self.view_single_package(convert_time)
            elif pkg_input == "all":
                self.view_all_packages(convert_time)
            else:
                print("Invalid option; please try again.")
                self.view_package_details()
        except ValueError:
            print("Invalid time format; please try again.")
            self.view_package_details()

    def view_single_package(self, convert_time):
        try:
            single_input = input("Please choose a package ID between 1 and 40: ")
            pkg_id = int(single_input)
            pkg = pkg_hash.lookup(pkg_id)
            if pkg:
                for i, truck in enumerate(trucks, start=1):
                    if pkg_id in truck.packages:
                        print(f'Truck {i} - {pkg.update_status(convert_time)}')
            else:
                print("Package not found; please try again.")
                self.view_single_package(convert_time)
        except ValueError:
            print("Invalid package ID; please try again.")
            self.view_single_package(convert_time)

    def view_all_packages(self, convert_time):
        try:
            for pkg_id in range(1, 41):
                pkg = pkg_hash.lookup(pkg_id)
                if pkg:
                    for i, truck in enumerate(trucks, start=1):
                        if pkg_id in truck.packages:
                            print(f'Truck {i} - {pkg.update_status(convert_time)}')
                            break  # No need to continue checking trucks once found
        except ValueError:
            self.exit_program("An error occurred; exiting the program.")

    def view_total_mileage(self):
        total_mileage = sum(truck.mileage for truck in trucks)
        for i, truck in enumerate(trucks, start=1):
            print(f'Truck {i} traveled {truck.mileage:.2f} miles.')
        print(f'The total distance traveled by all trucks is {total_mileage:.2f} miles.')

    def exit_program(self, message):
        print(message)
        exit()

    def time_input_to_timedelta(self, time_input):
        """
        Converts the user time input into a timedelta object.
        """
        try:
            if time_input.lower() == "eod":
                return timedelta(hours=17)
            else:
                hr, min = map(int, time_input.split(":"))
                return timedelta(hours=hr, minutes=min)
        except ValueError:
            print("Invalid time format; please use HH:MM or 'EOD'.")
            return None

# Run the program
if __name__ == "__main__":
    Main()

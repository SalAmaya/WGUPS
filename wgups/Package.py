from datetime import timedelta

class Package:
    
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, status):
        """
        Initialize a Package object with its details.
        """
        self.package_id = package_id
        self.original_address = address  # Keep the original address immutable
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def update_status(self, current_time):
        """
        Return a string representation of the package's status at a given time.
        This method does not modify the package object itself.
        """
        # Define the time when the address should be corrected (10:20 AM)
        cutoff_time = timedelta(hours=10, minutes=20)

        # Determine if we should use the corrected address for package 9
        address_to_use = self.original_address
        if self.package_id == 9 and current_time >= cutoff_time:
            address_to_use = "410 S State St, Salt Lake City, UT 84111"  # Corrected address after 10:20 AM
        elif self.package_id == 9 and current_time < cutoff_time:
            address_to_use = "Third District Juvenile Court"  # Original address before 10:20 AM

        # Determine the status and construct the status string
        if self.delivery_time and self.delivery_time <= current_time:
            status = f"Delivered at {self.delivery_time}."
        elif self.departure_time and self.departure_time <= current_time:
            status = f"En Route at {current_time}."
        else:
            status = f"At The Hub at {current_time}."

        # Return the formatted package details with the appropriate address
        return f'ID: {self.package_id}; Address: {address_to_use}, {self.city}, {self.state}, {self.zip_code}; Deadline: {self.deadline}; Weight: {self.weight} lbs; {status}'

    def __str__(self):
        """
        Return a string representation of the package's current state.
        """
        return f'ID: {self.package_id}; Address: {self.address}, {self.city}, {self.state}, {self.zip_code}; Deadline: {self.deadline}; Weight: {self.weight} lbs; Status: {self.status} at {self.delivery_time}.'

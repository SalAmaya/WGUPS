from datetime import timedelta, datetime

class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, status, note=None):
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
        self.note = note  # Any special note, e.g., delays or specific instructions

    def time_to_timedelta(self, time_str):
        """
        Converts a time string like '10:30 AM' or 'EOD' into a timedelta.
        """
        if time_str == "EOD":
            # Return a default 'end of day' value, e.g., 5:00 PM (17:00)
            return timedelta(hours=17)
        elif time_str == "Delayed on flight---will not arrive to depot until 9:05 am":
            return timedelta(hours=9, minutes=5)
        else:
            # Parse the 'HH:MM AM/PM' format
            time_obj = datetime.strptime(time_str, "%I:%M %p")
            return timedelta(hours=time_obj.hour, minutes=time_obj.minute)

    def update_status(self, current_time):
        """
        Return a string representation of the package's status at a given time.
        This method does not modify the package object itself.
        """
        # Define the cutoff time for corrected address for package 9 (10:20 AM)
        cutoff_time = timedelta(hours=10, minutes=20)

        # Correct address for Package #9 after 10:20 AM
        address_to_use = self.original_address
        if self.package_id == 9 and current_time >= cutoff_time:
            address_to_use = "410 S State St, Salt Lake City, UT 84111"  # Corrected address after 10:20 AM

        # Handle specific delayed packages
        if self.package_id == 6 and current_time < timedelta(hours=9, minutes=5):
            status = f"Delayed: Not yet at the hub (Delayed in flight). Will arrive at 9:05 AM."
        elif self.package_id == 6 and current_time >= timedelta(hours=9, minutes=5):
            status = f"Delivered at {self.delivery_time}."
        elif self.package_id == 18 and current_time < timedelta(hours=9, minutes=5):
            status = f"Delayed: Not yet at the hub (Delayed in flight). Will arrive at 9:05 AM."
        elif self.package_id == 18 and current_time >= timedelta(hours=9, minutes=5):
            status = f"Delivered at {self.delivery_time}."
        else:
            # For other packages, determine their status based on time
            if self.delivery_time and self.delivery_time <= current_time:
                status = f"Delivered at {self.delivery_time}."
            elif self.departure_time and self.departure_time <= current_time:
                status = f"En Route at {current_time}."
            else:
                status = f"At The Hub at {current_time}."

        # Return the formatted package details with the appropriate address
        return f'ID: {self.package_id}; Address: {address_to_use}, {self.city}, {self.state}, {self.zip_code}; Deadline: {self.deadline}; Weight: {self.weight} lbs; {status}'

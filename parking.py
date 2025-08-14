import datetime
import uuid
import math
import random

# Parking simulation
# Simulating vehicles entering the parking lot at random times


class Ticket:
    def __init__(self, vehicle_registration):
        self.__id = uuid.uuid4()
        self.__entry_time = datetime.datetime.now()
        self.__vehicle_registration = vehicle_registration
        self.__bar_code = self.generate_bar_code()

    def generate_bar_code(self):
        bar_code = (
            str(self.__id)
            + self.__vehicle_registration
            + self.__entry_time.strftime("%Y%m%d%H%M%S")
        ).replace("-", "")
        return bar_code

    # Getters
    def get_id(self):
        return self.__id

    def get_bar_code(self):
        return self.__bar_code

    def get_entry_time(self):
        return self.__entry_time

    def set_entry_time(self, new_time):
        """Used for simulation: set entry time to the past."""
        self.__entry_time = new_time

    def get_vehicle_registration(self):
        return self.__vehicle_registration


class ParkingService:
    def __init__(self, capacity=50, hourly_rate=120.0):
        self._capacity = capacity
        self._hourly_rate = hourly_rate
        self.__tickets = []

    def enter_vehicle(self, vehicle_registration):
        if len(self.__tickets) >= self._capacity:
            raise Exception("Parking is full")
        ticket = Ticket(vehicle_registration)

        # Simulate random parking duration between 1 and 8 hours ago
        random_hours = random.randint(1, 8)
        fake_entry_time = datetime.datetime.now() - datetime.timedelta(
            hours=random_hours
        )
        ticket.set_entry_time(fake_entry_time)

        self.__tickets.append(ticket)
        print(
            f"✅ Vehicle {vehicle_registration} entered ({random_hours}h ago for simulation)."
        )
        return ticket

    def find_ticket_by_id(self, ticket_id):
        for ticket in self.__tickets:
            if ticket.get_id() == ticket_id:
                return ticket
        return None

    def find_ticket_by_barcode(self, bar_code):
        for ticket in self.__tickets:
            if ticket.get_bar_code() == bar_code:
                return ticket
        return None

    def calculate_fee(self, ticket_id):
        ticket = self.find_ticket_by_id(ticket_id)
        if ticket:
            parked_duration = datetime.datetime.now() - ticket.get_entry_time()
            hours_parked = parked_duration.total_seconds() / 3600
            return math.ceil(hours_parked) * self._hourly_rate
        return 0

    def exit_vehicle(self, ticket_id):
        ticket = self.find_ticket_by_id(ticket_id)
        if ticket:
            fee = self.calculate_fee(ticket_id)
            self.__tickets.remove(ticket)
            print(
                f"🚗 Vehicle {ticket.get_vehicle_registration()} exited. Fee: {fee} RSD."
            )
            return fee
        return 0

    def show_parked_vehicles(self):
        if not self.__tickets:
            print("🅿 Parking is empty.")
            return
        print("\n📋 Currently Parked Vehicles:")
        print("-" * 60)
        for ticket in self.__tickets:
            time_str = ticket.get_entry_time().strftime("%d-%m-%Y-%H:%M")
            print(
                f"Reg: {ticket.get_vehicle_registration()} | Entry: {time_str} | Barcode: {ticket.get_bar_code()}"
            )
        print("-" * 60)


# Example usage
if __name__ == "__main__":  # Main entry point for the simulation
    garage = ParkingService()

    v1 = garage.enter_vehicle("BG1234AB")
    v2 = garage.enter_vehicle("NS5678CD")
    v3 = garage.enter_vehicle("NI9999EE")
    v4 = garage.enter_vehicle("CA5679LK")

    garage.show_parked_vehicles()

    garage.exit_vehicle(v1.get_id())
    garage.exit_vehicle(v2.get_id())

    garage.show_parked_vehicles()

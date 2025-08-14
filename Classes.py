import datetime
import uuid
import math


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
        self.__tickets.append(ticket)
        print(f"✅ Vehicle with registration {vehicle_registration} welcomed to the parking.")
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
            print(f"🚗 Vehicle with registration {ticket.get_vehicle_registration()} has exited. Fee: {fee} RSD.")
            return fee
        return 0

    def show_parked_vehicles(self):
        if not self.__tickets:
            print("🅿 Parking is empty.")
            return
        print("\n📋 Currently Parked Vehicles:")
        print("-" * 60)
        for ticket in self.__tickets:
            print(f"Reg: {ticket.get_vehicle_registration()} | Entry: {ticket.get_entry_time()} | Barcode: {ticket.get_bar_code()}")
        print("-" * 60)


# Example usage
if __name__ == "__main__":
    garage = ParkingService()
    
    v1 = garage.enter_vehicle("BG1234AB")
    v2 = garage.enter_vehicle("NS5678CD")
    
    garage.show_parked_vehicles()

    fee = garage.exit_vehicle(v1.get_id())
    print(f"Parking Fee for first car: {fee} RSD")

    garage.show_parked_vehicles()

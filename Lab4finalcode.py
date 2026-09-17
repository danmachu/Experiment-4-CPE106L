# Pet owner management
class Owner:

    def __init__(self, owner_id, name, contact_number):
        self.owner_id = owner_id
        self.name = name
        self.contact_number = contact_number

    def __str__(self):
        return f"[{self.owner_id}] {self.name} - {self.contact_number}"


class Pet:

    def __init__(self, name, owner_id):
        self.name = name
        self.owner_id = owner_id
        self.species = "Unknown"

    def __str__(self):
        return f"{self.name} ({self.species}) - Owner ID: {self.owner_id}"


# pet management
class Dog(Pet):
    def __init__(self, name, owner_id):
        super().__init__(name, owner_id)
        self.species = "Dog"


class Cat(Pet):
    def __init__(self, name, owner_id):
        super().__init__(name, owner_id)
        self.species = "Cat"


class Bird(Pet):
    def __init__(self, name, owner_id):
        super().__init__(name, owner_id)
        self.species = "Bird"


class Rabbit(Pet):
    def __init__(self, name, owner_id):
        super().__init__(name, owner_id)
        self.species = "Rabbit"


class PetFactory:

    _pet_types = {
        "dog": Dog,
        "cat": Cat,
        "bird": Bird,
        "rabbit": Rabbit,
    }

    @staticmethod
    def create_pet(pet_type, name, owner_id):
        pet_class = PetFactory._pet_types.get(pet_type.lower())
        if pet_class is None:
            raise ValueError(f"Unsupported pet type: {pet_type}")
        return pet_class(name, owner_id)


# appointment management
class Appointment:

    def __init__(self, appointment_id, pet_name, owner_id, date_time, status="Scheduled"):
        self.appointment_id = appointment_id
        self.pet_name = pet_name
        self.owner_id = owner_id
        self.date_time = date_time
        self.status = status

    def __str__(self):
        return f"[{self.appointment_id}] {self.pet_name} (Owner {self.owner_id}) - {self.date_time} - {self.status}"


# ---- input validation helpers ----
def is_valid_name(name):
    """True if name has letters/spaces/hyphens/apostrophes only - no digits."""
    stripped = name.replace(" ", "").replace("-", "").replace("'", "")
    return stripped.isalpha() if stripped else False


def is_valid_contact(contact):
    """True if contact is digits only, allowing spaces, dashes, or a leading +."""
    stripped = contact.replace(" ", "").replace("-", "")
    if stripped.startswith("+"):
        stripped = stripped[1:]
    return stripped.isdigit() and len(stripped) >= 7


# Singleton Pattern: one ClinicDatabase instance holds ALL clinic data
class ClinicDatabase:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.owners = {}
        self.pets = []
        self.appointments = []
        self._next_owner_id = 1
        self._next_appointment_id = 1

    # ---- owners ----
    def register_owner(self, name, contact_number):
        if not is_valid_name(name):
            raise ValueError("Owner name must contain letters only (no numbers).")
        if not is_valid_contact(contact_number):
            raise ValueError("Contact number must contain digits only (no letters), at least 7 digits.")
        owner_id = f"O{self._next_owner_id:03d}"
        self._next_owner_id += 1
        owner = Owner(owner_id, name, contact_number)
        self.owners[owner_id] = owner
        return owner

    # ---- pets ----
    def add_pet(self, pet_type, name, owner_id):
        if not is_valid_name(name):
            raise ValueError("Pet name must contain letters only (no numbers).")
        if owner_id not in self.owners:
            raise ValueError(f"Owner ID {owner_id} does not exist.")
        pet = PetFactory.create_pet(pet_type, name, owner_id)
        self.pets.append(pet)
        return pet

    def get_pet(self, owner_id, pet_name):
        for pet in self.pets:
            if pet.owner_id == owner_id and pet.name.lower() == pet_name.lower():
                return pet
        return None

    # ---- appointments ----
    def schedule_appointment(self, pet_name, owner_id, date_time):
        if owner_id not in self.owners:
            raise ValueError(f"Owner ID {owner_id} does not exist.")
        if self.get_pet(owner_id, pet_name) is None:
            raise ValueError(f"No pet named '{pet_name}' found for owner {owner_id}.")
        appointment_id = f"A{self._next_appointment_id:03d}"
        self._next_appointment_id += 1
        appointment = Appointment(appointment_id, pet_name, owner_id, date_time)
        self.appointments.append(appointment)
        return appointment

    def cancel_appointment(self, appointment_id):
        for appt in self.appointments:
            if appt.appointment_id == appointment_id:
                appt.status = "Cancelled"
                return appt
        raise ValueError(f"Appointment ID {appointment_id} not found.")

    def update_appointment_status(self, appointment_id, new_status):
        valid_statuses = ("Scheduled", "Completed", "Cancelled")
        if new_status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        for appt in self.appointments:
            if appt.appointment_id == appointment_id:
                appt.status = new_status
                return appt
        raise ValueError(f"Appointment ID {appointment_id} not found.")


def print_menu():
    print("\n===== Paws and Care Veterinary Clinic =====")
    print("1. Register Pet Owner")
    print("2. View Pet Owners")
    print("3. Add Pet Record")
    print("4. View Pets")
    print("5. Schedule Appointment")
    print("6. View Appointments")
    print("7. Cancel Appointment")
    print("8. Update Appointment Status")
    print("0. Exit")


def run_app():
    db = ClinicDatabase()

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Owner name: ").strip()
            contact = input("Contact number: ").strip()
            try:
                owner = db.register_owner(name, contact)
                print(f"Registered: {owner}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            if not db.owners:
                print("No owners registered yet.")
            for o in db.owners.values():
                print(o)

        elif choice == "3":
            owner_id = input("Owner ID: ").strip()
            pet_type = input("Pet type (Dog/Cat/Bird/Rabbit): ").strip()
            name = input("Pet name: ").strip()
            try:
                pet = db.add_pet(pet_type, name, owner_id)
                print(f"Added pet: {pet}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            owner_id = input("Filter by Owner ID (blank = all): ").strip() or None
            filtered = [p for p in db.pets if owner_id is None or p.owner_id == owner_id]
            if not filtered:
                print("No pets found.")
            for p in filtered:
                print(p)

        elif choice == "5":
            owner_id = input("Owner ID: ").strip()
            pet_name = input("Pet name: ").strip()
            date_time = input("Date and time (e.g., 2026-09-20 14:30): ").strip()
            try:
                appt = db.schedule_appointment(pet_name, owner_id, date_time)
                print(f"Scheduled: {appt}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "6":
            if not db.appointments:
                print("No appointments yet.")
            for a in db.appointments:
                print(a)

        elif choice == "7":
            appointment_id = input("Appointment ID to cancel: ").strip()
            try:
                appt = db.cancel_appointment(appointment_id)
                print(f"Cancelled: {appt}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "8":
            appointment_id = input("Appointment ID: ").strip()
            new_status = input("New status (Scheduled/Completed/Cancelled): ").strip()
            try:
                appt = db.update_appointment_status(appointment_id, new_status)
                print(f"Updated: {appt}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "0":
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run_app()
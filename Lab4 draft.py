#Pet owner management
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

#pet management
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

#test

owners = {}
pets = []
_next_owner_id = 1


def register_owner(name, contact_number):
    global _next_owner_id
    owner_id = f"O{_next_owner_id:03d}"
    _next_owner_id += 1
    owner = Owner(owner_id, name, contact_number)
    owners[owner_id] = owner
    return owner


def add_pet(pet_type, name, owner_id):
    if owner_id not in owners:
        raise ValueError(f"Owner ID {owner_id} does not exist.")
    pet = PetFactory.create_pet(pet_type, name, owner_id)
    pets.append(pet)
    return pet


def print_menu():
    print("\n===== Paws and Care Veterinary Clinic =====")
    print("1. Register Pet Owner")
    print("2. View Pet Owners")
    print("3. Add Pet Record")
    print("4. View Pets")
    print("0. Exit")


def run_app():
    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Owner name: ").strip()
            contact = input("Contact number: ").strip()
            owner = register_owner(name, contact)
            print(f"Registered: {owner}")

        elif choice == "2":
            if not owners:
                print("No owners registered yet.")
            for o in owners.values():
                print(o)

        elif choice == "3":
            owner_id = input("Owner ID: ").strip()
            pet_type = input("Pet type (Dog/Cat/Bird/Rabbit): ").strip()
            name = input("Pet name: ").strip()
            try:
                pet = add_pet(pet_type, name, owner_id)
                print(f"Added pet: {pet}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            owner_id = input("Filter by Owner ID (blank = all): ").strip() or None
            filtered = [p for p in pets if owner_id is None or p.owner_id == owner_id]
            if not filtered:
                print("No pets found.")
            for p in filtered:
                print(p)

        elif choice == "0":
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run_app()
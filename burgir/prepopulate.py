import os
import django
import random

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burgir.settings")  # Replace with your project's settings
django.setup()

from app.models import User, Table, MenuItem

# New number finders:

def get_next_available_user_number():
    """
    Finds the next available number for a username in the format 'UserX'.
    """
    existing_users = User.objects.filter(name__startswith="User").values_list("name", flat=True)
    
    used_numbers = set()
    for name in existing_users:
        if name.startswith("User") and name[4:].isdigit():
            used_numbers.add(int(name[4:]))
    
    new_number = 0
    while new_number in used_numbers:
        new_number += 1

    return new_number

def get_next_available_item_number(item_type):
    """
    Finds the next available number for a menu item with the given type.
    
    Args:
        item_type (str): The type of the menu item (e.g., "main course", "drink").
    
    Returns:
        int: The next available number for that item type.
    """
    existing_items = MenuItem.objects.filter(name__startswith=item_type).values_list("name", flat=True)
    
    used_numbers = set()
    for name in existing_items:
        parts = name.split()
        if len(parts) > 1 and parts[-1].isdigit():
            used_numbers.add(int(parts[-1]))

    new_number = 1
    while new_number in used_numbers:
        new_number += 1

    return new_number

# Population functions:

def populate_users(n=10):
    """
    Populates the User model with random user data.

    Args:
        n (int): Number of users to create.
    """
    users_created = 0
    for i in range(n):
        new_number = get_next_available_user_number()
        name = f"User{new_number}"
        
        user = User.objects.create(name=name)
        users_created += 1
        print(f"Created User {user.id}: {name}")

    print(f"\nSuccessfully created {users_created} users.\n")

def populate_tables(n=10):
    """
    Populates the Table model with random table data.

    Args:
        n (int): Number of tables to create.
    """
    tables_created = 0

    for _ in range(n):
        min_people = random.randint(1, 4)  # Random minimum capacity
        max_people = random.randint(min_people + 1, min_people + 6)  # Ensure max > min
        
        table = Table.objects.create(min_people=min_people, max_people=max_people)
        tables_created += 1
        print(f"Created Table {table.id}: Min {min_people}, Max {max_people}")

    print(f"\nSuccessfully created {tables_created} tables.")

def populate_menuitem(n=10):
    """
    Populates the MenuItem model with random data.

    Args:
        n (int): Number of menu items to create.
    """
    item_types = ["main course", "drink", "appetizer", "snack", "dessert"]
    menuitems_created = 0

    for i in range(n):
        item_type = random.choice(item_types)
        new_number = get_next_available_item_number(item_type)
        name = f"{item_type} {new_number}"
        description = f"Description for {item_type} {i + 1}"
        price = round(random.uniform(5.0, 35.0), 2)
        
        menu_item = MenuItem.objects.create(name=name, description=description, type=item_type, price=price)
        menuitems_created += 1
        print(f"Created MenuItem {menu_item.id}: {name}")

    print(f"\nSuccessfully created {menuitems_created} menu items.\n")

# Run the script
if __name__ == "__main__":
    # Adjust the number as needed
    n = 5
    populate_users(n)
    populate_tables(n)
    populate_menuitem(n)
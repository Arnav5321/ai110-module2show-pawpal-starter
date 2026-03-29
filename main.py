"""
Testing ground for PawPal+ System
This script demonstrates creating an owner, pets, and tasks, then displays today's schedule.
"""

from pawpal_system import Owner, Pet, Task


def main():
    # Create an Owner
    owner = Owner(
        name="Sarah",
        available_time_minutes=120,
        preferences={"preferred_walk_time": "morning"}
    )
    
    # Create Pets
    dog = Pet(
        name="Max",
        species="Golden Retriever",
        age=3,
        dietary_restrictions=["grain-free"]
    )
    
    cat = Pet(
        name="Whiskers",
        species="Tabby Cat",
        age=5,
        dietary_restrictions=[]
    )
    
    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Create and add tasks to Max (dog)
    task1 = Task(
        title="Morning Walk",
        duration_minutes=30,
        priority="high",
        category="walk",
        frequency="daily"
    )
    
    task2 = Task(
        title="Feeding",
        duration_minutes=10,
        priority="high",
        category="feeding",
        frequency="daily"
    )
    
    task3 = Task(
        title="Playtime",
        duration_minutes=20,
        priority="medium",
        category="play",
        frequency="daily"
    )
    
    dog.add_task(task1)
    dog.add_task(task2)
    dog.add_task(task3)
    
    # Create and add tasks to Whiskers (cat)
    task4 = Task(
        title="Litter Box Cleaning",
        duration_minutes=5,
        priority="high",
        category="grooming",
        frequency="daily"
    )
    
    task5 = Task(
        title="Feeding",
        duration_minutes=5,
        priority="high",
        category="feeding",
        frequency="daily"
    )
    
    task6 = Task(
        title="Interactive Play",
        duration_minutes=15,
        priority="medium",
        category="play",
        frequency="daily"
    )
    
    cat.add_task(task4)
    cat.add_task(task5)
    cat.add_task(task6)
    
    # Print Today's Schedule
    print("=" * 50)
    print("TODAY'S SCHEDULE")
    print("=" * 50)
    print(f"\nOwner: {owner.name}")
    print(f"Available Time: {owner.available_time_minutes} minutes\n")
    
    # Display tasks for each pet
    all_tasks = owner.get_all_tasks()
    total_duration = sum(task.duration_minutes for task in all_tasks)
    
    for pet in owner.pets:
        print(f"\n--- {pet.name.upper()} ({pet.species}) ---")
        for task in pet.get_tasks():
            status = "✓" if task.completed else "○"
            print(f"{status} {task.title:<25} | {task.duration_minutes:>3} min | Priority: {task.priority}")
    
    print(f"\n{'=' * 50}")
    print(f"Total Tasks: {len(all_tasks)}")
    print(f"Total Time Required: {total_duration} minutes")
    print(f"{'=' * 50}\n")


if __name__ == "__main__":
    main()

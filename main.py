"""
Testing ground for PawPal+ System
This script demonstrates creating an owner, pets, and tasks, then displays today's schedule.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


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
        frequency="daily",
        scheduled_time="07:30"
    )
    
    task2 = Task(
        title="Feeding",
        duration_minutes=10,
        priority="high",
        category="feeding",
        frequency="daily",
        scheduled_time="08:00"
    )
    
    task3 = Task(
        title="Playtime",
        duration_minutes=20,
        priority="medium",
        category="play",
        frequency="daily",
        scheduled_time="19:00"
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
        frequency="daily",
        scheduled_time="09:00"
    )
    
    task5 = Task(
        title="Feeding",
        duration_minutes=5,
        priority="high",
        category="feeding",
        frequency="daily",
        scheduled_time="08:30"
    )
    
    task6 = Task(
        title="Interactive Play",
        duration_minutes=15,
        priority="medium",
        category="play",
        frequency="daily",
        scheduled_time="17:00"
    )
    
    # Add intentional conflict tasks (same time) for conflict detection
    task7 = Task(
        title="Quick Checkup",
        duration_minutes=10,
        priority="medium",
        category="grooming",
        frequency="as-needed",
        scheduled_time="08:00"
    )
    task8 = Task(
        title="Extra Feeding",
        duration_minutes=5,
        priority="high",
        category="feeding",
        frequency="as-needed",
        scheduled_time="08:00"
    )
    
    cat.add_task(task4)
    cat.add_task(task5)
    cat.add_task(task6)
    dog.add_task(task7)
    cat.add_task(task8)
    
    # Print Today's schedule
    print("=" * 50)
    print("TODAY'S SCHEDULE")
    print("=" * 50)
    print(f"\nOwner: {owner.name}")
    print(f"Available Time: {owner.available_time_minutes} minutes\n")
    
    all_tasks = owner.get_all_tasks()
    total_duration = sum(task.duration_minutes for task in all_tasks)
    
    # Initial unordered tasks (the order they were added)
    print("\n--- TASKS IN ADDED ORDER ---")
    for task in all_tasks:
        status = "✓" if task.completed else "○"
        print(f"{task.scheduled_time} {status} {task.title:<20} | {task.duration_minutes:>3} min | {task.priority}")

    # Sort by scheduled_time via Scheduler.sort_by_time
    scheduler = Scheduler()
    tasks_sorted = scheduler.sort_by_time(all_tasks)
    print("\n--- TASKS SORTED BY TIME ---")
    for task in tasks_sorted:
        status = "✓" if task.completed else "○"
        print(f"{task.scheduled_time} {status} {task.title:<20} | {task.duration_minutes:>3} min | {task.priority}")

    # Mark one recurring task complete and generate next occurrence
    print("\n--- MARK TASK COMPLETE (RECURRING) ---")
    recurring_next = scheduler.mark_task_complete(dog, task1)
    if recurring_next:
        print(f"Completed '{task1.title}' and added new occurrence for {recurring_next.due_date} at {recurring_next.scheduled_time}")

    # Recompute all tasks and total duration after recurrence update
    all_tasks = owner.get_all_tasks()
    total_duration = sum(task.duration_minutes for task in all_tasks)

    conflict_warnings = scheduler.detect_conflicts(owner)
    print("\n--- CONFLICT DETECTION ---")
    if conflict_warnings:
        for warning in conflict_warnings:
            print(warning)
    else:
        print("No conflicts detected.")

    # Filter by pet name (Whiskers) and incomplete only
    whiskers_tasks = scheduler.filter_tasks(owner, completed=False, pet_name="Whiskers")
    print("\n--- INCOMPLETE TASKS FOR WHISKERS ---")
    for task in whiskers_tasks:
        print(f"{task.scheduled_time} {task.title:<20} | {task.duration_minutes:>3} min | {task.priority}")

    print(f"\n{'=' * 50}")
    print(f"Total Tasks: {len(all_tasks)}")
    print(f"Total Time Required: {total_duration} minutes")
    print(f"{'=' * 50}\n")


if __name__ == "__main__":
    main()

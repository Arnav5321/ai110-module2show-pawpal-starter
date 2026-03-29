"""
PawPal+ System - Core Logic Layer

This module contains the domain models and scheduling logic for the pet care application.
Uses dataclasses for clean, maintainable data models.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet care activity."""
    title: str
    duration_minutes: int
    priority: str  # 'low', 'medium', 'high'
    category: str  # 'walk', 'feeding', 'grooming', etc.
    frequency: str  # 'daily', 'weekly', 'as-needed'
    scheduled_time: str = "00:00"  # 'HH:MM' format for sorting
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    
    def mark_completed(self) -> Optional['Task']:
        """Mark the task as completed, and return the next occurrence for recurring tasks."""
        self.completed = True

        if self.frequency == 'daily':
            next_due_date = self.due_date + timedelta(days=1)
        elif self.frequency == 'weekly':
            next_due_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            frequency=self.frequency,
            scheduled_time=self.scheduled_time,
            due_date=next_due_date,
            completed=False,
        )
    
    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completed = False
    
    def get_priority_level(self) -> int:
        """Return numeric priority level (higher = more urgent)."""
        priority_map = {'low': 1, 'medium': 2, 'high': 3}
        return priority_map.get(self.priority.lower(), 1)


@dataclass
class Pet:
    """Represents a pet being cared for."""
    name: str
    species: str
    age: int
    dietary_restrictions: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        if task not in self.tasks:
            self.tasks.append(task)
    
    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)
    
    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks
    
    def get_incomplete_tasks(self) -> List[Task]:
        """Return only incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Represents a pet owner and their constraints."""
    name: str
    available_time_minutes: int
    preferences: dict = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's collection."""
        if pet not in self.pets:
            self.pets.append(pet)
    
    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's collection."""
        if pet in self.pets:
            self.pets.remove(pet)
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all of the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
    
    def get_all_incomplete_tasks(self) -> List[Task]:
        """Retrieve all incomplete tasks from all of the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_incomplete_tasks())
        return all_tasks


class Scheduler:
    """Orchestrator that manages and organizes pet care tasks."""
    
    def retrieve_all_tasks(self, owner: Owner) -> List[Task]:
        """
        Retrieve all tasks from the owner's pets.
        
        Args:
            owner: The Owner whose pets' tasks to retrieve
            
        Returns:
            List of all tasks across all the owner's pets
        """
        return owner.get_all_tasks()
    
    def organize_tasks(self, tasks: List[Task], available_time: int) -> List[Task]:
        """
        Organize and sort tasks by priority, fitting them within available time.
        
        Args:
            tasks: List of tasks to organize
            available_time: Available minutes for scheduling
            
        Returns:
            Sorted list of tasks that fit within available time
        """
        # Sort by priority (highest first), then by duration (shortest first)
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (-t.get_priority_level(), t.duration_minutes)
        )
        
        # Filter tasks that fit in available time
        total_time = 0
        scheduled = []
        for task in sorted_tasks:
            if total_time + task.duration_minutes <= available_time:
                scheduled.append(task)
                total_time += task.duration_minutes
        
        return scheduled
    
    def generate_schedule(self, owner: Owner) -> List[Task]:
        """
        Generate an optimized daily schedule for the owner's pets.
        
        Args:
            owner: The Owner for whom to generate a schedule
            
        Returns:
            Organized list of tasks that fit within the owner's available time
        """
        # Retrieve all incomplete tasks
        all_tasks = owner.get_all_incomplete_tasks()
        
        # Organize and filter by available time
        organized_tasks = self.organize_tasks(all_tasks, owner.available_time_minutes)
        
        return organized_tasks

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by `scheduled_time` in HH:MM format."""
        # Use sorted() with a lambda key for HH:MM strings
        return sorted(tasks, key=lambda t: tuple(int(x) for x in t.scheduled_time.split(':')))

    def mark_task_complete(self, pet: Pet, task: Task) -> Optional[Task]:
        """Mark a task complete and create the next occurrence if recurring."""
        next_task = task.mark_completed()
        if next_task:
            pet.add_task(next_task)
        return next_task

    def detect_conflicts(self, owner: Owner) -> List[str]:
        """Lightweight conflict detection for overlapping scheduled task times."""
        key_map = {}
        warnings = []

        for pet in owner.pets:
            for task in pet.get_tasks():
                key = (task.due_date, task.scheduled_time)
                if key in key_map:
                    existing_pet, existing_task = key_map[key]
                    warning = (
                        f"Conflict: {pet.name} ({task.title}) and "
                        f"{existing_pet.name} ({existing_task.title}) both at {task.scheduled_time} on {task.due_date}"
                    )
                    warnings.append(warning)
                else:
                    key_map[key] = (pet, task)

        return warnings

    def filter_tasks(self, owner: Owner, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter owner's tasks by completion status and/or pet name."""
        filtered_tasks = []
        for pet in owner.pets:
            if pet_name and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                filtered_tasks.append(task)
        return filtered_tasks

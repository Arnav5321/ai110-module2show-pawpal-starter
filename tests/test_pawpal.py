"""
Unit tests for PawPal+ System
Tests core functionality of Task and Pet classes.
"""

import pytest
from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTaskCompletion:
    """Tests for task completion functionality."""
    
    def test_mark_task_completed(self):
        """Verify that calling mark_completed() changes the task's status."""
        # Arrange
        task = Task(
            title="Morning Walk",
            duration_minutes=30,
            priority="high",
            category="walk",
            frequency="daily"
        )
        
        # Assert initial state
        assert task.completed is False
        
        # Act
        task.mark_completed()
        
        # Assert
        assert task.completed is True
    
    def test_mark_task_incomplete(self):
        """Verify that calling mark_incomplete() changes task back to incomplete."""
        # Arrange
        task = Task(
            title="Feeding",
            duration_minutes=10,
            priority="high",
            category="feeding",
            frequency="daily",
            completed=True
        )
        
        # Assert initial state
        assert task.completed is True
        
        # Act
        task.mark_incomplete()
        
        # Assert
        assert task.completed is False


class TestTaskAddition:
    """Tests for adding tasks to pets."""
    
    def test_add_task_to_pet_increases_count(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        # Arrange
        pet = Pet(
            name="Max",
            species="Golden Retriever",
            age=3
        )
        task = Task(
            title="Playtime",
            duration_minutes=20,
            priority="medium",
            category="play",
            frequency="daily"
        )
        
        # Assert initial state
        assert len(pet.get_tasks()) == 0
        
        # Act
        pet.add_task(task)
        
        # Assert
        assert len(pet.get_tasks()) == 1
        assert task in pet.get_tasks()
    
    def test_add_multiple_tasks_to_pet(self):
        """Verify that multiple tasks can be added to a pet."""
        # Arrange
        pet = Pet(
            name="Whiskers",
            species="Tabby Cat",
            age=5
        )
        task1 = Task(
            title="Feeding",
            duration_minutes=5,
            priority="high",
            category="feeding",
            frequency="daily"
        )
        task2 = Task(
            title="Litter Box Cleaning",
            duration_minutes=5,
            priority="high",
            category="grooming",
            frequency="daily"
        )
        task3 = Task(
            title="Interactive Play",
            duration_minutes=15,
            priority="medium",
            category="play",
            frequency="daily"
        )
        
        # Act
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Assert
        assert len(pet.get_tasks()) == 3
        assert task1 in pet.get_tasks()
        assert task2 in pet.get_tasks()
        assert task3 in pet.get_tasks()


class TestScheduler:
    """Tests for scheduling utility methods."""

    def test_sort_by_time_returns_chronological_order(self):
        scheduler = Scheduler()
        tasks = [
            Task(title="Evening", duration_minutes=30, priority="low", category="play", frequency="daily", scheduled_time="19:00"),
            Task(title="Morning", duration_minutes=20, priority="high", category="walk", frequency="daily", scheduled_time="07:30"),
            Task(title="Noon", duration_minutes=15, priority="medium", category="feeding", frequency="daily", scheduled_time="12:00"),
        ]

        sorted_tasks = scheduler.sort_by_time(tasks)

        assert [t.title for t in sorted_tasks] == ["Morning", "Noon", "Evening"]

    def test_mark_task_complete_creates_next_daily_occurrence(self):
        scheduler = Scheduler()
        realistic_due_date = date.today()
        pet = Pet(name="Max", species="Dog", age=3)

        task = Task(
            title="Morning Walk",
            duration_minutes=30,
            priority="high",
            category="walk",
            frequency="daily",
            scheduled_time="07:30",
            due_date=realistic_due_date,
        )

        pet.add_task(task)

        next_task = scheduler.mark_task_complete(pet, task)

        assert task.completed is True
        assert next_task is not None
        assert next_task.due_date == realistic_due_date + timedelta(days=1)
        assert next_task.scheduled_time == "07:30"
        assert next_task.completed is False
        assert next_task in pet.get_tasks()

    def test_detect_conflicts_reports_exact_time_matches(self):
        scheduler = Scheduler()
        owner = Owner(name="Sarah", available_time_minutes=180)
        dog = Pet(name="Max", species="Dog", age=3)
        cat = Pet(name="Whiskers", species="Cat", age=5)

        task_dog = Task(
            title="Morning Walk",
            duration_minutes=30,
            priority="high",
            category="walk",
            frequency="daily",
            scheduled_time="08:00",
            due_date=date.today(),
        )
        task_cat = Task(
            title="Feeding",
            duration_minutes=10,
            priority="high",
            category="feeding",
            frequency="daily",
            scheduled_time="08:00",
            due_date=date.today(),
        )

        dog.add_task(task_dog)
        cat.add_task(task_cat)
        owner.add_pet(dog)
        owner.add_pet(cat)

        warnings = scheduler.detect_conflicts(owner)

        assert len(warnings) == 1
        assert "Conflict" in warnings[0]
        assert "08:00" in warnings[0]


"""
Unit tests for PawPal+ System
Tests core functionality of Task and Pet classes.
"""

import pytest
from pawpal_system import Task, Pet, Owner


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

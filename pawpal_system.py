"""
PawPal+ System - Core Logic Layer

This module contains the domain models and scheduling logic for the pet care application.
Uses dataclasses for clean, maintainable data models.
"""

from dataclasses import dataclass, field
from typing import List
from datetime import date


@dataclass
class Pet:
    """Represents a pet being cared for."""
    name: str
    species: str
    age: int
    dietary_restrictions: List[str] = field(default_factory=list)


@dataclass
class Owner:
    """Represents a pet owner and their constraints."""
    name: str
    available_time_minutes: int
    preferences: dict = field(default_factory=dict)


@dataclass
class Task:
    """Represents a single pet care task."""
    title: str
    duration_minutes: int
    priority: str  # 'low', 'medium', 'high'
    category: str  # 'walk', 'feeding', 'grooming', etc.


@dataclass
class Schedule:
    """Represents an ordered daily pet care plan."""
    tasks: List[Task]
    owner: Owner
    pet: Pet
    date: date
    
    def generate(self) -> None:
        """Generate an optimized schedule based on constraints and priorities."""
        pass
    
    def explain(self) -> str:
        """Return a human-readable explanation of the schedule reasoning."""
        pass


class Scheduler:
    """Orchestrator that contains the core scheduling logic."""
    
    def schedule_day(self, owner: Owner, pet: Pet, available_tasks: List[Task]) -> Schedule:
        """
        Build an ordered daily plan that fits tasks into available time.
        
        Args:
            owner: The pet owner with time constraints
            pet: The pet to schedule care for
            available_tasks: List of tasks to potentially schedule
            
        Returns:
            A Schedule object containing ordered tasks and explanation
        """
        pass

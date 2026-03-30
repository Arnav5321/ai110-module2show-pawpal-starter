# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The core classes would be: Pet, Owner, Task, Schedule, Scheduler.

Pet
    Attributes: name, species, age, dietary_restrictions
    Responsibilities: Represent the pet being cared for
Owner
    Attributes: name, available_time_minutes, preferences
    Responsibilities: Represent the owner and their constraints
Task
    Attributes: title, duration_minutes, priority (low/medium/high), category (walk/feeding/grooming/etc.)
    Responsibilities: Represent a single pet care task
Schedule
    Attributes: tasks (list of Task), owner, pet, date
    Methods: generate(), explain()
    Responsibilities: Build an ordered daily plan and explain reasoning
Scheduler (orchestrator)
    Methods: schedule_day(owner, pet, available_tasks)
    Responsibilities: Contains the core scheduling logic (sorting, filtering, fitting tasks into time)

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

It did change, and it's because having a Schedule and a Scheduler is redundant.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  - The scheduler considers available time, task priority, and task duration.

- How did you decide which constraints mattered most?
  - Priority was prioritized first because high-priority tasks (like feeding) must happen regardless of time. Duration was secondary to maximize the number of tasks scheduled within the time budget. Preferences were deferred for MVP simplicity, as they add complexity without core functionality.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  - Current conflict detection checks only exact `due_date` + `scheduled_time` matches (not interval overlaps), which is simpler and faster but can miss tasks that overlap by duration.
- Why is that tradeoff reasonable for this scenario?
  - For MVP scheduling, exact-time collisions are a lightweight guardrail that avoids complexity of full interval intersection logic, and it is easier to reason about in a small pet-care context.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

- Copilot was instrumental in:
  - Phase 1: Brainstormed UML design and class structure (partly)
  - Phase 2: Built `Pet.add_task()`, `Owner.add_pet()` class methods per direction
  - Phase 3: Generated `sort_by_time()` with lambda key optimization for HH:MM parsing, `mark_task_complete()` with `timedelta` recurrence, and `detect_conflicts()` logic
  - Phase 4: Drafted unit tests for sorting, recurrence, and conflict detection
- Most helpful prompts:
  - "#file:pawpal_system.py — How should I sort Task objects by their scheduled_time in HH:MM format?"
  - "What are the edge cases for a pet care scheduler with recurring tasks?"

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

- One example: Copilot suggested a "pure Pythonic" version of `sort_by_time()` using direct string comparison, but I kept the explicit `tuple(int(...))` approach because:
  - It's more defensive (handles "8:00" vs "08:00" format variations).
  - Readability is slightly better for team members unfamiliar with HH:MM lexicographic ordering.

- I verified by adding test cases that checked chronological correctness.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  - Task completion state transitions (`mark_completed` / `mark_incomplete`)
  - Time-based sorting correctness (tasks in chronological order)
  - Recurrence logic (daily task creates next-day instance with `timedelta`)
  - Conflict detection (two tasks at same date/time are flagged)
  - Pet/Owner/Scheduler integration (adding/filtering tasks)

- Why were these tests important?
  - Core scheduling logic must be bulletproof; users trust daily plans.
  - Recurrence is the "magic feature"; if it breaks, owners miss tasks.
  - Conflict warnings prevent schedule collisions that confuse pet owners.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  - **4/5 stars** — Happy paths are solid, but edge cases (e.g., long-running plans, duration overlaps, timezone handling) are not fully explored.
- What edge cases would you test next if you had more time?
  - Tasks spanning midnight (e.g., 23:00–01:30)
  - Leap-second or DST transitions
  - Very large task duration (>24 hours)
  - Owners with 0 available time
  - Pets with 50+ tasks

---

## 5. Reflection

**a. What went well**

- The separation of concerns (Task, Pet, Owner, Scheduler) is clean and easy to test.
- Streamlit integration was smooth; users can immediately see the scheduler in action.
- AI collaboration accelerated the build; I could focus on architecture.

**b. What you would improve**

- Replace the simple conflict check with duration-aware interval overlaps.
- Add persistent storage (SQLite or cloud) so plans survive app restarts.
- Implement "explain scheduling" feature: "Why was task X chosen over Y?"
- Add preference-based constraints (e.g., "owner prefers walks before 9 AM").

**c. Key takeaway**

- Being the "lead architect" with AI collaboration means staying critical, the human vision comes first, and before merging suggestions it's important to understand the code.


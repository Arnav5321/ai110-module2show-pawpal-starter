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
- How did you decide which constraints mattered most?

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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

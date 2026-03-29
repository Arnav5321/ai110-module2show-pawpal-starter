import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file now connects the UI to the backend system classes.
"""
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time_minutes=240)

owner_name = st.text_input("Owner name", st.session_state.owner.name)
st.session_state.owner.name = owner_name

st.divider()

st.subheader("Pets")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"], index=0)
age = st.number_input("Age", min_value=0, max_value=30, value=2)

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species, age=age)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added pet: {new_pet.name} ({new_pet.species})")

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species, "age": p.age} for p in st.session_state.owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Tasks")
st.caption("Add a task and assign it to an existing pet.")

if st.session_state.owner.pets:
    selected_pet_name = st.selectbox("Assign task to pet", [p.name for p in st.session_state.owner.pets])
    selected_pet = next((p for p in st.session_state.owner.pets if p.name == selected_pet_name), None)
else:
    selected_pet = None

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

category = st.selectbox("Category", ["walk", "feeding", "grooming", "other"], index=0)
frequency = st.selectbox("Frequency", ["daily", "weekly", "as-needed"], index=0)

if st.button("Add task"):
    if selected_pet is None:
        st.warning("Add a pet first before adding tasks.")
    else:
        new_task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            category=category,
            frequency=frequency,
        )
        selected_pet.add_task(new_task)
        st.success(f"Added task '{new_task.title}' to {selected_pet.name}")

if st.session_state.owner.get_all_tasks():
    st.write("Current tasks across pets:")
    st.table([
        {
            "pet": p.name,
            "title": t.title,
            "duration": t.duration_minutes,
            "priority": t.priority,
            "category": t.category,
            "frequency": t.frequency,
            "completed": t.completed,
        }
        for p in st.session_state.owner.pets
        for t in p.tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Click to generate a schedule from prefs/tasks.")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    schedule = scheduler.generate_schedule(st.session_state.owner)
    if not schedule:
        st.warning("No tasks can be scheduled. Add tasks or increase available time.")
    else:
        st.write("Generated schedule:")
        st.table([
            {
                "pet": next(p.name for p in st.session_state.owner.pets if t in p.tasks),
                "title": t.title,
                "duration": t.duration_minutes,
                "priority": t.priority,
            }
            for t in schedule
        ])

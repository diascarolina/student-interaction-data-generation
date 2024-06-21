from main import Simulation

rooms_and_objects_dict = {
    "Classroom": ["Desk", "Book", "Computer"],
    "Auditorium": ["Chair1", "Screen", "Hand"],
    "Café": ["Chair2", "Student", "Table"],
}


sim = Simulation(num_users=100,
                 rooms_and_objects=rooms_and_objects_dict,
                 duration=200,  # ano letivo
                 start_date="2024-01-01",
                 generate_csv_file=True)

sim.run_simulation()

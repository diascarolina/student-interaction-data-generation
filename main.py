from faker import Faker
import datetime
import math
import pandas as pd
import random
import time

random_seed = 456
fake = Faker(locale='pt_BR')
Faker.seed(random_seed)

# Engagement level

# 1: low
# 2: average
# 3: high


class Student:
    def __init__(self, name, engagement_level):
        self.name = name
        self.engagement_level = engagement_level
        self.current_room = None
        self.interaction_log = []
        self.interaction_probability = 0  # Probability of interacting with an object
        self.movement_frequency = 0  # Time interval between moves
        self.interaction_duration = 0  # Duration of interaction
        self.num_interactions = 0  # Number of interactions
        self.login_frequency = None
        self.login_days = set()  # Track days the student logs in
        self.timestamp = fake.date_time_between(start_date='-30d', end_date='now')

        self.user_data()

    def calculate_login_days(self, simulation_start, total_days):
        current_day = simulation_start
        while current_day <= simulation_start + datetime.timedelta(days=total_days):
            if random.randint(1, self.login_frequency) == 1:
                self.login_days.add(current_day)
            current_day += datetime.timedelta(days=1)

    def user_data(self):
        # Customize user behavior based on engagement level
        match self.engagement_level:
            case 1:
                self.num_interactions = random.randint(1, 3)
                self.interaction_probability = 0.5  # 50% chance to interact
                self.movement_frequency = datetime.timedelta(
                    seconds=random.randint(60, 300))  # Move around more
                self.interaction_duration = datetime.timedelta(
                    seconds=random.randint(30, 90))  # Short interactions
                self.login_frequency = 7  # Log in every ~7 days
            case 2:
                self.num_interactions = random.randint(2, 5)
                self.interaction_probability = 0.7  # 70% chance to interact
                self.movement_frequency = datetime.timedelta(
                    seconds=random.randint(120, 240))  # Moderate movement
                self.interaction_duration = datetime.timedelta(
                    seconds=random.randint(60, 180))  # Longer interactions
                self.login_frequency = 4  # Log in every ~4 days
            case 3:
                self.num_interactions = random.randint(3, 7)
                self.interaction_probability = 0.9  # 90% chance to interact
                self.movement_frequency = datetime.timedelta(
                    seconds=random.randint(300, 600))  # Less movement
                self.interaction_duration = datetime.timedelta(
                    seconds=random.randint(180, 300))  # Extended interactions
                self.login_frequency = 2  # Log in every ~2 days

    def move_and_interact(self, rooms, current_date):
        self.move(rooms)
        for _ in range(self.num_interactions):
            if random.random() < self.interaction_probability:  # Check if user decides to interact
                self.interact(current_date)
            else:
                self.move(rooms)

    def move(self, rooms):
        previous_room = self.current_room
        self.current_room = random.choice(
            [room for room in rooms if room != self.current_room]
        )
        self.timestamp += self.movement_frequency
        self.interaction_log.append({
            "username": self.name,
            "engagement_level": self.engagement_level,
            "timestamp": self.timestamp,
            "activity_type": "movement",
            "room": self.current_room.name,
            "object": None,
            "duration": self.movement_frequency,
            "details": f"Moved {f'from {previous_room.name} ' if previous_room else ''}to {self.current_room.name}"
        })

    def interact(self, rooms):
        if not self.current_room.objects:
            return
        obj = random.choice(self.current_room.objects)
        self.timestamp += self.interaction_duration  # Update timestamp after interacting
        self.interaction_log.append({
            "username": self.name,
            "engagement_level": self.engagement_level,
            "timestamp": self.timestamp,
            "activity_type": "interaction",
            "room": self.current_room.name,
            "object": obj.name,
            "duration": self.interaction_duration,
            "details": f"Interacted with {obj.name}"
        })


class Object:
    def __init__(self, name: str):
        self.name = name


class Room:
    def __init__(self,
                 name: str,
                 objects: list[Object],
                 size: tuple[int] = (35, 50)):
        self.name = name
        self.objects = objects
        self.size = size  # width and length in meters


class Simulation:
    def __init__(
            self,
            num_users: int,
            rooms_and_objects: dict[str, list[str]],
            duration,
            generate_csv_file: bool = False):
        self.num_users = num_users
        self.rooms_and_objects = rooms_and_objects
        self.duration = duration
        self.generate_csv_file = generate_csv_file
        self.users = []
        self.rooms = []
        self.objects = []
        self.interaction_data = []
        self.start_date = fake.date_time_between(start_date='-30d', end_date='now')

    def run_simulation(self):
        print("Starting simulation...")
        start_time = time.time()
        self.create_users()
        self.create_rooms_and_objects()
        current_date = self.start_date

        for day in range(self.duration):
            current_date = self.start_date + datetime.timedelta(days=day)
            for user in self.users:
                if current_date in user.login_days:
                    user.move_and_interact(self.rooms, current_date)

        self.collect_data()
        if self.generate_csv_file:
            self.save_to_csv()
        end_time = time.time()
        print(f"Simulation completed in {end_time - start_time} seconds.")

    def create_users(self):
        num_users_low_engagement = math.ceil(self.num_users * 0.06)
        num_users_average_engagement = math.ceil(self.num_users * 0.88)
        num_users_high_engagement = math.ceil(self.num_users * 0.06)

        for _ in range(num_users_low_engagement):
            start_date = fake.date_time_between(start_date='-100d', end_date='now')
            new_user = Student(f"{fake.first_name()} {fake.last_name()}", 1)
            # new_user.timestamp = start_date  # Assign the individual start date
            new_user.calculate_login_days(start_date, self.duration)
            self.users.append(new_user)

        for _ in range(num_users_average_engagement):
            start_date = fake.date_time_between(start_date='-100d', end_date='now')
            new_user = Student(f"{fake.first_name()} {fake.last_name()}", 2)
            # new_user.timestamp = start_date  # Assign the individual start date
            new_user.calculate_login_days(start_date, self.duration)
            self.users.append(new_user)

        for _ in range(num_users_high_engagement):
            start_date = fake.date_time_between(start_date='-100d', end_date='now')
            new_user = Student(f"{fake.first_name()} {fake.last_name()}", 3)
            # new_user.timestamp = start_date  # Assign the individual start date
            new_user.calculate_login_days(start_date, self.duration)
            self.users.append(new_user)

    def create_rooms_and_objects(self):
        for room in self.rooms_and_objects.keys():
            room_objects = [Object(name=obj_name) for obj_name in self.rooms_and_objects[room]]
            self.rooms.append(Room(name=room, objects=room_objects))
            for obj in room_objects:
                self.objects.append(obj)

    def collect_data(self):
        for user in self.users:
            self.interaction_data.extend(user.interaction_log)

    def save_to_csv(self):
        df = pd.DataFrame(self.interaction_data)
        # df['duration'] = df['duration'].astype(str).map(lambda x: x[7:])
        df.to_csv("interaction_data.csv", index=False)
        # pd.set_option('expand_frame_repr', False)
        # print(df)


if __name__ == "__main__":
    rooms_and_objects_dict = {
        "Classroom": ["Desk", "Chair", "Book", "Computer"],
        "Auditorium": ["Chair", "Screen"],
        "Library": ["Book", "Computer"],
        "Laboratory": ["Microscope", "Computer"],
        # add café
    }

    sim = Simulation(num_users=3*36,
                     rooms_and_objects=rooms_and_objects_dict,
                     duration=100,  # semestre
                     generate_csv_file=True)
    sim.run_simulation()

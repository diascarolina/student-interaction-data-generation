import pygame
import random
import math
from faker import Faker
import datetime

# Initial setup
pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Faker for names
fake = Faker(locale='pt_BR')
Faker.seed(456)


class Object:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def draw(self):
        pygame.draw.polygon(screen, YELLOW, [
            (self.position[0], self.position[1] - 10),
            (self.position[0] - 10, self.position[1] + 10),
            (self.position[0] + 10, self.position[1] + 10)
        ])


class Student:
    def __init__(self, name, color, room):
        self.name = name
        self.color = color
        self.room = room
        self.x, self.y = self.room.get_random_position()

    def move(self):
        # Move within the confines of the room
        new_x = self.x + random.randint(-5, 5)
        new_y = self.y + random.randint(-5, 5)

        # Ensure the new position is within the room boundaries
        if self.room.rect.left < new_x < self.room.rect.right and self.room.rect.top < new_y < self.room.rect.bottom:
            self.x, self.y = new_x, new_y

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)


class Room:
    def __init__(self, name, rect, objects):
        self.name = name
        self.rect = rect
        self.objects = objects

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect, 2)
        font = pygame.font.Font(None, 36)

        label = font.render(self.name, True, BLUE)
        screen.blit(label, (self.rect.x + 10, self.rect.y + 10))

        for obj in self.objects:
            obj.draw()

    def get_random_position(self):
        return (
            random.randint(self.rect.left + 10, self.rect.right - 10),
            random.randint(self.rect.top + 10, self.rect.bottom - 10)
        )


def main():
    running = True

    # Define rooms and objects within them
    rooms = [
        Room("Classroom", pygame.Rect(50, 50, 200, 150), [
            Object("Desk", (100, 100)),
            Object("Chair", (150, 120))
        ]),
        Room("Library", pygame.Rect(300, 50, 200, 150), [
            Object("Book", (350, 100)),
            Object("Computer", (400, 120))
        ]),
        Room("Laboratory", pygame.Rect(550, 50, 200, 150), [
            Object("Microscope", (600, 100)),
            Object("Computer", (650, 120))
        ]),
        Room("Auditorium", pygame.Rect(50, 250, 700, 300), [
            Object("Chair", (100, 300)),
            Object("Screen", (400, 400))
        ]),
    ]

    # Create students
    students = [Student(f"{fake.first_name()} {fake.last_name()}", RED, random.choice(rooms)) for _ in range(10)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        # Draw rooms and objects
        for room in rooms:
            room.draw()

        # Move and draw students
        for student in students:
            student.move()
            student.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


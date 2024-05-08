import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Hypothetical library import statement
# from synthetic_lib import Persona, Topic, Mood, DatasetGenerator

# Define characteristics for personas, topics, moods, etc.
class Persona:
    def __init__(self, name, age_range, profession):
        self.name = name
        self.age_range = age_range
        self.profession = profession

class Topic:
    def __init__(self, subject, complexity):
        self.subject = subject
        self.complexity = complexity

class Mood:
    def __init__(self, mood_type):
        self.mood_type = mood_type

class Location:
    def __init__(self, city, country):
        self.city = city
        self.country = country

class Time:
    def __init__(self, time_of_day):
        self.time_of_day = time_of_day

# Generate random dates within the last year
def generate_random_datetime():
    start_date = datetime.now() - timedelta(days=365)
    random_date = start_date + timedelta(days=random.randint(0, 365))
    return random_date.strftime("%Y-%m-%d %H:%M:%S")

# Instantiate personas
personas = [
    Persona("Alice", (25, 35), "Engineer"),
    Persona("Bob", (40, 50), "Doctor"),
    Persona("Cindy", (30, 40), "Artist")
]

# Instantiate topics
topics = [
    Topic("Technology", "High"),
    Topic("Medicine", "Medium"),
    Topic("Art", "Low")
]

# Instantiate moods
moods = [
    Mood("Happy"),
    Mood("Sad"),
    Mood("Excited")
]

# Instantiate locations
locations = [
    Location("New York", "USA"),
    Location("London", "UK"),
    Location("Tokyo", "Japan")
]

# Instantiate times of day
times_of_day = [
    Time("Morning"),
    Time("Afternoon"),
    Time("Evening")
]

# Generate synthetic dataset
def generate_dataset(num_entries):
    dataset = []
    for _ in range(num_entries):
        persona = random.choice(personas)
        topic = random.choice(topics)
        mood = random.choice(moods)
        location = random.choice(locations)
        time_of_day = random.choice(times_of_day)
        date_time = generate_random_datetime()

        dataset.append({
            "Name": persona.name,
            "Age Range": f"{persona.age_range[0]}-{persona.age_range[1]}",
            "Profession": persona.profession,
            "Topic": topic.subject,
            "Complexity": topic.complexity,
            "Mood": mood.mood_type,
            "City": location.city,
            "Country": location.country,
            "Time of Day": time_of_day.time_of_day,
            "Date Time": date_time
        })
    return dataset

# Number of entries to generate
num_entries = 100

# Generate the dataset
synthetic_data = generate_dataset(num_entries)

# Convert list to DataFrame
df = pd.DataFrame(synthetic_data)

# Display the DataFrame
print(df.head())

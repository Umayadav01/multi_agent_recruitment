import json
from faker import Faker
import random

fake = Faker()

skills_pool = ["Python", "Java", "C++", "TensorFlow", "PyTorch", "React", "SQL", "Docker", "Kubernetes"]
roles_pool = ["AI Engineer", "Data Scientist", "Backend Developer", "Full Stack Developer"]

def generate_candidate():
    return {
        "name": fake.name(),
        "linkedin_summary": fake.text(max_nb_chars=200),
        "github_projects": [fake.word() for _ in range(random.randint(2, 5))],
        "skills": random.sample(skills_pool, k=random.randint(3, 6)),
        "experience_years": random.randint(1, 10),
        "role": random.choice(roles_pool)
    }

def generate_market_data():
    return {
        "role": random.choice(roles_pool),
        "avg_salary": random.randint(50000, 150000),
        "demand_index": random.randint(1, 10),
        "top_sources": ["LinkedIn", "GitHub", "Kaggle", "StackOverflow"]
    }

def generate_conversation():
    return {
        "candidate": fake.name(),
        "conversation": [
            "I love collaborating with teams on AI projects.",
            "I prefer solving complex problems step by step.",
            "I believe communication is key to successful projects."
        ]
    }

if __name__ == "__main__":
    candidates = [generate_candidate() for _ in range(10)]
    market_data = [generate_market_data() for _ in range(5)]
    conversations = [generate_conversation() for _ in range(10)]

    with open("data/candidates.json", "w") as f:
        json.dump(candidates, f, indent=2)

    with open("data/market_data.json", "w") as f:
        json.dump(market_data, f, indent=2)

    with open("data/conversations.json", "w") as f:
        json.dump(conversations, f, indent=2)

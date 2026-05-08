from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

# Load dataset
with open("data/tests.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

# Request models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# Keywords
KEYWORDS = {
    "java": ["java"],
    "python": ["python"],
    "sql": ["sql", "database"],
    "javascript": ["javascript", "js"],
    "react": ["react"],
    "node": ["node", "nodejs"],
    "cloud": ["cloud", "aws", "azure"],
    "security": ["security", "cybersecurity"],
    "ai": ["ai", "machine learning"],
    "personality": ["personality", "behavior", "opq"],
    "leadership": ["leadership", "manager"],
    "communication": ["communication", "stakeholder"],
    "reasoning": ["reasoning", "cognitive"],
}

BANNED = [
    "legal",
    "salary",
    "politics",
    "religion",
    "medical",
    "ignore previous"
]

VAGUE = [
    "assessment",
    "need assessment",
    "need test",
    "hiring"
]

@app.get("/health")
def health():
    return {"status": "ok"}

# Detect assessment type
def detect_test_type(text):

    text = text.lower()

    if any(x in text for x in ["personality", "behavior", "opq"]):
        return "Personality"

    if any(x in text for x in ["reasoning", "cognitive", "aptitude"]):
        return "Cognitive"

    if any(x in text for x in ["leadership", "communication", "teamwork"]):
        return "Behavioral"

    return "Technical"

# Recommendation engine
def get_recommendations(user_message):

    results = []

    for test in assessments:

        searchable = " ".join([
            test.get("name", ""),
            test.get("description", ""),
            " ".join(test.get("keys", []))
        ]).lower()

        score = sum(
            any(w in user_message for w in words) and
            any(w in searchable for w in words)
            for words in KEYWORDS.values()
        )

        if score > 0:

            results.append((
                score,
                {
                    "name": test.get("name"),
                    "url": test.get("link"),
                    "test_type": detect_test_type(searchable),
                    "remote_support": test.get("remote", "no"),
                    "adaptive_support": test.get("adaptive", "no")
                }
            ))

    results.sort(reverse=True, key=lambda x: x[0])

    unique = []
    seen = set()

    for _, item in results:
        if item["name"] not in seen:
            unique.append(item)
            seen.add(item["name"])

    return unique[:10]

@app.post("/chat")
def chat(req: ChatRequest):

    user_message = " ".join(
        msg.content.lower() for msg in req.messages
    )

    # Refusal
    if any(word in user_message for word in BANNED):
        return {
            "reply": "I can only help with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Clarification
    if user_message.strip() in VAGUE:
        return {
            "reply": "What role or skills are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Comparison
    if "difference" in user_message or "compare" in user_message:

        if "opq" in user_message and "gsa" in user_message:
            return {
                "reply": "OPQ evaluates personality and workplace behavior, while GSA focuses on cognitive and reasoning abilities.",
                "recommendations": [],
                "end_of_conversation": True
            }

        return {
            "reply": "Please mention the two assessments you want to compare.",
            "recommendations": [],
            "end_of_conversation": False
        }

    recommendations = get_recommendations(user_message)

    if not recommendations:
        return {
            "reply": "No matching SHL assessments were found.",
            "recommendations": [],
            "end_of_conversation": True
        }

    return {
        "reply": f"Found {len(recommendations)} matching SHL assessments.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }
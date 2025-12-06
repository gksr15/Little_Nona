"""
Little Nona - Configuration Settings
Warm bedtime stories told by Grandma Nona
"""

import os
from pathlib import Path

# Project Info
PROJECT_NAME = "Little Nona"
VERSION = "1.0.0"
DESCRIPTION = "Warm bedtime stories told by Grandma Nona 👵✨"

# API Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-3.5-turbo"

# Story Settings
STORY_CATEGORIES = [
    "adventure",
    "friendship", 
    "animals",
    "fantasy",
    "learning",
    "bedtime",
    "family",
    "nature"
]

AGE_RANGE = {
    "min": 3,
    "max": 12,
    "default": 7
}

STORY_LENGTHS = {
    "short": {
        "label": "Short (3-4 minutes)",
        "words": "250-350",
        "emoji": "🚀"
    },
    "medium": {
        "label": "Medium (5-6 minutes)", 
        "words": "400-500",
        "emoji": "📖"
    },
    "long": {
        "label": "Longer (7-8 minutes)",
        "words": "550-650", 
        "emoji": "📚"
    }
}

# Agent Settings (Little Nona's 3-agent architecture)
AGENT_CONFIG = {
    "storyteller": {
        "temperature": 0.8,
        "max_tokens": 1800,
        "role": "Creative storyteller with grandmother warmth"
    },
    "judge": {
        "temperature": 0.2,
        "max_tokens": 1000,
        "role": "Quality evaluator"
    },
    "reviser": {
        "temperature": 0.7,
        "max_tokens": 1800,
        "role": "Story improver"
    }
}

# Quality Thresholds
QUALITY_THRESHOLDS = {
    "excellent": 9.0,
    "very_good": 8.5,
    "good": 7.0,
    "needs_revision": 5.0
}

# Safety Settings
SAFETY_ENABLED = True
MAX_REVISION_ATTEMPTS = 3

# Grandma Nona's Personality
NONA_PERSONALITY = {
    "warmth": "Like a loving grandmother",
    "voice": "Gentle, soothing, caring",
    "tone": "Warm but never condescending",
    "signature": "Sweet dreams, little one! 🌙💖"
}

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
GIFS_DIR = ASSETS_DIR / "gifs"

# Gradio Settings
GRADIO_CONFIG = {
    "theme": "soft",  # Warm, cozy theme
    "title": "Little Nona - Your Bedtime Story Friend",
    "description": "Let Grandma Nona tell you a magical bedtime story 👵✨",
    "examples": [
        ["Emma", "7", "adventure", "A brave explorer finds a hidden treasure"],
        ["Lucas", "5", "animals", "A puppy makes new friends"],
        ["Sophia", "9", "fantasy", "A young wizard learns magic"]
    ]
}

"""
Little Nona - Utility Functions
Helper functions for story generation
"""

import re
import json
from typing import Dict, Optional


def create_character_name(child_name: str, category: str) -> str:
    """
    Create a SIMILAR but DIFFERENT character name.
    This makes the child feel connected but maintains story magic.
    
    Strategies:
    1. Diminutives (Elizabeth → Ellie, Benjamin → Benji)
    2. Add 'y'/'ie' ending (Jack → Jackie, Sam → Sammy)
    3. Rhyming pairs (Anna → Hannah, Jason → Mason)
    4. Letter swaps (Emma → Emmy, Mia → Mimi)
    5. First syllable variations (Alexander → Alex, Isabella → Bella)
    """
    name = child_name.strip().title()
    
    # Common diminutives and variations
    transformations = {
        # -a to -y endings
        "Emma": "Emmy",
        "Mia": "Mimi", 
        "Sophia": "Sophie",
        "Olivia": "Liv",
        "Isabella": "Bella",
        "Amelia": "Milly",
        "Ella": "Ellie",
        "Anna": "Annie",
        "Luna": "Lulu",
        
        # -er/-ar to -y
        "Alexander": "Alex",
        "Christopher": "Chris",
        "Oliver": "Ollie",
        
        # Add -ie/-y
        "Jack": "Jackie",
        "Sam": "Sammy",
        "Tom": "Tommy",
        "Ben": "Benny",
        "Max": "Maxie",
        "Luke": "Lukey",
        
        # Rhyming pairs
        "Jason": "Mason",
        "Hannah": "Anna",
        "Ethan": "Nathan",
        
        # Common boys names
        "Michael": "Mikey",
        "William": "Will",
        "James": "Jamie",
        "Daniel": "Danny",
        "Matthew": "Matty",
        "Lucas": "Luke",
        "Henry": "Hank",
        "Benjamin": "Benji",
        "Samuel": "Sammy",
        "David": "Davey",
        "Joseph": "Joey",
        "Jacob": "Jake",
        "Ryan": "Ry",
        "Andrew": "Andy",
        "Joshua": "Josh",
        
        # Common girls names
        "Elizabeth": "Ellie",
        "Victoria": "Vicky",
        "Katherine": "Katie",
        "Margaret": "Maggie",
        "Jennifer": "Jenny",
        "Jessica": "Jessie",
        "Sarah": "Sadie",
        "Emily": "Emma",
        "Grace": "Gracie",
        "Lily": "Lilly",
        "Chloe": "Coco",
        "Zoe": "Zoey",
    }
    
    # Check direct mapping
    if name in transformations:
        return transformations[name]
    
    # Try generic transformations
    # Strategy 1: If ends in 'a', change to 'y'
    if name.endswith('a') and len(name) > 3:
        return name[:-1] + 'y'
    
    # Strategy 2: If short name (3-5 letters), add 'ie' or 'y'
    if 3 <= len(name) <= 5:
        if name[-1] in 'aeiou':
            return name + 'y'
        else:
            return name + 'ie'
    
    # Strategy 3: Use first syllable + 'y'
    if len(name) > 5:
        # Try to find first syllable
        for i in [3, 4, 5]:
            if i < len(name):
                return name[:i] + 'y'
    
    # Strategy 4: Just add 'y' as fallback
    return name + 'y'


def validate_age(age_input: str) -> Optional[int]:
    """
    Validate and parse age input.
    Accepts numbers (7) or text (seven).
    Returns None if invalid.
    """
    text_to_num = {
        "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
        "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12
    }
    
    # Try text
    if age_input.lower().strip() in text_to_num:
        return text_to_num[age_input.lower().strip()]
    
    # Try number
    try:
        age = int(age_input)
        if 3 <= age <= 12:
            return age
    except ValueError:
        pass
    
    return None


def validate_name(name: str) -> bool:
    """
    Validate child's name.
    Must be letters, spaces, or hyphens only.
    """
    if not name or len(name) > 50:
        return False
    return bool(re.match(r'^[a-zA-Z\s\-]+$', name))


def extract_json_from_response(response: str) -> Optional[Dict]:
    """
    Extract JSON from AI response, handling markdown code blocks.
    """
    try:
        # Remove markdown code blocks
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        
        return json.loads(response.strip())
    except json.JSONDecodeError:
        return None


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def format_quality_score(score: float) -> str:
    """Format quality score with emoji."""
    if score >= 9.0:
        return f"⭐ {score:.1f}/10 - Excellent!"
    elif score >= 8.5:
        return f"✨ {score:.1f}/10 - Very Good!"
    elif score >= 7.0:
        return f"👍 {score:.1f}/10 - Good!"
    elif score >= 5.0:
        return f"⚠️ {score:.1f}/10 - Needs Work"
    else:
        return f"❌ {score:.1f}/10 - Poor"


def get_age_vocabulary(age: int) -> Dict[str, str]:
    """
    Get age-appropriate vocabulary guidelines.
    Returns vocab, sentences, complexity, details.
    """
    if age <= 5:
        return {
            "vocab": "very simple words (3-5 letters mostly)",
            "sentences": "very short sentences (5-8 words)",
            "complexity": "single simple ideas per sentence",
            "details": "basic, concrete details"
        }
    elif age <= 7:
        return {
            "vocab": "simple, everyday words",
            "sentences": "short sentences (6-10 words)",
            "complexity": "clear, straightforward ideas",
            "details": "vivid, concrete descriptions"
        }
    elif age <= 10:
        return {
            "vocab": "easy to medium words",
            "sentences": "medium sentences (8-12 words)",
            "complexity": "simple but interesting ideas",
            "details": "rich, colorful descriptions"
        }
    else:  # 11-12
        return {
            "vocab": "varied vocabulary with some challenging words",
            "sentences": "varied sentence length",
            "complexity": "more nuanced ideas",
            "details": "detailed, imaginative descriptions"
        }


def get_category_details(category: str) -> Dict[str, str]:
    """Get category-specific prompting strategy."""
    category_map = {
        "adventure": {
            "focus": "exciting journey with clear goal",
            "question": "What goal should {name} try to achieve?",
            "examples": "find treasure, explore new land, rescue friend"
        },
        "friendship": {
            "focus": "relationships and connection",
            "question": "What kind of friend should {name} meet?",
            "examples": "lonely animal, shy kid, magical creature"
        },
        "animals": {
            "focus": "cute animals and nature",
            "question": "What animal should {name} be or meet?",
            "examples": "puppy, kitten, bunny, baby dragon"
        },
        "fantasy": {
            "focus": "magical world with wonder",
            "question": "What magical thing should happen?",
            "examples": "learn a spell, find magic object, visit fairy land"
        },
        "learning": {
            "focus": "discovering something new",
            "question": "What should {name} learn or discover?",
            "examples": "how to share, be brave, solve puzzles"
        },
        "bedtime": {
            "focus": "calming evening routine",
            "question": "What peaceful evening should {name} have?",
            "examples": "cozy night, stargazing, gentle dreams"
        },
        "family": {
            "focus": "love and family bonds",
            "question": "What family moment should {name} experience?",
            "examples": "help parent, play with sibling, visit grandparent"
        },
        "nature": {
            "focus": "natural world and beauty",
            "question": "What part of nature should {name} explore?",
            "examples": "forest, garden, beach, mountain"
        }
    }
    
    return category_map.get(category, category_map["adventure"])


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def add_nona_warmth(message: str) -> str:
    """Add Grandma Nona's warm touch to messages."""
    warmth_phrases = [
        "my dear",
        "little one", 
        "sweetie",
        "my love"
    ]
    
    # Add random warmth (but keep it simple for now)
    return message


def sanitize_story_input(text: str) -> str:
    """Clean and sanitize user story input."""
    # Remove excessive whitespace
    text = " ".join(text.split())
    # Limit length
    return text[:500] if text else ""

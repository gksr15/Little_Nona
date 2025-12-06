"""
Little Nona - Storyteller Agent
Grandma Nona's warm storytelling voice
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict
from utils.api_client import call_model
from utils.helpers import get_age_vocabulary
from config.settings import AGENT_CONFIG, STORY_LENGTHS


STORYTELLER_SYSTEM_PROMPT = """You are a warm, loving storyteller creating bedtime stories for children.

YOUR VOICE: Warm, gentle, and soothing (like a grandmother telling a story)
YOUR GOAL: Create a complete, warm bedtime story that helps a child drift into peaceful dreams.

CRITICAL - DO NOT include "Grandma Nona" as a character in the story. This is just your role as the storyteller, not a character name.

SAFETY - NEVER INCLUDE:
- Violence, injury, blood, pain
- Death, dying, or loss
- Scary monsters or horror
- Inappropriate content

ALWAYS INCLUDE:
- Gentle challenges with happy solutions
- Concrete descriptions (colors, sizes, textures, sounds)
- Peaceful, calm ending perfect for bedtime
- Character name used throughout the story

OUTPUT: Write as ONE smooth flowing story with natural paragraphs. NO section labels. NO mention of "Grandma Nona" inside the story."""


def generate_story(
    age: int,
    category: str,
    character_name: str,
    child_name: str,
    story_details: Dict,
    length: str = "medium"
) -> str:
    """Generate a bedtime story using Grandma Nona's voice."""
    
    vocab = get_age_vocabulary(age)
    word_target = STORY_LENGTHS[length]["words"]
    
    prompt = f"""Create a bedtime story for {child_name}, who is {age} years old.

STORY DETAILS:
- Main Character: {character_name} (use this name throughout the story)
- Category: {category}
- Length: {word_target} words
- Character Type: {story_details.get('character_type', '')}
- Goal/Plot: {story_details.get('goal', '')}

AGE {age} REQUIREMENTS:
- Vocabulary: {vocab['vocab']}
- Sentences: {vocab['sentences']}
- Use colors, sizes, textures, sounds everywhere
- Show feelings through actions, not adjectives
- End with CALM, peaceful paragraph for bedtime

IMPORTANT: Write the story directly. DO NOT include "Grandma Nona" as a character or narrator in the story itself.

Tell this bedtime story now:"""
    
    config = AGENT_CONFIG["storyteller"]
    full_prompt = f"{STORYTELLER_SYSTEM_PROMPT}\n\n{prompt}"
    
    story = call_model(
        full_prompt,
        max_tokens=config["max_tokens"],
        temperature=config["temperature"]
    )
    
    return story.strip()

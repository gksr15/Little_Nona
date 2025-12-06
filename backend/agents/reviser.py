"""
Little Nona - Reviser Agent
Improves stories based on feedback
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.api_client import call_model
from config.settings import AGENT_CONFIG


def revise_story(original_story: str, feedback: str, age: int, character_name: str) -> str:
    """Revise story based on user feedback."""
    
    prompt = f"""A child or parent has requested changes to this bedtime story.

ORIGINAL STORY:
{original_story}

REQUESTED CHANGES:
{feedback}

REQUIREMENTS:
- Child's Age: {age}
- Main Character: {character_name}
- Make the requested changes thoughtfully
- Keep what's working well
- Maintain warm, gentle, soothing storytelling voice
- Ensure safe and age-appropriate
- DO NOT include "Grandma Nona" as a character or narrator in the story

Return the complete REVISED story (no notes, just the story):"""
    
    config = AGENT_CONFIG["reviser"]
    
    revised_story = call_model(
        prompt,
        max_tokens=config["max_tokens"],
        temperature=config["temperature"]
    )
    
    return revised_story.strip()

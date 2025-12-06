"""
Little Nona - Story Service
Orchestrates the 3-agent system
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from typing import Dict, Optional
from agents.storyteller import generate_story
from agents.judge import evaluate_story, format_evaluation_report
from agents.reviser import revise_story
from utils.helpers import create_character_name, count_words


class StorySession:
    """Manages a complete story generation session."""
    
    def __init__(self, child_name: str, age: int, category: str, 
                 story_details: Optional[Dict] = None, length: str = "medium"):
        self.child_name = child_name
        self.age = age
        self.category = category
        self.story_details = story_details or {}
        self.length = length
        
        # Create similar character name
        self.character_name = create_character_name(child_name, category)
        self.story_details["character_name"] = self.character_name
        
        # Story state
        self.current_story = None
        self.revision_count = 0
    
    def generate_initial_story(self):
        """Generate the initial story."""
        self.current_story = generate_story(
            age=self.age,
            category=self.category,
            character_name=self.character_name,
            child_name=self.child_name,
            story_details=self.story_details,
            length=self.length
        )
        return self.current_story
    
    def evaluate_current_story(self):
        """Evaluate current story with judge agent."""
        if not self.current_story:
            return None
        
        return evaluate_story(
            story=self.current_story,
            age=self.age,
            category=self.category,
            character_name=self.character_name
        )
    
    def revise_from_user_feedback(self, user_feedback: str):
        """Revise story based on user's feedback."""
        if not self.current_story or self.revision_count >= 3:
            return self.current_story
        
        self.current_story = revise_story(
            original_story=self.current_story,
            feedback=user_feedback,
            age=self.age,
            character_name=self.character_name
        )
        
        self.revision_count += 1
        return self.current_story


def create_story_simple(child_name: str, age: int, category: str,
                       story_details: Optional[Dict] = None, length: str = "medium") -> Dict:
    """Simple interface for creating a story."""
    session = StorySession(child_name, age, category, story_details, length)
    story = session.generate_initial_story()
    
    return {
        "story": story,
        "character_name": session.character_name,
        "word_count": count_words(story),
        "child_name": child_name,
        "age": age,
        "category": category
    }

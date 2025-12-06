"""
Little Nona - Judge Agent
Evaluates story quality with child safety as priority
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, Optional
from utils.api_client import call_model
from utils.helpers import extract_json_from_response
from config.settings import AGENT_CONFIG


def evaluate_story(story: str, age: int, category: str, character_name: str) -> Optional[Dict]:
    """Evaluate story quality using judge agent."""
    
    prompt = f"""Evaluate this bedtime story and return ONLY valid JSON:

STORY:
{story}

CONTEXT: Age {age}, Category {category}, Character {character_name}

Evaluate on these dimensions (0-10 each):
1. safety (MOST IMPORTANT - no violence, death, scary content)
2. age_appropriateness
3. concrete_descriptions
4. show_dont_tell
5. character_development
6. story_flow
7. engagement
8. bedtime_suitability
9. warmth

Return JSON:
{{
  "overall_score": 8.5,
  "needs_revision": false,
  "dimension_scores": {{"safety": 10.0, ...}},
  "strengths": ["Point 1", "Point 2"],
  "improvements": ["Point 1"]
}}"""
    
    config = AGENT_CONFIG["judge"]
    
    try:
        response = call_model(prompt, max_tokens=config["max_tokens"], temperature=config["temperature"])
        evaluation = extract_json_from_response(response)
        return evaluation
    except Exception as e:
        print(f"Judge evaluation failed: {e}")
        return None


def format_evaluation_report(evaluation: Dict) -> str:
    """Format evaluation results into human-readable report."""
    if not evaluation:
        return "❌ Evaluation failed"
    
    score = evaluation["overall_score"]
    
    if score >= 9.0:
        emoji = "⭐"
        rating = "Excellent!"
    elif score >= 8.5:
        emoji = "✨"
        rating = "Very Good!"
    else:
        emoji = "👍"
        rating = "Good!"
    
    report = f"\n📊 Story Quality Score: {emoji} {score:.1f}/10 - {rating}\n\n"
    
    if evaluation.get("strengths"):
        report += "🌟 Strengths:\n"
        for strength in evaluation["strengths"]:
            report += f"  ✓ {strength}\n"
        report += "\n"
    
    if evaluation.get("improvements"):
        report += "🔧 Suggested Improvements:\n"
        for improvement in evaluation["improvements"]:
            report += f"  • {improvement}\n"
    
    return report

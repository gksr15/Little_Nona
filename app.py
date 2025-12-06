"""
Little Nona - Gradio Frontend
Simple, warm interface for bedtime stories
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

import gradio as gr
from story_service import StorySession
from agents.judge import format_evaluation_report
from utils.helpers import validate_age, validate_name
from config.settings import STORY_CATEGORIES, STORY_LENGTHS
from utils.api_client import get_client

# Global session and API key
current_session = None
current_api_key = None


def set_api_key(api_key):
    """Set the OpenAI API key."""
    global current_api_key
    
    if not api_key or not api_key.strip():
        return "❌ Please enter your OpenAI API key"
    
    if not api_key.startswith("sk-"):
        return "❌ Invalid API key format. Should start with 'sk-'"
    
    try:
        # Set the API key
        current_api_key = api_key.strip()
        os.environ["OPENAI_API_KEY"] = current_api_key
        
        # Test the connection
        client = get_client(current_api_key)
        if client.test_connection():
            return "✅ API key verified! You can now create stories. 🌟"
        else:
            return "❌ API key test failed. Please check your key."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def generate_story_handler(child_name, age_input, category, custom_story, character_type, goal, length):
    """Generate initial story."""
    global current_session, current_api_key
    
    # Check API key is set
    if not current_api_key:
        return "", "", "❌ Please enter your OpenAI API key in the Setup tab first!"
    
    if not validate_name(child_name):
        return "", "", "❌ Please enter a valid name (letters only)."
    
    age = validate_age(age_input)
    if age is None:
        return "", "", "❌ Please enter age between 3 and 12."
    
    try:
        story_details = {}
        
        # If custom story is provided, use it as the main goal
        if custom_story and custom_story.strip():
            story_details["goal"] = custom_story.strip()
        else:
            # Otherwise use character type and goal
            if character_type:
                story_details["character_type"] = character_type
            if goal:
                story_details["goal"] = goal
        
        current_session = StorySession(child_name, age, category, story_details, length)
        story = current_session.generate_initial_story()
        character_name = current_session.character_name
        word_count = len(story.split())
        
        status = f"""✨ Story created by Grandma Nona!

👶 For: {child_name} (Age {age})
🎭 Character: {character_name}
📚 Category: {category.title()}
📏 Length: {word_count} words

Sweet dreams, little one! 🌙💖"""
        
        return story, character_name, status
    
    except Exception as e:
        return "", "", f"❌ Error: {str(e)}\n\nPlease check your API key is valid."


def evaluate_story_handler():
    """Evaluate current story."""
    global current_session, current_api_key
    
    if not current_api_key:
        return "❌ Please enter your OpenAI API key in the Setup tab first!"
    
    if not current_session or not current_session.current_story:
        return "❌ Please generate a story first!"
    
    try:
        evaluation = current_session.evaluate_current_story()
        if evaluation:
            return format_evaluation_report(evaluation)
        else:
            return "❌ Evaluation failed."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def revise_story_handler(feedback):
    """Revise story based on feedback."""
    global current_session, current_api_key
    
    if not current_api_key:
        return "", "❌ Please enter your OpenAI API key in the Setup tab first!"
    
    if not current_session or not current_session.current_story:
        return "", "❌ Please generate a story first!"
    
    if not feedback.strip():
        return current_session.current_story, "❌ Please tell me what to change!"
    
    try:
        revised_story = current_session.revise_from_user_feedback(feedback)
        word_count = len(revised_story.split())
        
        status = f"""✨ Story revised!

📝 Changes made
📏 Length: {word_count} words
🔄 Revision #{current_session.revision_count}

Sweet dreams! 🌙💖"""
        
        return revised_story, status
    except Exception as e:
        return current_session.current_story, f"❌ Error: {str(e)}"


# Build interface
with gr.Blocks(title="Little Nona") as app:
    
    gr.HTML("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); border-radius: 15px; margin-bottom: 20px;">
        <h1>👵 Little Nona - Your Bedtime Story Friend ✨</h1>
        <p style="font-size: 18px;">Let Grandma Nona tell you a warm, magical bedtime story 🌙💖</p>
    </div>
    """)
    
    with gr.Tabs():
        
        # Tab 0: Setup (API Key)
        with gr.Tab("🔑 Setup"):
            gr.Markdown("""
            ## Welcome to Little Nona! 👵✨
            
            ### Step 1: Enter Your OpenAI API Key
            
            To use Little Nona, you'll need an OpenAI API key:
            
            1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
            2. Create a new API key (or use existing one)
            3. Paste it below
            4. Click "Save API Key"
            
            **Note:** Your API key is only used during this session and is never stored.
            """)
            
            with gr.Row():
                api_key_input = gr.Textbox(
                    label="OpenAI API Key",
                    placeholder="sk-...",
                    type="password",
                    scale=3
                )
                save_key_btn = gr.Button("💾 Save API Key", variant="primary", scale=1)
            
            api_key_status = gr.Textbox(
                label="Status",
                interactive=False,
                lines=2
            )
            
            gr.Markdown("""
            ---
            
            ### Privacy & Security
            
            - 🔒 Your API key is **never stored** on disk
            - 🔒 Used only for the **current session**
            - 🔒 When you close the browser, it's **gone**
            - 🔒 Stories are **not saved** anywhere
            
            ### Need an API Key?
            
            1. Visit [OpenAI Platform](https://platform.openai.com)
            2. Sign up or log in
            3. Go to API Keys section
            4. Create a new key
            5. Paste it here!
            
            **Cost:** ~$0.003 per story (very cheap!)
            """)
        
        # Tab 1: Create Story
        with gr.Tab("📖 Create Story"):
            gr.Markdown("### Tell Grandma Nona about the child")
            
            with gr.Row():
                child_name_input = gr.Textbox(label="Child's Name", placeholder="Emma")
                age_input = gr.Textbox(label="Age", placeholder="7")
            
            category_input = gr.Dropdown(
                choices=STORY_CATEGORIES,
                value="adventure",
                label="Story Category"
            )
            
            custom_story_input = gr.Textbox(
                label="Custom Story Idea (Optional)",
                placeholder="Tell me any story you want! E.g., 'A story about a puppy who learns to swim' or 'An adventure in a magical library'",
                lines=2
            )
            
            with gr.Row():
                character_type_input = gr.Textbox(
                    label="Character Type (Optional)",
                    placeholder="a brave explorer"
                )
                goal_input = gr.Textbox(
                    label="Goal (Optional)",
                    placeholder="find a treasure"
                )
            
            length_input = gr.Radio(
                choices=list(STORY_LENGTHS.keys()),
                value="medium",
                label="Story Length"
            )
            
            generate_btn = gr.Button("✨ Create My Bedtime Story", variant="primary", size="lg")
            
            with gr.Row():
                with gr.Column(scale=3):
                    story_output = gr.Textbox(label="Your Story", lines=20, interactive=False)
                with gr.Column(scale=1):
                    character_name_output = gr.Textbox(label="Character Name", interactive=False)
                    status_output = gr.Textbox(label="Status", lines=8, interactive=False)
        
        # Tab 2: Improve Story
        with gr.Tab("🔄 Improve Story"):
            gr.Markdown("### Ask Grandma Nona to make changes")
            
            feedback_input = gr.Textbox(
                label="What would you like to change?",
                placeholder="Add more flowers, make it longer...",
                lines=3
            )
            
            revise_btn = gr.Button("🔄 Revise Story", variant="primary")
            
            revised_story_output = gr.Textbox(label="Revised Story", lines=20, interactive=False)
            revision_status_output = gr.Textbox(label="Status", lines=5, interactive=False)
        
        # Tab 3: Quality Check
        with gr.Tab("⭐ Quality Check"):
            gr.Markdown("### See how good the story is")
            
            evaluate_btn = gr.Button("⭐ Evaluate Story Quality", variant="secondary")
            evaluation_output = gr.Textbox(label="Quality Report", lines=15, interactive=False)
        
        # Tab 4: About
        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
            # 👵 About Little Nona
            
            **Little Nona** is your warm, loving bedtime story companion!
            
            ### Features:
            - 🎭 Similar character names (Emma → Emmy)
            - 👵 Grandmother warmth in every story
            - 🎯 Age-perfect stories (3-12 years)
            - 🛡️ Safe, gentle content always
            - 🔄 Request changes until perfect
            
            ### How It Works:
            1. Enter your OpenAI API key (Setup tab)
            2. Enter child's name and age
            3. Choose story category
            4. Click "Create Story"
            5. Request changes if needed
            6. Check quality (optional)
            
            ### Privacy:
            - Your API key is used only during this session
            - No data is stored anywhere
            - Stories are generated fresh each time
            
            *Sweet dreams, little one! 🌙💖*
            
            **Version 1.0** • Made with 💖 for bedtime
            """)
    
    # Wire up handlers
    save_key_btn.click(
        fn=set_api_key,
        inputs=[api_key_input],
        outputs=[api_key_status]
    )
    
    generate_btn.click(
        fn=generate_story_handler,
        inputs=[child_name_input, age_input, category_input, custom_story_input, character_type_input, goal_input, length_input],
        outputs=[story_output, character_name_output, status_output]
    )
    
    revise_btn.click(
        fn=revise_story_handler,
        inputs=[feedback_input],
        outputs=[revised_story_output, revision_status_output]
    )
    
    evaluate_btn.click(
        fn=evaluate_story_handler,
        outputs=[evaluation_output]
    )


if __name__ == "__main__":
    print("🌟 Little Nona - Starting up...")
    print("📍 Open your browser to: http://localhost:7860")
    print("🔑 You'll need to enter your OpenAI API key in the Setup tab")
    print()
    
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)

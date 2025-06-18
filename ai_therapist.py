import openai
import os
from datetime import datetime
import json
import random
from config import Config

class AITherapist:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
        self.model = Config.AI_MODEL

    def get_response(self, user_input, therapy_style="Cognitive Behavioral Therapy (CBT)", language="English"):
        try:
            if "OPENAI_API_KEY" in os.environ:
                system_prompt = Config.DEFAULT_THERAPY_PROMPT.format(
                    therapy_style=therapy_style,
                    language=language,
                    user_input=user_input
                )
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=Config.MAX_TOKENS,
                    temperature=Config.AI_TEMPERATURE
                )
                return response.choices[0].message["content"]
            else:
                return self._generate_demo_response(user_input)
        except Exception as e:
            return f"I'm sorry, I'm having trouble processing your message right now. Error: {str(e)}"

    def _generate_demo_response(self, user_input):
        input_lower = user_input.lower()

        if any(word in input_lower for word in ['anxious', 'anxiety', 'worried', 'nervous']):
            return ("I understand you're feeling anxious. That's a very common experience. Let's try a grounding technique: "
                    "Can you name 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, "
                    "and 1 thing you can taste? This can help bring you back to the present moment.")

        elif any(word in input_lower for word in ['sad', 'depressed', 'down', 'low']):
            return ("I hear that you're feeling down right now. It's important to acknowledge these feelings. Sometimes when "
                    "we're feeling low, small activities can help - like taking a short walk, listening to music, or reaching out "
                    "to someone you trust. What's one small thing you could do for yourself today?")

        elif any(word in input_lower for word in ['stress', 'stressed', 'overwhelmed']):
            return ("Feeling stressed and overwhelmed is challenging. Let's break this down - what's the most pressing thing on "
                    "your mind right now? Sometimes it helps to write down what's causing stress and then prioritize what you can "
                    "actually control versus what you can't.")

        elif any(word in input_lower for word in ['sleep', 'insomnia', 'tired']):
            return ("Sleep issues can really affect our mental health. Good sleep hygiene includes: keeping a regular sleep schedule, "
                    "avoiding screens before bed, and creating a calming bedtime routine. What's your current sleep routine like?")

        else:
            return ("Thank you for sharing with me. I'm here to listen and support you. Can you tell me more about what's been on your "
                    "mind lately? Sometimes talking through our thoughts and feelings can help us process them better.")

    def analyze_mood_patterns(self, mood_history):
        if not mood_history:
            return "Not enough data to analyze patterns yet. Keep logging your mood!"

        recent_moods = mood_history[-7:]
        avg_energy = sum(entry['energy'] for entry in recent_moods) / len(recent_moods)
        avg_anxiety = sum(entry['anxiety'] for entry in recent_moods) / len(recent_moods)

        insights = f"""
        Based on your recent mood data:
        - Average energy level: {avg_energy:.1f}/10
        - Average anxiety level: {avg_anxiety:.1f}/10
        """

        if avg_energy < 4:
            insights += "Your energy levels seem low. Consider gentle activities like short walks or listening to uplifting music."
        elif avg_energy > 7:
            insights += "Your energy levels look good! This is a great time to tackle challenging tasks."

        if avg_anxiety > 6:
            insights += " Your anxiety levels are elevated. Practice relaxation techniques like deep breathing or meditation."

        return insights

    def get_journal_prompt(self, language="English"):
        prompt_base = f"Give me a reflective journaling question in {language}."
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt_base}],
                temperature=0.7,
                max_tokens=100
            )
            return response.choices[0].message["content"]
        except Exception:
            prompts = [
                "What are three things you're grateful for today, and why?",
                "Describe a challenge you're facing and how you might approach it.",
                "What emotions have you experienced today? What triggered them?",
                "Write about a time when you overcame a difficult situation.",
                "What are your hopes and goals for the next week?",
                "How do you typically handle stress, and what works best for you?",
                "Describe someone who has had a positive impact on your life.",
                "What activities or hobbies bring you the most joy?",
                "Write about a moment today when you felt proud of yourself.",
                "What would you tell a friend who was going through what you're experiencing?"
            ]
            return random.choice(prompts)

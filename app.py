import streamlit as st
import pandas as pd
from datetime import datetime
from ai_therapist import AITherapist
from voice_handler import VoiceHandler
from mood_tracker import MoodTracker
from journal_manager import JournalManager
from session_manager import SessionManager
from config import Config

st.set_page_config(
    page_title="MindCare AI Therapy",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'session_manager' not in st.session_state:
    st.session_state.session_manager = SessionManager()
if 'ai_therapist' not in st.session_state:
    st.session_state.ai_therapist = AITherapist()
if 'voice_handler' not in st.session_state:
    st.session_state.voice_handler = VoiceHandler()
if 'mood_tracker' not in st.session_state:
    st.session_state.mood_tracker = MoodTracker()
if 'journal_manager' not in st.session_state:
    st.session_state.journal_manager = JournalManager()
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = list(Config.VOICE_LANGUAGES.values())[0]

def main():
    st.title("🧠 MindCare AI Therapy Platform")
    st.markdown("*Your personal AI-powered mental health companion*")

    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Choose a feature:",
            ["AI Therapist Chat", "Mood Tracker", "Journal", "Session History", "Settings"]
        )

        st.markdown("---")
        st.subheader("Language Preference")
        selected = st.selectbox("Choose your language:", list(Config.VOICE_LANGUAGES.keys()))
        st.session_state.selected_language = Config.VOICE_LANGUAGES[selected]

        st.markdown("---")
        st.subheader("Quick Stats")
        sessions_count = len(st.session_state.session_manager.get_sessions())
        st.metric("Total Sessions", sessions_count)

        if sessions_count > 0:
            last_session = st.session_state.session_manager.get_latest_session()
            st.metric("Last Session", last_session['date'])

    if page == "AI Therapist Chat":
        ai_therapist_page()
    elif page == "Mood Tracker":
        mood_tracker_page()
    elif page == "Journal":
        journal_page()
    elif page == "Session History":
        session_history_page()
    elif page == "Settings":
        settings_page()

def ai_therapist_page():
    st.header(" AI Therapist Chat")

    col1, col2 = st.columns([3, 1])
    with col1:
        input_mode = st.radio("Input Mode:", ["Text", "Voice"], horizontal=True)
    with col2:
        if st.button("Clear Chat"):
            st.session_state.session_manager.clear_current_session()
            st.rerun()

    chat_container = st.container()
    with chat_container:
        st.subheader("Conversation")
        current_session = st.session_state.session_manager.get_current_session()

        for message in current_session.get('messages', []):
            with st.chat_message(message['role']):
                st.write(message['content'])
                if message.get('emotion'):
                    st.caption(f"Detected emotion: {message['emotion']}")

    st.markdown("---")

    if input_mode == "Text":
        user_input = st.chat_input("Type your message here...")
        if user_input:
            process_user_input(user_input)
    else:
        st.info("Voice input simulation - Click to record")
        if st.button("🎤 Start Recording"):
            st.info("Recording... (This is a simulation)")
            simulated_input = st.text_input("Simulated voice input:", key="voice_sim")
            if simulated_input:
                process_user_input(simulated_input, is_voice=True)

def process_user_input(user_input, is_voice=False):
    st.session_state.session_manager.add_message("user", user_input)

    ai_response = st.session_state.ai_therapist.get_response(
        user_input,
        language=st.session_state.selected_language
    )

    st.session_state.session_manager.add_message("assistant", ai_response)

    if is_voice:
        st.session_state.voice_handler.text_to_speech(ai_response, language=st.session_state.selected_language)

    st.rerun()

def mood_tracker_page():
    st.header("📊 Mood Tracker")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Log Your Mood")

        mood_options = ["😊 Great", "🙂 Good", "😐 Okay", "😔 Low", "😢 Very Low"]
        selected_mood = st.selectbox("How are you feeling?", mood_options)

        energy_level = st.slider("Energy Level", 1, 10, 5)
        anxiety_level = st.slider("Anxiety Level", 1, 10, 5)

        triggers = st.multiselect(
            "What triggered this mood?",
            ["Work", "Family", "Health", "Relationships", "Money", "Sleep", "Other"]
        )

        notes = st.text_area("Additional notes:")

        if st.button("Log Mood"):
            mood_data = {
                'mood': selected_mood,
                'energy': energy_level,
                'anxiety': anxiety_level,
                'triggers': triggers,
                'notes': notes,
                'timestamp': datetime.now().isoformat()
            }
            st.session_state.mood_tracker.log_mood(mood_data)
            st.success("Mood logged successfully!")

    with col2:
        st.subheader("Mood Trends")
        mood_history = st.session_state.mood_tracker.get_mood_history()

        if mood_history:
            df = pd.DataFrame(mood_history)
            if not df.empty:
                st.line_chart(df[['energy', 'anxiety']])
                st.subheader("AI Insights")
                insights = st.session_state.ai_therapist.analyze_mood_patterns(mood_history)
                st.write(insights)
        else:
            st.info("No mood data yet. Start logging to see trends!")

def journal_page():
    st.header("📔 Personal Journal")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Write Your Thoughts")

        if st.button("Get AI Writing Prompt"):
            prompt = st.session_state.ai_therapist.get_journal_prompt(language=st.session_state.selected_language)
            st.info(f"💡 Prompt: {prompt}")

        journal_entry = st.text_area("Your journal entry:", height=300)

        if st.button("Save Entry"):
            if journal_entry.strip():
                entry_data = {
                    'content': journal_entry,
                    'timestamp': datetime.now().isoformat(),
                    'word_count': len(journal_entry.split())
                }
                st.session_state.journal_manager.save_entry(entry_data)
                st.success("Journal entry saved!")
            else:
                st.warning("Please write something before saving.")

    with col2:
        st.subheader("Recent Entries")
        entries = st.session_state.journal_manager.get_recent_entries()

        for i, entry in enumerate(entries[:5]):
            with st.expander(f"Entry {i+1} - {entry['timestamp'][:10]}"):
                st.write(entry['content'][:200] + "..." if len(entry['content']) > 200 else entry['content'])
                st.caption(f"Words: {entry['word_count']}")

def session_history_page():
    st.header("📋 Session History")
    sessions = st.session_state.session_manager.get_sessions()

    if not sessions:
        st.info("No sessions yet. Start chatting with the AI therapist!")
        return

    for session_id, session in sessions.items():
        with st.expander(f"Session {session_id} - {session['date']}"):
            st.write(f"**Duration:** {session.get('duration', 'Unknown')}")
            st.write(f"**Messages:** {len(session.get('messages', []))}")

            for message in session.get('messages', []):
                if message['role'] == 'user':
                    st.write(f"**You:** {message['content']}")
                else:
                    st.write(f"**AI Therapist:** {message['content']}")

def settings_page():
    st.header("⚙️ Settings")

    st.subheader("AI Configuration")
    therapy_approach = st.selectbox(
        "Therapy Approach:",
        ["Cognitive Behavioral Therapy (CBT)", "Dialectical Behavior Therapy (DBT)", 
         "Acceptance and Commitment Therapy (ACT)", "General Supportive"]
    )

    ai_personality = st.selectbox(
        "AI Personality:",
        ["Warm and Empathetic", "Professional and Direct", "Gentle and Patient", "Encouraging and Motivating"]
    )

    language = st.selectbox("Language:", list(Config.VOICE_LANGUAGES.keys()))
    st.session_state.selected_language = Config.VOICE_LANGUAGES[language]

    st.subheader("Privacy & Data")
    auto_delete = st.checkbox("Auto-delete sessions after 30 days", value=True)

    if st.button("Save Settings"):
        settings = {
            'therapy_approach': therapy_approach,
            'ai_personality': ai_personality,
            'language': language,
            'auto_delete': auto_delete
        }
        st.success("Settings saved!")

if __name__ == "__main__":
    main()
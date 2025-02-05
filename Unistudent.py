import streamlit as st
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
import streamlit.components.v1 as components
from datetime import datetime
import json
from exam_module import exam_interface

# Load environment 
load_dotenv()

def initialize_groq():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(client, prompt, system_message="You are a helpful AI assistant. Provide clear and accurate responses to questions."):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            model=os.getenv("GROQ_MODEL", "mixtral-8x7b-32768"),
            temperature=float(os.getenv("AI_TEMPERATURE", "0.7")),
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error getting AI response: {str(e)}"

def analyze_notes(client, notes):
    system_message = """You are an educational analyst. Analyze the following notes and provide:
    1. Main concepts covered
    2. Knowledge gaps or areas needing clarification
    3. Suggestions for better organization
    4. Key points to review
    Be specific and constructive in your feedback."""
    
    return get_ai_response(client, notes, system_message)

def generate_summary(client, notes, topic=None):
    if topic:
        system_message = f"""You are a study assistant. Generate a focused summary of the notes specifically about '{topic}'.
        Include:
        1. Key points about the topic
        2. Related concepts
        3. Important definitions or formulas
        If the topic isn't found in the notes, kindly indicate that."""
    else:
        system_message = """You are a study assistant. Generate a comprehensive summary of these notes.
        Include:
        1. Main topics covered
        2. Key points for each topic
        3. Important concepts and their relationships"""
    
    return get_ai_response(client, notes, system_message)

def format_last_edited(timestamp):
    """Format the last edited timestamp in a Google Docs style"""
    dt = datetime.fromtimestamp(timestamp)
    return f"Last edited {dt.strftime('%I:%M %p')}"

def create_doc_toolbar():
    """Create a Google Docs-style toolbar"""
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 3])
    
    with col1:
        st.button("📝", help="Edit")
    with col2:
        st.button("🔍", help="Search")
    with col3:
        st.button("💾", help="Save")
    with col4:
        st.button("📤", help="Share")
    with col5:
        st.button("⚙️", help="Settings")

def main():
    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY not found in environment variables. Please check your .env file.")
        return

    st.set_page_config(layout="wide", page_title="Interactive Learning Platform")
    client = initialize_groq()
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'notes' not in st.session_state:
        st.session_state.notes = []
    if 'current_note' not in st.session_state:
        st.session_state.current_note = None
    if 'show_analysis' not in st.session_state:
        st.session_state.show_analysis = False

    st.title("Interactive Learning Platform")

    #  Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Whiteboard", "AI Chat", "Notes", "Exams"])

    # Whiteboard Tab
    with tab1:
        st.header("Interactive Whiteboard")
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=int(os.getenv("CANVAS_STROKE_WIDTH", "2")),
            stroke_color="#000000",
            background_color="#ffffff",
            height=int(os.getenv("CANVAS_HEIGHT", "400")),
            drawing_mode="freedraw",
            key="canvas",
        )
        
        if canvas_result.image_data is not None and st.button("Analyze Whiteboard"):
            st.info("Whiteboard analysis feature will be integrated with OCR + Groq AI in the next update.")

    # AI Chat Tab
    with tab2:
        st.header("AI Chat Assistant")
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("Ask anything..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_ai_response(client, prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.experimental_rerun()

    # Notes Tab
    with tab3:
        # Left sidebar for document list and tools
        with st.sidebar:
            st.subheader("My Documents")
            
            # New document button
            if st.button("+ New Document"):
                new_note = {
                    "title": "Untitled Document",
                    "content": "",
                    "created": datetime.now().timestamp(),
                    "last_edited": datetime.now().timestamp(),
                    "id": len(st.session_state.notes)
                }
                st.session_state.notes.append(new_note)
                st.session_state.current_note = new_note["id"]
            
            # List of existing documents
            for note in st.session_state.notes:
                if st.button(
                    f"📄 {note['title']}\n{format_last_edited(note['last_edited'])}",
                    key=f"doc_{note['id']}"
                ):
                    st.session_state.current_note = note["id"]
                    
            # Search and Analysis Tools
            st.sidebar.divider()
            st.sidebar.subheader("Tools")
            
            # Search through notes
            search_query = st.sidebar.text_input("🔍 Search in notes...")
            if search_query:
                st.sidebar.markdown("### Search Results")
                for note in st.session_state.notes:
                    if search_query.lower() in note['content'].lower() or search_query.lower() in note['title'].lower():
                        st.sidebar.markdown(f"Found in: **{note['title']}**")

        # Main document area
        col1, col2 = st.columns([3, 2])
        
        with col1:
            if st.session_state.current_note is not None:
                current_note = next(
                    (note for note in st.session_state.notes 
                     if note["id"] == st.session_state.current_note), 
                    None
                )
                
                if current_note:
                    # Document toolbar
                    create_doc_toolbar()
                    
                    # Title input
                    new_title = st.text_input(
                        "Title",
                        value=current_note["title"],
                        key=f"title_{current_note['id']}"
                    )
                    
                    # Content area with rich text editor
                    new_content = st.text_area(
                        "Content",
                        value=current_note["content"],
                        height=500,
                        key=f"content_{current_note['id']}"
                    )
                    
                    # Auto-save functionality
                    if new_title != current_note["title"] or new_content != current_note["content"]:
                        current_note["title"] = new_title
                        current_note["content"] = new_content
                        current_note["last_edited"] = datetime.now().timestamp()
                        st.session_state.notes = [
                            note if note["id"] != current_note["id"] else current_note 
                            for note in st.session_state.notes
                        ]

        # Analysis panel
        with col2:
            if st.session_state.current_note is not None:
                st.markdown("### Analysis Tools")
                show_analysis = st.toggle("Show Analysis Tools", False)
                
                if show_analysis:
                    current_note = next(
                        (note for note in st.session_state.notes 
                         if note["id"] == st.session_state.current_note),
                        None
                    )
                    
                    if current_note:
                        # Generate summary
                        if st.button("Generate Summary"):
                            with st.spinner("Generating summary..."):
                                summary = generate_summary(client, current_note["content"])
                                st.markdown("#### Summary")
                                st.markdown(summary)
                        
                        # Topic-specific summary
                        topic = st.text_input("Summarize specific topic:")
                        if topic and st.button("Generate Topic Summary"):
                            with st.spinner("Generating topic summary..."):
                                topic_summary = generate_summary(client, current_note["content"], topic)
                                st.markdown(f"#### Summary: {topic}")
                                st.markdown(topic_summary)
                        
                        # Analyze notes
                        if st.button("Analyze Notes"):
                            with st.spinner("Analyzing notes..."):
                                analysis = analyze_notes(client, current_note["content"])
                                st.markdown("#### Analysis")
                                st.markdown(analysis)

    # Exams Tab
    with tab4:
        exam_interface() 

if __name__ == "__main__":
    main()
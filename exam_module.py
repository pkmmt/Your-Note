import streamlit as st
from groq import Groq
import json
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

class ExamQuestion:
    def __init__(self, question_text, correct_answer, marks, question_type="text", options=None):
        self.question_text = question_text
        self.correct_answer = correct_answer
        self.marks = marks
        self.question_type = question_type  # "text", "mcq", "true_false"
        self.options = options if options else []

class Exam:
    def __init__(self, title, subject, duration_minutes, questions):
        self.title = title
        self.subject = subject
        self.duration_minutes = duration_minutes
        self.questions = questions
        self.total_marks = sum(q.marks for q in questions)

def grade_answer(client, student_answer, question, detailed_feedback=True):
    """
    Grade a student's answer using AI and provide feedback
    """
    system_message = f"""You are an expert exam grader for {question.question_type} questions.
    Grade the following answer and provide:
    1. Mark awarded out of {question.marks}
    2. Explanation of any mistakes
    3. Correct approach or solution
    4. Tips for improvement
    
    Question: {question.question_text}
    Correct Answer: {question.correct_answer}
    Student Answer: {student_answer}
    
    Provide the response in JSON format with keys: 
    marks_awarded, explanation, correct_solution, improvement_tips
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": "Grade this answer"}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.3
        )
        
        feedback = json.loads(response.choices[0].message.content)
        return feedback
    except Exception as e:
        return {
            "marks_awarded": 0,
            "explanation": f"Error grading answer: {str(e)}",
            "correct_solution": "Error retrieving solution",
            "improvement_tips": "Please try again"
        }

def analyze_exam_performance(client, exam_results):
    """
    Analyze overall exam performance and provide study recommendations
    """
    analysis_prompt = f"""
    Analyze the following exam results and provide:
    1. Overall performance analysis
    2. Areas of strength
    3. Areas needing improvement
    4. Specific study recommendations
    5. Practice suggestions
    
    Results: {json.dumps(exam_results)}
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an educational analyst specializing in exam performance analysis."},
                {"role": "user", "content": analysis_prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing performance: {str(e)}"

def exam_interface():
    st.title("Interactive Exam Platform")
    
    # Initialize session state for exam data
    if 'current_exam' not in st.session_state:
        st.session_state.current_exam = None
    if 'exam_results' not in st.session_state:
        st.session_state.exam_results = []
    if 'exam_in_progress' not in st.session_state:
        st.session_state.exam_in_progress = False
    
    # tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["Take Exam", "Review Results", "Upload Exam"])
    
    # Exam Tab
    with tab1:
        if st.session_state.exam_in_progress:
            display_exam()
        elif st.session_state.current_exam:
            if st.button("Start Exam"):
                st.session_state.exam_in_progress = True
                st.session_state.start_time = datetime.now()
            st.info("Please upload an exam in the Upload Exam tab")
    
    #Results Tab
    with tab2:
        if st.session_state.exam_results:
            display_results()
        else:
            st.info("No exam results to display")
    
    # upload Exam Tab
    with tab3:
        upload_exam()

def display_exam():
    exam = st.session_state.current_exam
    st.header(exam.title)
    
    # display timer
    time_elapsed = datetime.now() - st.session_state.start_time
    time_remaining = exam.duration_minutes * 60 - time_elapsed.total_seconds()
    
    if time_remaining <= 0:
        st.warning("Time's up! Please submit your answers.")
        submit_exam()
        return
    
    st.progress(time_remaining / (exam.duration_minutes * 60))
    st.write(f"Time remaining: {int(time_remaining // 60)} minutes {int(time_remaining % 60)} seconds")
    
    # display questions
    answers = {}
    for i, question in enumerate(exam.questions):
        st.subheader(f"Question {i + 1} ({question.marks} marks)")
        st.write(question.question_text)
        
        if question.question_type == "mcq":
            answers[i] = st.radio(f"Select answer for question {i + 1}:", 
                                question.options,
                                key=f"q_{i}")
        elif question.question_type == "true_false":
            answers[i] = st.radio(f"Select answer for question {i + 1}:", 
                                ["True", "False"],
                                key=f"q_{i}")
        else:
            answers[i] = st.text_area(f"Your answer for question {i + 1}:",
                                    key=f"q_{i}")
    
    if st.button("Submit Exam"):
        submit_exam(answers)

def submit_exam(answers=None):
    if not answers:
        answers = {}
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    results = []
    
    for i, question in enumerate(st.session_state.current_exam.questions):
        if i in answers:
            feedback = grade_answer(client, answers[i], question)
            results.append({
                "question_number": i + 1,
                "question_text": question.question_text,
                "student_answer": answers[i],
                "feedback": feedback
            })
    
    st.session_state.exam_results = results
    st.session_state.exam_in_progress = False
def display_results():
    st.header("Exam Results")
    
    total_marks = 0
    available_marks = 0
    
    for result in st.session_state.exam_results:
        st.subheader(f"Question {result['question_number']}")
        st.write("Question:", result["question_text"])
        st.write("Your Answer:", result["student_answer"])
        
        feedback = result["feedback"]
        marks = feedback["marks_awarded"]
        total_marks += marks
        available_marks += st.session_state.current_exam.questions[result['question_number']-1].marks
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Marks", f"{marks}/{st.session_state.current_exam.questions[result['question_number']-1].marks}")
        
        with col2:
            with st.expander("See detailed feedback"):
                st.write("Explanation:", feedback["explanation"])
                st.write("Correct Solution:", feedback["correct_solution"])
                st.write("Tips for Improvement:", feedback["improvement_tips"])
    
    # performance
    st.header("Overall Performance")
    st.metric("Total Score", f"{total_marks}/{available_marks}")
    
    # Get AI analysis of  performance
    if st.button("Generate Performance Analysis"):
        Groq(api_key=os.getenv("GROQ_API_KEY"))
        analysis = analyze_exam_performance(client, st.session_state.exam_results)
        st.write(analysis)

def upload_exam():
    st.header("Upload New Exam")
    
    # Example exam upload form
    title = st.text_input("Exam Title")
    subject = st.text_input("Subject")
    duration = st.number_input("Duration (minutes)", min_value=1, value=60)
    
    st.subheader("Add Questions")
    questions = []
    
    num_questions = st.number_input("Number of Questions", min_value=1, value=1)
    
    for i in range(int(num_questions)):
        st.write(f"Question {i + 1}")
        question_type = st.selectbox(f"Question Type for Q{i + 1}", 
                                   ["text", "mcq", "true_false"],
                                   key=f"type_{i}")
        
        question_text = st.text_area(f"Question Text for Q{i + 1}", key=f"text_{i}")
        marks = st.number_input(f"Marks for Q{i + 1}", min_value=1, value=1, key=f"marks_{i}")
        
        options = None
        if question_type == "mcq":
            num_options = st.number_input(f"Number of Options for Q{i + 1}", 
                                        min_value=2, value=4, key=f"num_opt_{i}")
            options = []
            for j in range(int(num_options)):
                option = st.text_input(f"Option {j + 1} for Q{i + 1}", key=f"opt_{i}_{j}")
                options.append(option)
        
        correct_answer = st.text_area(f"Correct Answer for Q{i + 1}", key=f"ans_{i}")
        
        questions.append(ExamQuestion(question_text, correct_answer, marks, 
                                   question_type, options))
    
    if st.button("Create Exam"):
        exam = Exam(title, subject, duration, questions)
        st.session_state.current_exam = exam
        st.success("Exam created successfully!")

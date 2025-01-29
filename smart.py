import streamlit as st
from transformers import pipeline


@st.cache_resource
def get_model():
    return pipeline("text2text-generation", model="google/flan-t5-large")

explanation_model = get_model()

@st.cache_data
def llm(prompt: str, **kwargs):
    return explanation_model(prompt, **kwargs)


st.session_state.setdefault("button_clicked", False)
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []  
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = []  
if "quiz_selected" not in st.session_state:
    st.session_state.quiz_selected = {}  


col1, col2 = st.columns([1, 5])
with col1:
    st.image("student.png", width=80)  # Small logo
with col2:
    st.markdown("<h1 style='color: blue;'>Smart Study Buddy</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: gray;'>Your AI-Powered Learning Assistant</h3>", unsafe_allow_html=True)


st.text(" ")
st.text(" ")


user_input = st.text_area("💡 Enter a topic, concept, or text to learn about:", height=200, placeholder="Type something here...")


task = st.selectbox(
    "🛠️ What do you want to do?",
    ["Summarize Text", "Explain Concept", "Generate Questions", "Interactive Quiz"]
)


if st.button("🚀 Get Results") or st.session_state.button_clicked:
    st.session_state.button_clicked = True
    if user_input:
        if task == "Summarize Text":
            prompt = f"Summarize the following text concisely and avoid repetition: {user_input}"
            response = llm(prompt, max_length=150, min_length=30, num_return_sequences=1)
            st.markdown("<h3 style='color: green;'>Summary:</h3>", unsafe_allow_html=True)
            st.write(response[0]["generated_text"])
        
        elif task == "Explain Concept":
            prompt = f"Explain the following concept in simple terms: {user_input}"
            response = llm(prompt, max_length=150, min_length=30, num_return_sequences=1)
            st.markdown("<h3 style='color: green;'>Explanation:</h3>", unsafe_allow_html=True)
            st.write(response[0]["generated_text"])
        
        elif task == "Generate Questions":
            prompt = f"Generate 3 questions based on the following text: {user_input}"
            st.markdown("<h3 style='color: green;'>Generated Questions:</h3>", unsafe_allow_html=True)
            for i in range(3):  
                response = llm(prompt, max_length=150, num_return_sequences=1, do_sample=True)
                st.markdown(f"<div style='border:1px solid #ddd; padding:10px; margin:10px; border-radius:5px;'>"
                            f"<strong>Question {i+1}:</strong> {response[0]['generated_text']}</div>",
                            unsafe_allow_html=True)
        
        elif task == "Interactive Quiz":
            if not st.session_state.quiz_questions:
                for i in range(1):  
                    prompt =("Generate three multiple-choice questions based on the provided text. "
                              "Make sure that the output follows the following format:\n"
                              "The first line is the question, the following four lines are the choices. Followed by a single line for the answer and an empty line seperating the questions.\n\n"
                              "For Example:\n"
                              "What is the capital of France?\n"
                              "A) Paris\n"
                              "B) London\n"
                              "C) Berlin\n"
                              "D) Madrid\n"
                              "A\n\n"
                              "Context:\n"
                              f"{user_input}.")
                    response = llm(prompt, max_length=1000, num_return_sequences=1, do_sample=True)
                    question = response[0]["generated_text"]
                    st.write(repr(question))
                    # question, *options, answer = response[0]["generated_text"].split("\n")
                    options = [
                        "Option A: Correct Answer",
                        "Option B: Incorrect Option 1",
                        "Option C: Incorrect Option 2",
                        "Option D: Incorrect Option 3"
                    ]
                    st.session_state.quiz_questions.append((question, options))
                    st.session_state.quiz_answers.append("Option A: Correct Answer")
            
            
            st.markdown("<h3 style='color: green;'>Interactive Quiz:</h3>", unsafe_allow_html=True)
            for i, (question, options) in enumerate(st.session_state.quiz_questions):
                st.markdown(f"{i+1}. {question}")
                selected_option = st.radio(f"Select your answer for Question {i+1}:", options, key=f"quiz_{i}", on_change=lambda: None)
                st.session_state.quiz_selected[f"quiz_{i}"] = selected_option
                if st.button(f"Check Answer for Question {i+1}", key=f"check_{i}"):
                    if selected_option == st.session_state.quiz_answers[i]:
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Incorrect! The correct answer is: {st.session_state.quiz_answers[i]}")
    else:
        st.warning("⚠️ Please enter a topic or text first!")


st.sidebar.title("About Smart Study Buddy")
st.sidebar.info("This app helps you learn concepts, summarize texts, generate questions, and explore examples using AI.")
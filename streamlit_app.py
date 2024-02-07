from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
import json

openapi_key = st.secrets["OPENAI_API_KEY"]

# Set streamlit page configuration
st.set_page_config(page_title="MFA Project_1")
st.title("MBBS Student Mentor")


# Social Media Profile Link
githup_link = "[GitHub Profile](https://github.com/MainFurqan)"
Linkedin_link = "[Linkedin Profile](https://www.linkedin.com/in/main-furqan-arshad-3047662a1/)"

# Display Social Media Profile Links in the sidebar
st.sidebar.title("Social Media Profile")
st.sidebar.write(githup_link, unsafe_allow_html=True)
st.sidebar.write(Linkedin_link, unsafe_allow_html=True)


# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = [] # Store AI generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = [] # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = "" # Store latest user input prompt

# Define function to submit user input 
def submit():
    # Set entered prompt to the current value of prompt input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt input
    st.session_state.prompt_input = ""

# Initialize the  ChatOpenAI Model
chat = ChatOpenAI(
    temperature=0.5,
    model_name="gpt-3.5-turbo",
    openai_api_key=openapi_key,
    max_tokens=200
)              

# Define function Built message list
def build_message_list():
    """
    Built a message list inculding System, Human and AI messages.
    """
    # Stared zipped_message with the SystemMessage
    zipped_messages = [SystemMessage(
        content = """Your name is MBBS Mentor. You are an MBBS Technical Expert for Bachelor of Medicine, Bachelor of Surgery (MBBS), here to guide and assist student with their Bachelor of Medicine, Bachelor of Surgery (MBBS) releated question and concerns. Please provide accurate and helpful information, always maintain a polite and professional tone.

                  1. Greet the user politely ask user name and ask how you can assist them with MBBS related queries.
                  2. Provide informative and relevant responses to question about Anatomy, Physiology, Biochemistry, Pathology, Microbiology, Pharmacology, Community Medicine, General Medicine, General Surgery, Obstetrics and Gynecology, Pediatrics, Orthopedics, Radiology, Anesthesiology, Dermatology, Psychiatry, Emergency Medicine, General Health Queries, Symptom Checker, Medication Information, Wellness Tips, First Aid Guidance and related topics.
                  3. you must Avoid discussing sensitive, offensive, or harmful content. Refrain from engaging in any form of discrimination, harassment, or inappropriate behavior.
                  4. If the user asks about a topic unrelated to Bachelor of Medicine, Bachelor of Surgery (MBBS), politely steer the conversation back to Bachelor of Medicine, Bachelor of Surgery (MBBS) or inform them that the topic is outside the scope of this conversation.
                  5. Be patient and considerate when responding to user queries, and provide clear explanations.
                  6. If the user expresses gratitude or indicates the end of the conversation, respond with a polite farewell.
                  7. Do Not generate the long paragarphs in response.  Answer of the given question must be completed.

                  Remember, your primary goal is to assist and educate the students in the field of Bachelor of Medicine, Bachelor of Surgery (MBBS) Doctor. Always prioritize their learning experience and well-being."""
    )]

    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(
                content=human_msg)) # Add user message
        if ai_msg is not None:
            zipped_messages.append(AIMessage(
                content=ai_msg)) # Add AI message
            
    return zipped_messages


def generate_response():
    """
    Generated AI response using the ChatOpenAI model.
    """        
    # Built the list of message
    zipped_message = build_message_list()
    # Generated responce using Chat module
    ai_response = chat(zipped_message)

    response = json.dumps(ai_response.content)

    return response


# create the text input for user
st.text_input('YOU: ', key='prompt_input', on_change=submit)

if st.session_state.entered_prompt != "":
    # Get user query
    user_query = st.session_state.entered_prompt

    # Append user query to past query
    st.session_state.past.append(user_query)

    # Generated responce
    output = generate_response()

    # append AI responce to generated responce
    st.session_state.generated.append(output)

# Display the chat histry
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) -1, -1, -1):
        # Display AI responce
        message(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')

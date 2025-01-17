import streamlit as st
import cohere
import fitz # An alias for the PyMuPDF library.
from elevenlabs import *
#from elevenlabs.api.error import UnauthenticatedRateLimitError, RateLimitError
import speech_recognition as sr
r = sr.Recognizer()
def pdf_to_documents(pdf_path):
    """
    Converts a PDF to a list of 'documents' which are chunks of a larger document that can be easily searched
    and processed by the Cohere LLM. Each 'document' chunk is a dictionary with a 'title' and 'snippet' key

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list: A list of dictionaries representing the documents. Each dictionary has a 'title' and 'snippet' key.
        Example return value: [{"title": "Page 1 Section 1", "snippet": "Text snippet..."}, ...]
    """

    doc = fitz.open(pdf_path)
    documents = []
    text = ""
    chunk_size = 1000
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        part_num = 1
        for i in range(0, len(text), chunk_size):
            documents.append({"title": f"Page {page_num + 1} Part {part_num}", "snippet": text[i:i + chunk_size]})
            part_num += 1
    return documents


api_key_found = False
if hasattr(st, "secrets"):
    if "COHERE_API_KEY" in st.secrets.keys():
        if st.secrets["COHERE_API_KEY"] not in ["", "PASTE YOUR API KEY HERE"]:
            api_key_found = True

# Add a sidebar to the Streamlit app
with st.sidebar:
    with st.expander(label="llElevenLabs", expanded=False):
        st.caption(
            "The basic API has a limited number of characters. To increase this limit, you can get a free API key from [llElevenLabs](https://beta.elevenlabs.io/subscription)")
        API_KEY = st.text_input(label="API KEY")

    st.title("Text to Voice")
    english = st.radio(
        label="Choose your language", options=['English', 'Multilingual'], index=0, horizontal=True)

    value = "I am the machine." if english == 'English' else "बस बातें अपने जैसे करते है"
    text = st.text_area(label="Enter the text here",
                        value=value, max_chars=30 if not API_KEY else None)

    if api_key_found:
        cohere_api_key = st.secrets["COHERE_API_KEY"]
        # st.write("API key found.")
    else:
        cohere_api_key = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
        st.markdown("[Get a Cohere API Key](https://dashboard.cohere.ai/api-keys)")

    level_two_options = {
        "Intermediate 1": ["not completed yet"],
        "Intermediate 3": ["Unit 1.1", "Unit 1.2", "Unit 2.1", "Unit 2.2", "Unit 3.1"],
        "Intermediate 5": ["Not Completed yet"]
    }

    first_choice = "Intermediate 1"
    first_choice = st.selectbox("Chinese Level", ["Intermediate 1", "Intermediate 3", "Intermediate 5"])
    second_choice = st.selectbox("Chinese Unit", level_two_options[first_choice])

    st.write(f"Currently Selected: {second_choice}, in {first_choice}")
    st.image("XiaoMing.jpg", caption="Xiao Ming, Your friend!!! 😊😊")


st.title("Xiao Ming Bot")
st.write(f"Xiao ming is here to help!")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "Chatbot",  "text": "Hi! I’m Xiao Ming, Your Chinese Study Buddy. \n Select your current Chinese level from the dropdown, then tell me what you’d like to practice—whether it’s speaking, vocabulary, or sentence structures. I’ll guide you through real-time conversations, help you master ETK words and phrases, and give you instant feedback to improve your skills. Let’s make learning Chinese fun and effective! \n 你准备好了吗？(Are you ready?) Let’s get started! 😊"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["text"])


audio_value = st.audio_input("Record a voice message")

if audio_value:
    st.audio(audio_value)
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        st.write("did you say:" + r.recognize_google(audio_value))
    except sr.UnknownValueError:
        st.write("wo bu keyi ting ni")
    except sr.RequestError as e:
        st.write("Could not request results from Google Speech Recognition service; {0}".format(e))
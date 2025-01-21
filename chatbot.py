import streamlit as st
import cohere
import fitz # An alias for the PyMuPDF library.
from elevenlabs import *
#from elevenlabs.api.error import UnauthenticatedRateLimitError, RateLimitError
import speech_recognition as sr
r = sr.Recognizer()
from pydub import AudioSegment, silence
import os
import azure.cognitiveservices.speech as speechsdk



import os
recog=sr.Recognizer()
final_result=""
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
    with st.expander(label="ElevenLabs TTS", expanded=False):
        st.caption(
            "The basic API has a limited number of characters. To increase this limit, you can get a free API key from [llElevenLabs](https://beta.elevenlabs.io/subscription)")
        API_KEY = st.text_input(label="API KEY")
        client = ElevenLabs(
            api_key=API_KEY,  # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
        )
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

def recognize_from_microphone(audio):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = audio

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return(speech_recognition_result.text)
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        return("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
            return ("error Did you set the speech resource key and region values?")
        else:
            return ("Speech Recognition canceled: {}".format(cancellation_details.reason))


def split():
    audio_segment = AudioSegment.from_file(audio)
    chunks = silence.split_on_silence(audio_segment, min_silence_len=500, silence_thresh=audio_segment.dBFS - 20,
                                      keep_silence=100)
    for index, chunk in enumerate(chunks):
        chunk = chunk + 20
        chunk.export(str(index) + ".wav", format="wav")
        with sr.AudioFile(str(index) + ".wav") as source:
            #recorded =
            try:
                text = recognize_from_microphone(recorded)
                final_result = final_result + " " + text
                print(text)
            except:
                print("None")
                final_result = final_result + " Unaudible"
audio = st.audio_input("Record a voice message")
if audio:
    st.audio(audio)
    audio_segment = AudioSegment.from_file(audio)
    chunks = silence.split_on_silence(audio_segment, min_silence_len=500, silence_thresh=audio_segment.dBFS - 20,
                                      keep_silence=100)
    for index, chunk in enumerate(chunks):
        chunk = chunk + 20
        chunk.export(str(index) + ".wav", format="wav")
        with sr.AudioFile(str(index) + ".wav") as source:
            try:
                text = recognize_from_microphone(source)
                final_result = final_result + " " + text
                print(text)
            except:
                print("None")
                final_result = final_result + " Unaudible"
    with st.form("Result"):
        result=st.text_area("TEXT", value=final_result)
        d_btn=st.form_submit_button("Say it")
        if d_btn:
            audio = client.generate(
                text=final_result,
                voice="Brian",
                model="eleven_multilingual_v2"
            )
            play(audio)
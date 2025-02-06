import streamlit as st
import cohere
import fitz # An alias for the PyMuPDF library.
from elevenlabs import *
#from elevenlabs.api.error import UnauthenticatedRateLimitError, RateLimitError
from pydub import AudioSegment, silence
import os
import azure.cognitiveservices.speech as speechsdk



import os

final_result=""
def pdf_to_documents(pdf_path):
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
            cohere_api_key = st.secrets["COHERE_API_KEY"]
    if "ElevenLabsKey" in st.secrets.keys():
        if st.secrets["ElevenLabsKey"] not in ["", "PASTE YOUR API KEY HERE"]:
            api_key_found1 = True



# Add a sidebar to the Streamlit app
with st.sidebar:
    with st.expander(label="ElevenLabs TTS", expanded=False):
        st.caption(
            "NOTE: Not needed if you put the key in Secrets.toml under ElevenLabsKey. \n The basic API has a limited number of characters. To increase this limit, you can get a free API key from [llElevenLabs](https://beta.elevenlabs.io/subscription)")
        API_KEY = st.text_input(label="API KEY")
        if api_key_found1:
            client = ElevenLabs(api_key=st.secrets["ElevenLabsKey"])
        else:
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
    if second_choice == "Unit 2.2":
        my_documents = pdf_to_documents('docs/L2.2 Learning Goals 逛夜市.pdf')
    elif second_choice == "Unit 3.1":
        my_documents = pdf_to_documents('docs/L3.1 Learning Targets.pdf'
    else:
        my_documents = pdf_to_documents('docs/L2.2 Learning Goals 逛夜市.pdf')

    st.image("XiaoMing.jpg", caption="Xiao Ming, Your friend!!! 😊😊")


st.title("Xiao Ming Bot")
st.write(f"Xiao ming is here to help!")


coclient = cohere.Client(api_key=cohere_api_key)
preamble = """
Your name is xiao ming, a chinese man who talks to people. You have engaged in a conversation with the user. Answer normally and relatively short and ask something for the user, like a conversation.
The user, based on the unit, has goals based on the PDF. The user practices conversation with you, and you help them with their goals. These include ETK (Essential to Know) words and phrases, sentence structures, and vocabulary. Not only that, but the general topic per unit is also important.
"""
text = "Hi! I’m Xiao Ming, Your Chinese Study Buddy. \n Select your current Chinese level from the dropdown, then tell me what you’d like to practice—whether it’s speaking, vocabulary, or sentence structures. I’ll guide you through real-time conversations, help you master ETK words and phrases, and give you instant feedback to improve your skills. Let’s make learning Chinese fun and effective! \n 你准备好了吗？(Are you ready?) Let’s get started! 😊"
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "Chatbot",  "text": text}]
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["text"])

def send(prompt):
    #chat_history_str = "\n".join([msg["text"] for msg in st.session_state.messages])
    print(prompt)
    response = coclient.chat(
        chat_history=st.session_state.messages,
        message=prompt,
        prompt_truncation='AUTO',
        preamble=preamble
    )
    # print("Promt = ", result)
    # Add the user prompt to the chat history
    st.session_state.messages.append({"role": "User", "text": result})
    # Add the response to the chat history
    msg = response.text
    st.session_state.messages.append({"role": "Chatbot", "text": msg})
    # Write the response to the chat window
    st.chat_message("Chatbot", avatar="XiaoMing.jpg").write(msg)
    audio = client.generate(
        text=msg,
        voice="Brian",
        model="eleven_multilingual_v2"
    )
    play(audio)

    #st.write(response.text)
    #print = response.text


# prompt = result
# Send the user message and pdf text to the model and capture the response

with st.chat_message("ai", avatar="XiaoMing.jpg"):
    d_btn = st.button("Say it")
    if d_btn:
        audio = client.generate(
            text=text,
            voice="Brian",
            model="eleven_multilingual_v2"
        )
        play(audio)

def recognize_from_microphone(audio):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=st.secrets.SPEECH_KEY, region=st.secrets.SPEECH_REGION)
    speech_config.speech_recognition_language="zh-CN"

    print("audio input:", audio)
    #audio_config = speechsdk.audio.AudioConfig(filename=str(audio))
    audio_config = speechsdk.audio.AudioConfig(filename=str(audio))
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Processing")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

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
    chunks = silence.split_on_silence(audio_segment, min_silence_len=500, silence_thresh=audio_segment.dBFS - 20, keep_silence=100)
    for index, chunk in enumerate(chunks):
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
        chunk.export(str(index) + ".wav", format="wav")
        print(str(index) + ".wav")
        text = recognize_from_microphone(str(index) + ".wav")
        final_result = final_result + " " + text
        print(text)
    result = ""
    with st.form("Result"):
        result=st.text_area("TEXT", value=final_result)
        d_btn=st.form_submit_button("Say it and send")
        if d_btn:
            audio = client.generate(
                text=result,
                voice="Brian",
                model="eleven_multilingual_v2"
            )
            play(audio)
    send(result)


# Stop responding if the user has not added the Cohere API key
if not cohere_api_key:
    st.info("Please add your Cohere API key to continue.")
    st.stop()

# Create a connection to the Cohere API

# XiaoMingBot
Xiao Ming: Your Real-Time Chinese Language Partner and Study Buddy!

This bot is xiao ming, the man in your chinese class! talk with him to help

Meet Xiao Ming: Your Real-Time Chinese Language Partner and Study Buddy!

Xiao Ming is an advanced LLM-powered bot designed to help you master Chinese in a fun, interactive, and educational way. Whether you're a beginner or an advanced learner, Xiao Ming is here to guide you through the nuances of the language, with a special focus on school-related vocabulary, sentence structures, and ETK (Expected to Know) words!
Key Features of Xiao Ming:

    Real-Time Conversation Practice:

        Chat with Xiao Ming in real-time to improve your speaking and listening skills.

        Receive instant feedback on your pronunciation, grammar, and fluency.

    ETK Vocabulary and Sentence Structures:

        Xiao Ming incorporates Essential Terminology and Knowledge (ETK) into your conversations, helping you master the words and phrases commonly used in school settings.

        Learn how to construct sentences that are essential for exams, presentations, and everyday classroom interactions.

    Personalized Feedback:

        Xiao Ming analyzes your responses and provides tailored suggestions to improve your Chinese.

        Whether it’s correcting tones, suggesting better word choices, or explaining grammar rules, Xiao Ming ensures you learn effectively.

    Interactive Learning:

        Engage in role-playing scenarios like ordering food, asking for directions, or participating in a classroom discussion.

        Xiao Ming adapts to your skill level, making each conversation challenging yet achievable.

    Cultural Insights:

        Beyond language, Xiao Ming shares cultural tips and context to help you understand the "why" behind certain phrases and expressions.

    Progress Tracking:

        Track your improvement over time with Xiao Ming’s built-in progress reports.

        Set goals and celebrate milestones as you become more confident in your Chinese skills.

Why Choose Xiao Ming?

    School-Focused Learning: Xiao Ming is designed with students in mind, ensuring you learn the vocabulary and structures that matter most in academic settings.

    24/7 Availability: Practice anytime, anywhere—Xiao Ming is always ready to chat!

    Fun and Engaging: Learning Chinese doesn’t have to be boring. Xiao Ming makes every conversation enjoyable and rewarding.

Whether you're preparing for exams, improving your conversational skills, or just exploring the Chinese language, Xiao Ming is your go-to companion for mastering Chinese in a way that’s practical, engaging, and effective. Start chatting with Xiao Ming today and take your Chinese skills to the next level!

你准备好了吗？(Are you ready?) Let’s learn together! 😊


## Installation: 


   > pip install -r requirements.txt

   Substitute `pip` for `pip3` if you have problems with this.

1. Type the following terminal commands to create the necessary secrets file. Not having this will result in an error.

   > mkdir .streamlit

   > touch .streamlit/secrets.toml

   > echo "COHERE_API_KEY = 'PASTE YOUR API KEY HERE'" > .streamlit/secrets.toml

4. Run the app by typing the following command in the terminal window. 
   > streamlit run chatbot.py
   
   A new browser window will open where you can interact with the chatbot.

   > [!NOTE]
   > If you didn't paste a valid Cohere API key into your secrets file you will need to enter it into the sidebar for the chatbot to work.

5. Add a valid Microsoft Azure Speech API Key into secrets.toml under the name SPEECH_KEY and SPEECH_REGION

   > This is so Xiao Ming can hear you!
   
   It should be this:
   ```
    SPEECH_KEY = "(Api key)"
    SPEECH_REGION = "(Region)"
   ```
   > Go here for more information: https://shorturl.at/WE8Vu

6. Make minor changes to the code, save and then run your app again to see what happens.

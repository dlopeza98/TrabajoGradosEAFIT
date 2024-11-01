# Libraries
import base64
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load secrets and client configurations
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
fine_tuned_model_id = os.getenv("ID_MODEL_OPENAI")

system_message = """
You are an advanced assistant specialized in analyzing and detecting emotions in short text. 
Your role is to identify the underlying emotion conveyed in each input and provide the most accurate emotional classification between: shame, sadness, joy, guilt, fear, disgust and anger"
"""


# Function to create the user message (prompt) for emotion detection
def create_user_message(input_text: str) -> str:
    """
    Creates a formatted user prompt for emotion detection.

    Args:
        input_text (str): The text input from the user.

    Returns:
        str: A formatted string prompt for the model.
    """
    if not isinstance(input_text, str):
        raise TypeError("input_text must be a string.")
    return f"Text: {input_text}\n\nWhat is the emotion expressed in this text?"


def detect_emotion(
    input_text: str, system_message: str, fine_tuned_model_id: str
) -> str:
    """
    Detects the emotion expressed in the given text using a fine-tuned model.

    Args:
        input_text (str): The text input from the user.
        system_message (str): The system message providing context for the model.
        fine_tuned_model_id (str): The ID of the fine-tuned model to use.

    Returns:
        str: The detected emotion.

    Raises:
        TypeError: If any of the inputs are not strings.
    """
    # Input type checking
    if not all(
        isinstance(arg, str)
        for arg in [input_text, system_message, fine_tuned_model_id]
    ):
        raise TypeError("All inputs must be strings.")

    # Prepare messages for the model
    input_message = []
    input_message.append({"role": "system", "content": system_message})
    user_input_text = create_user_message(input_text)
    input_message.append({"role": "user", "content": user_input_text})

    # Call the OpenAI API to get the response
    response = client.chat.completions.create(
        model=fine_tuned_model_id, messages=input_message, temperature=0, max_tokens=4
    )

    # Extract the emotion from the response
    emotion = response.choices[0].message.content.strip()

    # Output type checking
    if not isinstance(emotion, str):
        raise TypeError("The response from the model is not a string.")

    return emotion


emotion_emojis = {
    "joy": "😊",
    "fear": "😨",
    "disgust": "🤢",
    "guilt": "😔",
    "shame": "😳",
    "sadness": "😢",
    "anger": "😡",
}


def main():
    # Load the logo and convert it to base64 for displaying
    logo_url = "logo/DELTA-WITS-LOGO-WHITE.png"  # Replace with your logo file path
    try:
        with open(logo_url, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        st.error("Logo image not found. Please check the file path.")
        return

    # Display header and clickable logo
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 700px; margin: auto; padding-top: 18px;">
            <h1 style="margin: 0; font-size: 2.5em; font-weight: bold; color: white;">Janus</h1>
            <a href="https://www.deltawits.com" target="_blank">
                <img src="data:image/png;base64,{logo_base64}" style="width:200px;"/>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Description aligned with text box width, without the link icon
    st.markdown(
        """
        <div style="max-width: 700px; margin: auto; color: white; font-size: 1.1em;">
            Experience the power of AI with our LLM based demo app! Efficiently identify emotions in texts through seven distinct emotions: joy, fear, disgust, guilt, shame, sadness, and anger.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Central content area with class to control width
    with st.container():
        st.markdown(
            '<div style="max-width: 700px; margin: auto;">', unsafe_allow_html=True
        )

        # Create a form for user input
        with st.form(key="emotion_form"):
            user_input = st.text_area(
                "Enter your text here:", placeholder="Insert text in English"
            )
            submit_button = st.form_submit_button(label="Analyze")

        if submit_button and user_input:
            with st.spinner("Analyzing text..."):
                try:
                    response = detect_emotion(
                        user_input, system_message, fine_tuned_model_id
                    )

                    # Get the emoji for the detected emotion
                    emoji = emotion_emojis.get(response.lower(), "🔍")

                    # Display result with consistent styling and label
                    st.markdown("### Emotion Detected:")
                    st.markdown(
                        f"<div style='background-color: #333333; padding: 10px; border-radius: 10px; color: white; font-size: 20px; text-align: center;'>{emoji} {response.capitalize()}</div>",
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        st.markdown("</div>", unsafe_allow_html=True)  # Close main-content div


if __name__ == "__main__":
    main()

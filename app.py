from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# Commented out the load_dotenv since we won't be using .env for API key
# load_dotenv()

# Function to get the response from the Gemini model
def get_gemini_response(input_prompt, image, api_key):
    # Configure API key from the user input
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Function to prepare image for API request
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_part = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_part
    else:
        raise FileNotFoundError("No File Uploaded")

# Streamlit app settings
st.set_page_config(page_title="GEMINI CALORIE APP")
st.header("Gemini Health App")

# API key input from user
api_key = st.text_input("Enter your Google API Key", type="password")

# File uploader for image input
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
image = ""

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

# Submit button for user to get the calorie info
submit = st.button("Tell me about the total calories")

# Input prompt for the model
input_prompt = """
You are an expert in nutrition where you need to see the food items from the image
and calculate the total calories. Also, provide the details of every food item with calorie intake 
in the format below:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
----
"""

# When the submit button is clicked
if submit:
    if not api_key:
        st.error("Please enter your Google API key.")
    else:
        try:
            # Setup the image for API request
            image_data = input_image_setup(uploaded_file)
            # Get the response from the Gemini API
            response = get_gemini_response(input_prompt, image_data, api_key)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

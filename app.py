import streamlit as st
import base64
from io import BytesIO
from PIL import Image
import os

from openai import OpenAI

# Load API key

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to encode image
def encode_image(image):
    buffer = BytesIO()
    image.save(buffer, format="png")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

# Streamlit UI
st.title("🍔 Food Calorie Estimator")

uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Analyze Food"):
        with st.spinner("Analyzing..."):
            base64_image = encode_image(image)

            prompt = """
            Analyze this food image and provide:
            - Food name
            - Estimated calories
            - Protein, carbs, fat
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{base64_image}"
                                             }
                            }
                        ]
                    }
                ]
            )

            result = response.choices[0].message.content
            st.subheader("🍽️ Result")
            st.write(result)

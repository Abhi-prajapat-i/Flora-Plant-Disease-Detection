import streamlit as st
from plant_and_crops_name import languages, crops_plant_name , prediction_class
from tensorflow.keras.preprocessing import image
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
from LLM import llm
from prompt_maker import get_prompt, build_chat_messages , MAX_HISTORY_MESSAGES
from report_maker import generate_recommendation_pdf

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import io
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def main():

    if "disease" not in st.session_state:
        st.session_state.disease = ""

    if "confidence" not in st.session_state:
        st.session_state.confidence = 0.0

    if "treatment_advice" not in st.session_state:
        st.session_state.treatment_advice = ""

    if "messages" not in st.session_state:
        st.session_state.messages = []

   

    # Page Configuration
   
    st.set_page_config(
        page_title="Flora AI Plant Disease Detection",
        page_icon="🌿",
        layout="wide"
    )



    # Global Styling 
   
    st.markdown(
        """
        <style>
        .main-header {
            background: linear-gradient(135deg, #2e7d32 0%, #66bb6a 100%);
            padding: 2rem 2.2rem;
            border-radius: 14px;
            color: white;
            margin-bottom: 1.5rem;
        }
        .main-header h1 {
            margin-bottom: 0.3rem;
            font-size: 2.1rem;
        }
        .main-header p {
            margin: 0;
            font-size: 1.02rem;
            opacity: 0.92;
        }
        .section-card {
            background-color: #ffffff;
            border: 1px solid #e3e8e3;
            border-radius: 12px;
            padding: 1.3rem 1.4rem;
            margin-bottom: 1rem;
        }
        .result-card {
            background-color: #f1f8f2;
            border: 1px solid #cfe8d1;
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 1rem;
        }
        .chat-row {
            display: flex;
            margin-bottom: 0.6rem;
        }
        .chat-row-user {
            justify-content: flex-end;
        }
        .chat-row-ai {
            justify-content: flex-start;
        }
        .chat-bubble-user {
            background-color: #e8f5e9;
            color: #1b1b1b;
            border-radius: 10px;
            padding: 0.6rem 0.9rem;
            max-width: 75%;
            text-align: right;
        }
        .chat-bubble-ai {
            background-color: #f5f5f5;
            color: #1b1b1b;
            border-radius: 10px;
            padding: 0.6rem 0.9rem;
            max-width: 75%;
            text-align: left;
        }
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
        }
        .app-footer {
            margin-top: 2.5rem;
            padding: 1rem 0 0.5rem 0;
            border-top: 1px solid #e3e8e3;
            text-align: center;
            color: #6b7a6b;
            font-size: 0.9rem;
        }
        .app-footer b {
            color: #2e7d32;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


   
    # Header
   
    st.markdown(
        """
        <div class="main-header">
            <h1> 🌿 Flora</h1>
            <h2>    Plant Disease Detection & Treatment Advisor</h2>
            <p>📷 Upload a plant leaf image to detect diseases and receive AI-powered treatment recommendations — fast, accurate, and easy to use.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

   

    # Sidebar
   
    with st.sidebar:

        st.header("⚙️ Settings")

        st.markdown("#### 🌱 Crop Selection")
        crop = st.selectbox(
            "Select Crop",
            crops_plant_name,
            label_visibility="collapsed",
        )

        st.markdown("---")

        st.markdown("#### 🌐 Language")
        language = st.selectbox(
            "Response Language",
            languages,
            label_visibility="collapsed",
        )

        st.markdown("---")

        st.markdown("#### 🤖 AI Recommendation")
        ai = st.checkbox(
            "Enable AI Treatment Recommendation",
            value=True,
        )

        st.markdown("---")

        st.info(
            "💡 **Tip:** Select the crop before uploading the image.\n\n"
            "The corresponding AI model will be used."
        )

        st.caption("🌾 Powered by Flora AI.")


    # Main Layout

    left, right = st.columns([1, 1], gap="large")

   
    # Upload Section
   
    with left:

        st.subheader("📤 Upload Leaf Image")

        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        st.caption("Accepted formats: JPG, JPEG, PNG. For best results, use a clear, well-lit close-up of the leaf.")

        image = st.file_uploader(
            "Choose a leaf image",
            type=["jpg", "jpeg", "png"],
        )

        if image is not None:
            image = Image.open(image)
            st.image(image, caption="🖼️ Uploaded Leaf Image", use_column_width=True)
            st.success("✅ Image uploaded successfully. Ready for prediction.")
        else:
            st.info("👆 No image uploaded yet. Please choose a leaf image to get started.")

        st.markdown('</div>', unsafe_allow_html=True)



    # Prediction Section
  
    def predection(image, model, classes_name):
        
        image = image.convert("RGB")
        image = image.resize((180, 180))

        image_array = np.array(image)
        img_array = np.expand_dims(image_array, axis=0)

        prediction = model.predict(img_array, verbose=0)

        predicted_class = classes_name[np.argmax(prediction[0])]
        confidence = float(np.max(prediction[0]) * 100)

        return predicted_class, confidence

    with right:

        st.subheader("🔍 Prediction")

        if image is None:

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.info("⏳ Upload an image on the left to begin diagnosis.")
            st.markdown('</div>', unsafe_allow_html=True)

        else:

            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            if st.button(
                "🔎 Predict Disease",
                type="primary",
            ):
                # select the model according to the user.
                with st.spinner("Loading model..."):
                    #potato plant.
                    if crop == "Potato":
                        model = keras.models.load_model("models/potato_model.keras")
                        predicted_class, confident = predection(image,model,prediction_class[crop])
                        st.session_state.disease = predicted_class
                        st.session_state.confidence = confident
                    #Tomato plant
                    if crop == "Tomato":
                        model = keras.models.load_model("models/tomato_model.keras")
                        predicted_class, confident = predection(image,model,prediction_class[crop])
                        st.session_state.disease = predicted_class
                        st.session_state.confidence = confident

                    st.session_state.treatment_advice = ""
                    st.session_state.messages = []

                st.success("✅ Prediction Complete")

            if st.session_state.disease:

                st.markdown('<div class="result-card">', unsafe_allow_html=True)

                st.metric("🌱 Crop", crop)
        
                st.metric("🦠 Disease", st.session_state.disease)

                st.markdown("**🎯 Confidence Score**")
                st.progress(min(int(st.session_state.confidence), 100))
                st.caption(f"{st.session_state.confidence:.2f}% confidence")

                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Generate the AI Recommendation.
    if ai:

        st.subheader("🌾 AI Treatment Recommendation")

        if st.button(
            "✨ Generate AI Recommendation",
        ):
            if st.session_state.disease :
                with st.spinner("Generating recommendation..."):
                    prompt = get_prompt(crop, language, st.session_state.disease)
                    response = llm.invoke(prompt)
                    st.session_state.treatment_advice = response.content
            else:
                st.warning(
                        "⚠️ Please upload a leaf image and predict the disease before requesting AI recommendations."
                )

       
       # Generate recommendation report.
        if st.session_state.treatment_advice:

            with st.expander(
                "🌾 AI Treatment Advice",
                expanded=True,
            ):

                st.markdown(st.session_state.treatment_advice)

            pdf_buffer = generate_recommendation_pdf(
                crop=crop,
                disease=st.session_state.disease,
                confidence=st.session_state.confidence,
                treatment_advice=st.session_state.treatment_advice,
            )

            st.download_button(
                label="📄 Download Report as PDF",
                data=pdf_buffer,
                file_name=f"{crop}_{st.session_state.disease}_treatment_report.pdf",
                mime="application/pdf",
            )

    if st.session_state.disease :
        
        st.markdown("---")
        st.subheader("💬 Discuss This Recommendation")

        discussion = st.radio(
            "Do you want to discuss this recommendation?",
            ["No", "Yes"],
            horizontal=True
        )

        if discussion == "Yes":

            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            # Display previous messages
            if not st.session_state.messages:
                st.caption("Ask a question about the diagnosis or treatment below.")

            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="chat-row chat-row-user"><div class="chat-bubble-user">🧑 <b>You:</b> {msg["content"]}</div></div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="chat-row chat-row-ai"><div class="chat-bubble-ai">🤖 <b>AI:</b> {msg["content"]}</div></div>',
                        unsafe_allow_html=True,
                    )

            with st.form("chat_form", clear_on_submit=True):

                col_input, col_btn = st.columns([4, 1])
                with col_input:
                    question = st.text_input("Ask a question", label_visibility="collapsed")
                with col_btn:
                    submitted = st.form_submit_button("Send 📨")

            st.markdown('</div>', unsafe_allow_html=True)

            if submitted and question.strip():

                # Build a memory aware message list: system context
                chat_messages = build_chat_messages(
                    crop=crop,
                    disease=st.session_state.disease,
                    treatment_advice=st.session_state.treatment_advice,
                    history=st.session_state.messages,
                    question=question,
                )

                response = llm.invoke(chat_messages).content

                st.session_state.messages.append(
                    {"role": "user", "content": question}
                )

                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

                st.session_state.messages = st.session_state.messages[-MAX_HISTORY_MESSAGES:]

                st.experimental_rerun()

    # -------------------------
    # Footer
    # -------------------------

    st.markdown(
        """
        <div class="app-footer">
            🌿 Developed by <b>Abhishek Kumar</b> — AI Learner.
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
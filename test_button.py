import streamlit as st

st.title("Button Test")

if st.button("Test Button"):
    st.write("Button clicked!")
    st.success("Button is working!")
    
story_prompt = st.text_area("Enter text:")

if st.button("Test BEGIN STORY", disabled=not story_prompt.strip()):
    st.write(f"Story prompt: {story_prompt}")
    st.success("BEGIN STORY button logic is working!")
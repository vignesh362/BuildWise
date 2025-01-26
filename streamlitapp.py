import streamlit as st
from PIL import Image
from streamlit_chat import message
from query_answering import get_answer
from invokeWord import invoke_streamlit_app

# Set page configuration
st.set_page_config(page_title="Chatbot System", layout="wide")
# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

# Sidebar customization
with st.sidebar:
    st.title("All For One")
    theme = st.radio("Choose Theme", ["Light", "Dark"])
    avatar = st.text_input("Set Chatbot Name", "AI Assistant")

# Chat container
chat_container = st.container()

# Message input
with st.form(key="message_form"):
    user_input = st.text_input("Type your message:", key="input")
    submit_button = st.form_submit_button("Send")

    if submit_button and user_input:
        # Store user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get AI response
        try:
            response = get_answer(user_input)

            # Display images
            image_one = Image.open("Building Floor Plan Analysis.png")
            image_two = Image.open("Building Safety Systems.png")
            st.image([image_one, image_two])

            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error processing response: {str(e)}")

# Display chat history
with chat_container:
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            message(msg["content"], is_user=True, key=f"msg_{i}")
        else:
            message(msg["content"], is_user=False, key=f"msg_{i}")

# Generate Report button
if st.button("Generate Report"):
    if st.session_state.messages:
        # Use the latest assistant response and an image file for the report
        last_response = st.session_state.messages[-1]["content"]
        try:
            a="""Based on the provided context, here are the buildings mentioned along with their layouts: 4 Penn Plaza Location: Block 781, Lot Z Permitted uses: Restaurant, offices, dressing rooms, locker rooms, storage, forum (auditor), basketball, boxing, tennis, dance, loading area, accessory parking, and mechanical equipment rooms. Floor space: 145 feet 9 inches Weight classification: 1B Seating capacity: 4-14 people in exhibition areas 138 Spring Street Location: C 1-58 zoning district Permitted uses: Commercial purposes, including storage, office, and showroom space, cellar, and showrooms. Height: 7 stories Commercial classification 4 Penn Plaza Block TOL Lot 2 (new building in Manhattan) Location: Bounded by specific coordinates, including a starting point at 7th Avenue and West 131st Street Permitted uses: Commercial venue with various facilities such as restaurants, offices, dressing rooms, and storage areas. Height: 111 feet and 5 stories Mets - altered - building Location: Classified under the city's zoning regulations (c6-6.5) Permitted uses: Public building with various facilities such as screening rooms, elevators, mechanical rooms, storage, and offices. Height: 8 to 12 feet and from 16 to 20 feet Total stories: 41 Note that the layouts of these buildings are not explicitly mentioned in the provided context. However, based on the permitted uses and other details, it can be inferred that they have various facilities such as offices, storage areas, dressing rooms, and mechanical equipment rooms."""
            invoke_streamlit_app(a, "Building Safety Systems.png")
            st.success("Report generation invoked successfully!")
        except Exception as e:
            st.error(f"Error invoking report generation: {str(e)}")
    else:
        st.warning("No messages to generate a report from.")

import streamlit as st

def render_contact():
    """Renders the Contact Us page."""
    st.title("Contact Us")
    
    st.markdown("""
    This Bioinformatics Toolkit was developed by:
    
    ### Mohammad Yusuf
    **Bioscience Student at Jamia Millia Islamia & AI Trainer**
    
    ---
    
    *   **LinkedIn:** [[Insert LinkedIn URL]](#)
    *   **Email:** [[Insert Email Address]](mailto:your.email@example.com)
    
    ---
    
    Feel free to reach out for collaborations, feedback, or any inquiries regarding this computational biology toolkit.
    """)

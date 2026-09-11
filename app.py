import streamlit as st
from tools.gc_content import render_gc_calculator
from tools.orf_finder import render_orf_finder
from tools.primer_design import render_primer_design
from tools.contact import render_contact

def main():
    st.set_page_config(page_title="Bioinformatics Toolkit", page_icon="🧬", layout="wide")

    st.sidebar.title("🧬 Bioinformatics Toolkit")
    st.sidebar.markdown("Navigate through our tools below:")

    page = st.sidebar.radio("Select a Tool:", [
        "ORF Finder", 
        "GC Content Calculator", 
        "Primer Design Tool", 
        "Contact Us"
    ])

    if page == "ORF Finder":
        render_orf_finder()
    elif page == "GC Content Calculator":
        render_gc_calculator()
    elif page == "Primer Design Tool":
        render_primer_design()
    elif page == "Contact Us":
        render_contact()

if __name__ == "__main__":
    main()

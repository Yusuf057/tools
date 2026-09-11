import streamlit as st
import re

def calculate_gc(sequence):
    """Calculates the GC percentage of a DNA/RNA sequence."""
    seq = sequence.upper()
    g_count = seq.count('G')
    c_count = seq.count('C')
    a_count = seq.count('A')
    t_count = seq.count('T')
    
    total = g_count + c_count + a_count + t_count
    if total == 0:
        return 0.0
    return ((g_count + c_count) / total) * 100

def render_gc_calculator():
    """Renders the GC Content Calculator UI."""
    st.title("GC Content Calculator")
    
    st.markdown("""
    ### Educational Context
    The **GC content** (Guanine-Cytosine content) is the percentage of nitrogenous bases in a DNA or RNA molecule that are either guanine (G) or cytosine (C).
    
    **Formula:** 
    `GC% = (G + C) / (A + T + G + C) * 100`
    
    GC pairs are bound by three hydrogen bonds, while AT pairs are bound by two. Therefore, higher GC content implies a higher melting temperature and more stability in the DNA structure.
    """)
    
    st.divider()
    
    st.subheader("Input Sequence")
    sequence = st.text_area("Enter your raw DNA sequence or FASTA format:", height=150)
    
    if st.button("Calculate GC Content", type="primary"):
        if sequence:
            # Clean sequence (remove fasta header and newlines/spaces)
            if sequence.startswith(">"):
                sequence = "\n".join(sequence.split("\n")[1:])
            
            # Keep only standard bases for GC calculation
            clean_seq = re.sub(r'[^ATGCUatgcu]', '', sequence)
            
            if len(clean_seq) == 0:
                st.warning("No valid DNA/RNA sequence found.")
            else:
                gc_percentage = calculate_gc(clean_seq)
                st.success(f"### Calculated GC Content: **{gc_percentage:.2f}%**")
                
                # Visual progress bar for GC content
                st.progress(gc_percentage / 100.0)
                
                st.info(f"Total bases analyzed: {len(clean_seq)} bp")
        else:
            st.error("Please enter a sequence.")

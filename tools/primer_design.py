import streamlit as st
import re

def reverse_complement(seq):
    """Returns the reverse complement of a DNA sequence."""
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return "".join(complement.get(base, base) for base in reversed(seq))

def gc_content(seq):
    """Calculates GC content percentage."""
    g = seq.count('G')
    c = seq.count('C')
    return ((g + c) / len(seq)) * 100 if len(seq) > 0 else 0

def calculate_tm(seq):
    """Calculates Melting Temperature (Tm) based on sequence length."""
    a = seq.count('A')
    t = seq.count('T')
    g = seq.count('G')
    c = seq.count('C')
    
    length = len(seq)
    
    if length < 14:
        # Wallace rule
        return 2 * (a + t) + 4 * (g + c)
    elif length > 0:
        # Simplified salt-adjusted formula
        # Basic estimation for educational purposes
        return 64.9 + 41 * (g + c - 16.4) / length
    return 0

def find_primers(sequence, length=20, min_gc=40, max_gc=60):
    """Finds basic forward and reverse primers."""
    fwd_primer = None
    rev_primer = None
    
    # Forward primer scanning from the start (5' end)
    for i in range(len(sequence) - length):
        candidate = sequence[i:i+length]
        gc = gc_content(candidate)
        
        # Check GC clamp (ends with G or C) - basic check to ensure strong 3' binding
        if candidate[-1] in ['G', 'C'] and candidate[-2:] not in ['GG', 'CC', 'GC', 'CG']: 
             if min_gc <= gc <= max_gc:
                 fwd_primer = candidate
                 break
                 
    if not fwd_primer:
        fwd_primer = sequence[:length] # Fallback if no ideal primer found
        
    # Reverse primer scanning from the end (3' end of original, so 5' of reverse complement)
    rev_seq = reverse_complement(sequence)
    for i in range(len(rev_seq) - length):
        candidate = rev_seq[i:i+length]
        gc = gc_content(candidate)
        
        if candidate[-1] in ['G', 'C'] and candidate[-2:] not in ['GG', 'CC', 'GC', 'CG']:
            if min_gc <= gc <= max_gc:
                rev_primer = candidate
                break
                
    if not rev_primer:
        rev_primer = rev_seq[:length] # Fallback if no ideal primer found
        
    return fwd_primer, rev_primer

def render_primer_design():
    """Renders the Primer Design Tool UI."""
    st.title("Primer Design Tool")
    
    st.markdown("""
    ### Educational Context
    **Primers** are short, single-stranded DNA sequences used in PCR (Polymerase Chain Reaction) to initiate DNA replication by DNA polymerase.
    
    **Design Rules Implemented in this Tool:**
    *   **Length:** Typically 18-24 base pairs (bp). Long enough for adequate specificity and short enough for primers to bind easily.
    *   **GC Content:** Optimal range is 40-60%.
    *   **3' GC Clamp:** Having a G or C at the 3' end ensures a strong bond to the template, but avoiding long runs of G/C prevents non-specific binding.
    
    **Melting Temperature (Tm) Calculation:**
    *   For short sequences (under 14 bases), we use the **Wallace rule**: `Tm = 2(A+T) + 4(G+C)`
    *   For longer sequences (14+ bases), we use a basic **salt-adjusted formula**: `Tm = 64.9 + 41*(G+C-16.4)/(Length)`
    """)
    
    st.divider()
    
    st.subheader("Input Target Sequence")
    sequence = st.text_area("Enter your target DNA sequence:", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        length_opt = st.slider("Target Primer Length (bp)", 18, 24, 20)
    with col2:
        st.write("Target GC Content: 40% - 60%")
    
    if st.button("Generate Primers", type="primary"):
        if sequence:
            if sequence.startswith(">"):
                sequence = "\n".join(sequence.split("\n")[1:])
            
            clean_seq = re.sub(r'[^ATGCatgc]', '', sequence).upper()
            
            if len(clean_seq) < 50:
                st.warning("Please provide a longer sequence (at least 50 bp) for effective primer design.")
            else:
                fwd, rev = find_primers(clean_seq, length=length_opt)
                
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    st.markdown("### Forward Primer (5' -> 3')")
                    st.info(f"**`{fwd}`**")
                    fwd_gc = gc_content(fwd)
                    fwd_tm = calculate_tm(fwd)
                    st.write(f"**Length:** {len(fwd)} bp")
                    st.write(f"**GC Content:** {fwd_gc:.1f}%")
                    st.write(f"**Tm:** {fwd_tm:.1f} °C")
                    
                with res_col2:
                    st.markdown("### Reverse Primer (5' -> 3')")
                    st.info(f"**`{rev}`**")
                    rev_gc = gc_content(rev)
                    rev_tm = calculate_tm(rev)
                    st.write(f"**Length:** {len(rev)} bp")
                    st.write(f"**GC Content:** {rev_gc:.1f}%")
                    st.write(f"**Tm:** {rev_tm:.1f} °C")
                    
        else:
            st.error("Please enter a sequence.")

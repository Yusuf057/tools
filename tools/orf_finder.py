import streamlit as st
import re

# Standard genetic code dictionary
CODON_TABLE = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',                 
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
    'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
}

def reverse_complement(seq):
    """Returns the reverse complement of a DNA sequence."""
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return "".join(complement.get(base, base) for base in reversed(seq))

def find_orfs(sequence, min_len=30):
    """Finds all ORFs in 6 reading frames."""
    seq_len = len(sequence)
    orfs = []
    
    # Check all 3 forward frames
    for frame in range(3):
        for i in range(frame, seq_len - 2, 3):
            codon = sequence[i:i+3]
            if codon == 'ATG':
                # Find the first stop codon in this frame
                for j in range(i + 3, seq_len - 2, 3):
                    stop_codon = sequence[j:j+3]
                    if stop_codon in ['TAA', 'TAG', 'TGA']:
                        orf_seq = sequence[i:j+3]
                        if len(orf_seq) >= min_len:
                            orfs.append({'frame': f"+{frame+1}", 'start': i, 'end': j+3, 'seq': orf_seq})
                        break
                        
    # Check all 3 reverse frames
    rev_seq = reverse_complement(sequence)
    for frame in range(3):
        for i in range(frame, seq_len - 2, 3):
            codon = rev_seq[i:i+3]
            if codon == 'ATG':
                for j in range(i + 3, seq_len - 2, 3):
                    stop_codon = rev_seq[j:j+3]
                    if stop_codon in ['TAA', 'TAG', 'TGA']:
                        orf_seq = rev_seq[i:j+3]
                        if len(orf_seq) >= min_len:
                            # Adjust coordinates for the original sequence orientation
                            actual_start = seq_len - (j+3)
                            actual_end = seq_len - i
                            orfs.append({'frame': f"-{frame+1}", 'start': actual_start, 'end': actual_end, 'seq': orf_seq})
                        break
                        
    # Sort by sequence length descending
    orfs.sort(key=lambda x: len(x['seq']), reverse=True)
    return orfs

def translate(seq):
    """Translates a DNA sequence to a protein sequence."""
    protein = ""
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i:i+3]
        protein += CODON_TABLE.get(codon, 'X')
    return protein

def render_orf_finder():
    """Renders the ORF Finder UI."""
    st.title("Open Reading Frame (ORF) Finder")
    
    st.markdown("""
    ### Educational Context
    An **Open Reading Frame (ORF)** is a continuous stretch of codons that begins with a start codon (usually **ATG**) and ends at a stop codon (**TAA**, **TAG**, or **TGA**).
    
    DNA is double-stranded, and the sequence can be read in sets of three bases (codons) starting from the first, second, or third base. This gives **3 forward reading frames**. Because the other strand runs in the opposite direction, there are also **3 reverse reading frames**, making a total of **6 possible reading frames**.
    
    This tool scans all 6 frames to identify potential protein-coding regions and translates them into amino acid sequences.
    """)
    
    st.divider()
    
    st.subheader("Input Sequence")
    sequence = st.text_area("Enter your raw DNA sequence or FASTA format:", height=150)
    
    min_len = st.number_input("Minimum ORF length (bp):", min_value=15, value=30, step=3)
    
    if st.button("Find ORFs", type="primary"):
        if sequence:
            if sequence.startswith(">"):
                sequence = "\n".join(sequence.split("\n")[1:])
            
            clean_seq = re.sub(r'[^ATGCatgc]', '', sequence).upper()
            
            if len(clean_seq) < 3:
                st.warning("Sequence too short to contain an ORF.")
            else:
                orfs = find_orfs(clean_seq, min_len=min_len)
                if not orfs:
                    st.info(f"No ORFs found longer than {min_len} bp in the provided sequence.")
                else:
                    st.success(f"Found {len(orfs)} ORFs longer than {min_len} bp.")
                    
                    for idx, orf in enumerate(orfs):
                        with st.expander(f"ORF {idx+1} | Length: {len(orf['seq'])} bp | Frame: {orf['frame']} | Coordinates: {orf['start']} - {orf['end']}"):
                            protein = translate(orf['seq'])
                            st.markdown(f"**DNA Sequence:**\n```text\n{orf['seq']}\n```")
                            st.markdown(f"**Protein Sequence:**\n```text\n{protein}\n```")
        else:
            st.error("Please enter a sequence.")

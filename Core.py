from Bio import AlignIO

"""
Program: ConservFinder for .maf files.
Language: Python 
Description: 
Author: Yehor Tertyshnyk 
Email: egor.tertyshnyk@gmail.com
Github: --TBS--
Description: This program takes your .maf file and output conserved sequences as well as their genomic range; relative to beginnning of alignment (1) and relative to position on chromosome (2). 
"""

# Define the MAF file location and the species to include
maf_file ='/Users/egortertyshnyk/Desktop/Simakov_Group/Conserved_regions/MOLLUSC_Chr10_small.maf' 
include_species = ["Octopusvulgaris6645.OX597823.1", "Octopusbimaculoides37653.NC_068990.1", "Octopussinensis2607531.NC_043005.1"]
Bp_Threshold = 70.0 # for 70%

# Parse the MAF file
for multiple_alignment in AlignIO.parse(maf_file, "maf"):
    print("\n--------------------------------New Alignment Block--------------------------------")  # It's just to show that all ranges down are part of same ali, maybe we don't need it.      
    # Lists to hold sequence strings and record IDs
    sequences = []
    records = []
    Chrom_Position = [] 
    
    # Filter alignments by included species and collect their sequences and IDs
    for record in multiple_alignment:
        if record.id in include_species:
            sequences.append(str(record.seq).upper())  # Ensure case consistency
            records.append(record.id)  
            Chrom_Position.append(record.annotations['start'])

    sequence_length = len(sequences[0])
    num_sequences = len(sequences)
 

    if not sequences:  # Skip if no sequences match the filter
        continue

    # Find matching indices across all sequences
    matching_indices = [] 
    for i in range(len(sequences[0])):
        if all(seq[i].upper() == sequences[0][i].upper() for seq in sequences):
 #make upper 
            matching_indices.append(i)

    # Initialize variables for finding ranges longer than 5
    range_indices = []
    start = end = matching_indices[0]
    for index in matching_indices[1:] + [None]:  # Add None to handle the last range effectively
        if index is not None and index == end + 1:
                end = index
        else:
            if end - start >= 4:  # Ensure the range includes more than 5 matching bases
                    range_indices.append((start, end))
            if index is not None:
                    start = end = index
  
    for start, end in range_indices:  
        conserved_sequence = sequences[0][start:end+1] # This part was tricky, just remmeber sequence[0] is for choosing the first seq and then we are choosing the range that we need. 
        print(f"Conserved sequence: {conserved_sequence} Relative range: {start}-{end}") # maybe relative range is not the best name. 
        for i, record_id in enumerate(records): # 'records' are just names of species, enumerate gives pair of index and value asigned to this index. Like (0, 'apple').
            genomic_start = Chrom_Position[i] + start + 1 
            genomic_end = Chrom_Position[i] + end + 1
            print(f"{record_id} {genomic_start} {genomic_end}")
        print()  
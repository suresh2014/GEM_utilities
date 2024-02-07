#!/usr/bin/python
'''
To extract  number of metabolites, Genes and reactions from Multiple reconstructed draft models
Input files are xml files 
output willbe csv file
'''
from cameo import load_model
import os
import warnings
import argparse

def extract_info(model):
    genes = len(model.genes)
    metabolites = len(model.metabolites)
    reactions = len(model.reactions)

    return genes, reactions, metabolites

def process_folder(folder_path):
    data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder_path, filename)
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    model = load_model(file_path)
                genes, reactions, metabolites = extract_info(model)
                data.append((filename, genes, reactions, metabolites))
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    return data

def write_tsv(data, output_file):
    with open(output_file, 'w') as f:
        # Write header
        f.write("File\tGenes\tReactions\tMetabolites\n")
        
        # Write data
        for entry in data:
            f.write("\t".join(map(str, entry)) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process XML files and generate a table.")
    parser.add_argument("-f", "--folder", required=True, help="Path to the folder containing XML files")
    parser.add_argument("-o", "--output", required=True, help="Output file name")

    args = parser.parse_args()
    
    folder_path = args.folder
    output_file = args.output

    data = process_folder(folder_path)
    write_tsv(data, output_file)


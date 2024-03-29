#libraries used in this code
from rcsbsearchapi.const import CHEMICAL_ATTRIBUTE_SEARCH_SERVICE, STRUCTURE_ATTRIBUTE_SEARCH_SERVICE
from rcsbsearchapi.search import AttributeQuery, TextQuery
from Bio.PDB import PDBList
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
import os 
import pandas as pd

#the first part of the code used to simulate the search process

q1 = TextQuery("transcription factor")

q2 = AttributeQuery("exptl.method", "exact_match", "X-RAY DIFFRACTION",
                    STRUCTURE_ATTRIBUTE_SEARCH_SERVICE
                    )
q3 = AttributeQuery("rcsb_entry_info.resolution_combined", "less_or_equal", 3.0,
                    STRUCTURE_ATTRIBUTE_SEARCH_SERVICE
                    )

q4 = AttributeQuery("chem_comp.name", "contains_phrase", "sodium",
                    CHEMICAL_ATTRIBUTE_SEARCH_SERVICE 
                    )

q5 = AttributeQuery("rcsb_entity_source_organism.taxonomy_lineage.name", "exact_match", "Homo sapiens",
                    STRUCTURE_ATTRIBUTE_SEARCH_SERVICE
                    )

query = (q1 & q2 & q3 & q4) - q5

query_result = list(query())

 print ("The query matches "+ str(len(query_result))+" structure")


#second part of the code used to download the mmCIF files of each protein

pdb_list = PDBList()  
# for num,each_id in enumerate(query_result):
#     if num >= 2288:
#         print(num,each_id)
#       pdb_filename= pdb_list.retrieve_pdb_file(each_id, pdir="data", file_format="mmCif")
   

         
   
#third part of the code is going to go throw each structure's file and extract the data we need

data_needed = [
    "_entry.id", "_struct.title","_struct.pdbx_descriptor",   
    "_entity_src_gen.pdbx_gene_src_scientific_name",
    "_entity_src_gen.pdbx_host_org_scientific_name",
    "_exptl.method", "_refine.ls_d_res_high",
    "_citation.title", "_citation.pdbx_database_id_DOI",
    "_chem_comp.name", "_struct_keywords.text" 
]

my_list = [os.path.join("data", file) for file in os.listdir("data") if file.endswith(".cif")]

data = {
    key[1:]: [] for key in data_needed
}

for file_path in my_list:
    pdb_info = MMCIF2Dict(file_path)
    for key in data_needed:
        if key in pdb_info:
            data[key[1:]].append(pdb_info[key])
        else:
            data[key[1:]].append("N/A")

#last part of the code takes all data the code collected and put in excel sheet has the name of "output"
    
df = pd.DataFrame(data)   

excel_file_path = 'output.xlsx'

df.to_excel(excel_file_path, index=False)

print(excel_file_path)

#improvements can be done to the code:
#  1-make an new input to take the user search criteria
#  2- make the user choose number of downloaded
#  3-make the user input the path where he wants the cif files to be downloaded
#  4-make the user choose the data needed from the cif file 
#  5-make a the user choose the excel file name and its location

#if you would like to know more about the code and how to customize your RCSB search, contact:marwanosama3002@gmail.com
#©2024 Marwan Osama.All rights reserved
#!/bin/bash

# The RDF quiet program waits for an input of the name of the xyz file (without its extension) 
#and produces an output file called output.csv
echo "Running example cluster #01"

echo "001-klmc" | /home/uccatka/software/RDF/RDF_Quiet #This assumes the RDF_Quiet program is in the folder above this one, as it is in GitHub
mv output.csv output_example_cluster01.csv #Renames the output to a sensible name

echo "Running example cluster #02"

echo "example_cluster02" | /home/uccatka/software/RDF/RDF_Quiet 
mv output.csv output_example_cluster02.csv 



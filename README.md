# FAS (a tool for Fragments association studies)

FAS method for identification of molecular Fragments associated with a particular toxicity class.
Requirements:

1) Plink software (https://www.cog-genomics.org/plink2)

2) Openbabel (http://openbabel.org/wiki/Main_Page)

3) Java

The dataset "dataset_MUTA_KNN" is a test set provided here. 

Commands:

# define a root for the dataset
ROOT="dataset_MUTA_KNN"

# from the dataset file, extract 3 tab-separated columns: SMILES, molecule IDENTIFIER e toxicity class (i.e. NON-Mutagen, Mutagen)
perl -ane 'print "$F[2]\t$F[1]\t$F[4]\n"' < ${ROOT}.txt | sed '1d' > ${ROOT}.smi

# convert SMILES file to SDF
babel -ismi ${ROOT}.smi -osdf ${ROOT}.sdf

# extract from SDF file a list of fragments identified in each molecule
java -jar PubChemFragmenter.jar ${ROOT}.sdf > ${ROOT}.pcfrags

# prepare input files for association study
python preprocess_pchem_quantitative.py $ROOT

# perform the association study
plink --file ${ROOT} --assoc --no-parents --allow-no-sex --no-fid --out ${ROOT} --adjust

The plink tools creates a file with extension ".assoc", where for each fragment ID (second column of the output) the frequency in both mutagen molecules (column "F_A") and non mutagen molecules (columns "F_U") is reported; column "P" is the pvalue of the chi-square test.

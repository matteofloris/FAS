# FAS (a tool for Fragments association studies)

FAS method for identification of molecular Fragments associated with a particular toxicity class.
Requirements:
1) Plink software (https://www.cog-genomics.org/plink2)
2) Openbabel (http://openbabel.org/wiki/Main_Page)
3) Java

The dataset "dataset_MUTA_KNN" is a test set provided here.

Commands:

ROOT="dataset_MUTA_KNN"

perl -ane 'print "$F[2]\t$F[1]\t$F[4]\n"' < ${ROOT}.txt | sed '1d' > ${ROOT}.smi

babel -ismi ${ROOT}.smi -osdf ${ROOT}.sdf

java -jar PubChemFragmenter.jar ${ROOT}.sdf > ${ROOT}.pcfrags

python preprocess_pchem_quantitative.py $ROOT

plink --file ${ROOT} --assoc --no-parents --allow-no-sex --no-fid --out ${ROOT} --adjust

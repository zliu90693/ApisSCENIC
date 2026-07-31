```bash
conda activate create_cistarget_databases # see ../.env
cd /home/liuzhiyu/Projects/neo_caste/ApisSCENIC/01_create_cistarget_db
pwd # ...01_create_cistarget_db
```

```bash
wget https://resources.aertslab.org/cistarget/motif_collections/v10nr_clust_public/v10nr_clust_public.zip
unzip v10nr_clust_public.zip
rm v10nr_clust_public.zip
```
Link the homologous genes of bees and fruit flies obtained through OrthoFinder in a previous project to this project.
```bash
ln -s /home/liuzhiyu/Projects/neo_caste/Find_Ortholog/primary_transcripts/OrthoFinder/Results_Jun15/Orthologues/Orthologues_Drosophila_melanogaster .
ls Orthologues_Drosophila_melanogaster 
# Drosophila_melanogaster__v__Aedes_aegypti.tsv      Drosophila_melanogaster__v__Apis_mellifera.tsv     Drosophila_melanogaster__v__Camponotus_floridanus.tsv  Drosophila_melanogaster__v__Lasioglossum_albipes.tsv
# Drosophila_melanogaster__v__Anopheles_gambiae.tsv  Drosophila_melanogaster__v__Bombus_terrestris.tsv  Drosophila_melanogaster__v__Ceratina_calcarata.tsv     Drosophila_melanogaster__v__Lasioglossum_zephyrus.tsv
# Drosophila_melanogaster__v__Apis_cerana.tsv        Drosophila_melanogaster__v__Bombyx_mori.tsv        Drosophila_melanogaster__v__Harpegnathos_saltator.tsv  Drosophila_melanogaster__v__Monomorium_pharaonis.tsv
```
get annotation data of bees and fruit flies:
```bash
mkdir -p gtf
cd gtf
wget https://ftp.ensemblgenomes.ebi.ac.uk/pub/metazoa/current/gtf/apis_mellifera/Apis_mellifera.Amel_HAv3.1.63.gtf.gz -O Apis_mellifera.gtf.gz
gunzip Apis_mellifera.gtf.gz
wget https://ftp.ensemblgenomes.ebi.ac.uk/pub/metazoa/current/gtf/drosophila_melanogaster/Drosophila_melanogaster.BDGP6.54.63.gtf.gz -O Drosophila_melanogaster.gtf.gz
gunzip Drosophila_melanogaster.gtf.gz
```
transter gtf to tsv format:
```bash
# pip install gppy
gppy txinfo -g Drosophila_melanogaster.gtf > Drosophila_melanogaster.tsv
gppy txinfo -g Apis_mellifera.gtf > Apis_mellifera.tsv
```
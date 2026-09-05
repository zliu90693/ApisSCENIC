```bash
conda activate create_cistarget_databases # see ../../.env
cd /home/liuzhiyu/Projects/neo_caste/ApisSCENIC/02_Apis_cerana/01_create_cistarget_db
pwd # ...01_create_cistarget_db
```
Link the v10nr_clust_public data downloaded in 01_Apis_mellifera/01_create_cistarget_db
```bash
ln -s /home/liuzhiyu/Projects/neo_caste/ApisSCENIC/01_Apis_mellifera/01_create_cistarget_db/v10nr_clust_public .
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
ln -sf /home/liuzhiyu/Projects/neo_caste/ApisSCENIC/01_Apis_mellifera/01_create_cistarget_db/gtf/Drosophila_melanogaster.gtf ./gtf/
ln -sf /home/liuzhiyu/Projects/neo_caste/ApisSCENIC/01_Apis_mellifera/01_create_cistarget_db/gtf/Drosophila_melanogaster.tsv ./gtf/
```
```bash
# ncbi中，东方蜜蜂的GTF格式与ensembl严重不符，需要手动校正，见https://github.com/zliu90693/fastq2matrix/blob/master/Acer/ref-inspection.ipynb，因此本次使用事先经过手动校准的东方蜜蜂gtf
ln -sf /home/liuzhiyu/Projects/neo_caste/fastq2matrix/Acer/ref/GCF_029169275.1_fixed.filtered.gtf ./gtf/Apis_cerana.gtf
gppy txinfo -g ./gtf/Apis_cerana.gtf > ./gtf/Apis_cerana.tsv
```

get gene_id & gene_name relationship of fruit fly TF-motif tbl generated in 01_Apis_mellifera/01_create_cistarget_db/02_determine_bee_tbl.py:
```bash
ln -s /home/liuzhiyu/Projects/neo_caste/ApisSCENIC/01_Apis_mellifera/01_create_cistarget_db/metadata/Dmel_gname_gid.tsv ./metadata
```
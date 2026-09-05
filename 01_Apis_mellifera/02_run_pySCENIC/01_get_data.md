```bash
conda activate create_cistarget_databases
work_dir="/home/liuzhiyu/Projects/neo_caste/ApisSCENIC/01_Apis_mellifera"
cd "${work_dir}/02_run_pySCENIC"
mkdir -p "./feather"
ln -s "${work_dir}/01_create_cistarget_db/feather/V10nr_clust_tbl-cb-inter_Amel.motifs_vs_regions.scores.feather" "${work_dir}/02_run_pySCENIC/feather/V10nr_clust_tbl-cb-inter_Amel.motifs_vs_regions.scores.feather" 

ln -s "${work_dir}/01_create_cistarget_db/feather/V10nr_clust_tbl-cb-inter_Amel.regions_vs_motifs.rankings.feather" "${work_dir}/02_run_pySCENIC/feather/V10nr_clust_tbl-cb-inter_Amel.regions_vs_motifs.rankings.feather" 

ln -s "${work_dir}/01_create_cistarget_db/feather/V10nr_clust_tbl-cb-inter_Amel.regions_vs_motifs.scores.feather" "${work_dir}/02_run_pySCENIC/feather/V10nr_clust_tbl-cb-inter_Amel.regions_vs_motifs.scores.feather" 
```
Because the glibc library version required by pyscenic (executable) is higher than the current system version, aertslab-pyscenic-scanpy-0.12.1-1.9.1.sif will be used in this test.
```bash
mkdir -p "./tools"
ln -sf "/home/liuzhiyu/Projects/neo_caste/ApisSCENIC/.reference/data_from_LZU/suppliment/aertslab-pyscenic-scanpy-0.12.1-1.9.1.sif" "./tools/aertslab-pyscenic-scanpy-0.12.1-1.9.1.sif"

apptainer exec ./tools/aertslab-pyscenic-scanpy-0.12.1-1.9.1.sif pyscenic grn -h
```
Get drosophila melanogaster TF list for pyscenic grn:
```bash
mkdir -p "./metadata"
wget -O "./metadata/allTFs_dmel.txt" "https://resources.aertslab.org/cistarget/tf_lists/allTFs_dmel.txt"
```
Obtain the gene_name-gene_id mapping file to retrieve the gene_id corresponding to the TF name in allTFs_dmel.txt that does not appear in the GTF.
```bash
wget -O "./metadata/fbgn_annotation_ID_fb_2026_02.tsv.gz" "https://s3ftp.flybase.org/releases/current/precomputed_files/genes/fbgn_annotation_ID_fb_2026_02.tsv.gz"
wget -O "./metadata/gene_map_table_fb_2026_02.tsv.gz" "https://s3ftp.flybase.org/releases/current/precomputed_files/genes/gene_map_table_fb_2026_02.tsv.gz"

gunzip "./metadata/fbgn_annotation_ID_fb_2026_02.tsv.gz"
gunzip "./metadata/gene_map_table_fb_2026_02.tsv.gz"
```

Link the homologous genes of bees and fruit flies obtained through OrthoFinder in a previous project to this project.
```bash
ln -s /home/liuzhiyu/Projects/neo_caste/Find_Ortholog/primary_transcripts/OrthoFinder/Results_Jun15/Orthologues/Orthologues_Drosophila_melanogaster .
```


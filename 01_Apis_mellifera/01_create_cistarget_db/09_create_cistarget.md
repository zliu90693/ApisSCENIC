```bash
cd /home/liuzhiyu/Projects/neo_caste/ApisSCENIC/01_Apis_mellifera/01_create_cistarget_db
conda activate create_cistarget_databases
create_cistarget_databases_dir='../../4/create_cisTarget_databases'
${create_cistarget_databases_dir}/create_cistarget_motif_databases.py --help
${create_cistarget_databases_dir}/convert_motifs_or_tracks_vs_regions_or_genes_scores_to_rankings_cistarget_dbs.py --help
```
```bash
"${create_cistarget_databases_dir}/create_cistarget_motif_databases.py" \
    -f "./fasta/Apis_mellifera_4_cisTarget.fasta" \
    -M "./v10nr_clust_public/singletons" \
    -m "./metadata/Bee_motif_cb_ids.txt" \
    -o "./feather/V10nr_clust_tbl-cb-inter_Amel" \
    -t 16
```
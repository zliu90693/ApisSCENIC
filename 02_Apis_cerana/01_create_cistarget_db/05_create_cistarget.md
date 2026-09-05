```bash
cd /home/liuzhiyu/Projects/neo_caste/ApisSCENIC/02_Apis_cerana/01_create_cistarget_db
conda activate create_cistarget_databases
create_cistarget_databases_dir='../../.reference/create_cisTarget_databases'
${create_cistarget_databases_dir}/create_cistarget_motif_databases.py --help
${create_cistarget_databases_dir}/convert_motifs_or_tracks_vs_regions_or_genes_scores_to_rankings_cistarget_dbs.py --help
```
```bash
"${create_cistarget_databases_dir}/create_cistarget_motif_databases.py" \
    -f "./fasta/Apis_cerana_4_cisTarget.fasta" \
    -M "./v10nr_clust_public/singletons" \
    -m "./metadata/Bee_motif_cb_ids.txt" \
    -o "./feather/V10nr_clust_tbl-cb-inter_Acer" \
    -t 16
```
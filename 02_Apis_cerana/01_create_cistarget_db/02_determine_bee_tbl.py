# 同 01_Apis_mellifera/01_create_cistarget_db/02_determine_bee_tbl.py, 此处使用果蝇的TF-motif对照表, 构建中蜂TF-motif对照表
# %%
import pandas as pd
# %%
# fruit fly & honeybee ortho protein name 
Dmel_Acer_Ortho = pd.read_csv("./Orthologues_Drosophila_melanogaster/Drosophila_melanogaster__v__Apis_cerana.tsv", sep="\t")
Dmel_Acer_Ortho
# %%
Dmel_gene_motif_tbl = pd.read_csv("./v10nr_clust_public/snapshots/motifs-v10-nr.flybase-m0.00001-o0.0.tbl", sep="\t")
Dmel_gene_motif_tbl
# %%
# filt 1 to 1 Orthologs:
Dmel_Acer_Ortho_121 = Dmel_Acer_Ortho[
    ~Dmel_Acer_Ortho["Drosophila_melanogaster"].str.contains(",", na=False)
    & ~Dmel_Acer_Ortho["Apis_cerana"].str.contains(",", na=False)
]
Dmel_Acer_Ortho_121
# %%
# fruitfly gene name in tbl -> (fruitfly GTF) -> fruitfly gene ID -> (Dmel_Acer_Ortho) -> bee gene ID -> (motif-to-TF tbl) -> bee motif
Dmel_gtf = pd.read_csv("./gtf/Drosophila_melanogaster.tsv", sep="\t")
Dmel_gtf
# %%
# 根据 01_Apis_mellifera/01_create_cistarget_db/02_determine_bee_tbl.py, 可知果蝇 TF-motif tbl 中的 gene_name 列对应果蝇 GTF 中的 gene_name 列, 
# 果蝇 GTF 中的 gene_id 列对应 Dmel_Acer_Ortho 中的 Drosophila_melanogaster 列
# 在 01_Apis_mellifera/01_create_cistarget_db/02_determine_bee_tbl.py 中，已经建立了 fruitfly gene name in tbl -> (fruitfly GTF) -> fruitfly gene ID 对照关系表，此处直接使用：
# %%
Dmel_gname_gid = pd.read_csv("./metadata/Dmel_gname_gid.tsv", sep="\t", index_col=0)
Dmel_gname_gid
# %%
# fruitfly gene name in tbl -> (fruitfly GTF) -> fruitfly gene ID -> (Dmel_Acer_Ortho) -> bee gene ID 
Dmel_Acer_Ortho_link = Dmel_Acer_Ortho_121[["Drosophila_melanogaster", "Apis_cerana"]].rename(columns={"Drosophila_melanogaster": "gene_id"})
Dmel_Acer_Ortho_link
# %%
Dmel_gname_gid_beegid = Dmel_gname_gid.merge(
    Dmel_Acer_Ortho_link, on="gene_id", how="left"
)
Dmel_gname_gid_beegid = Dmel_gname_gid_beegid.rename(columns={"Apis_cerana": "Acer_gene_id"})
# %%
Dmel_gname_gid_beegid = Dmel_gname_gid_beegid[~Dmel_gname_gid_beegid["Acer_gene_id"].isna()]
Dmel_gname_gid_beegid
# %%
Dmel_gname_gid_beegid.to_csv("./metadata/Dmel_gname_gid_beegid.tsv", sep="\t")
# %%
# fruitfly gene name in tbl -> (fruitfly GTF) -> fruitfly gene ID -> (Dmel_Acer_Ortho) -> bee gene ID -> (motif-to-TF tbl) -> bee motif
Dmel_gname_beegid = Dmel_gname_gid_beegid[["gene_name", "Acer_gene_id"]]
Dmel_gname_beegid
# %%
Bee_gene_motif_tbl = Dmel_gene_motif_tbl.merge(
    Dmel_gname_beegid, on="gene_name", how="left"
)
Bee_gene_motif_tbl = Bee_gene_motif_tbl[~Bee_gene_motif_tbl["Acer_gene_id"].isna()]
Bee_gene_motif_tbl
# %%
Bee_gene_motif_tbl.to_csv("./metadata/Bee_gene_motif_tbl.tsv", sep="\t")
# %%

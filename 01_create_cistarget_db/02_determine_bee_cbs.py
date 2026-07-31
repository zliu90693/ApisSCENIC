# Motifs in honeybees were identified using a motif-to-TF annotation table and Drosophila-Honeybee homologous gene mapping.
# %%
import pandas as pd
# %%
# fruit fly & honeybee ortho protein name 
Dmel_Amel_Ortho = pd.read_csv("./Orthologues_Drosophila_melanogaster/Drosophila_melanogaster__v__Apis_mellifera.tsv", sep="\t")
Dmel_Amel_Ortho
# %%
Dmel_gene_motif_tbl = pd.read_csv("./v10nr_clust_public/snapshots/motifs-v10-nr.flybase-m0.00001-o0.0.tbl", sep="\t")
Dmel_gene_motif_tbl
# %%
# filt 1 to 1 Orthologs:
Dmel_Amel_Ortho_121 = Dmel_Amel_Ortho[
    ~Dmel_Amel_Ortho["Drosophila_melanogaster"].str.contains(",", na=False)
    & ~Dmel_Amel_Ortho["Apis_mellifera"].str.contains(",", na=False)
]
Dmel_Amel_Ortho_121
# %%
# fruitfly gene name -> (fruitfly GTF) -> fruitfly gene ID -> (Dmel_Amel_Ortho) -> bee gene ID -> (motif-to-TF tbl) -> bee motif
# %%
Dmel_gtf = pd.read_csv("./gtf/Drosophila_melanogaster.tsv", sep="\t")
Dmel_gtf
# %%
#? Which column in Dmel_gtf corresponds to the gene_name column in Dmel_gene_motif_tbl?
#? "gene_name" column?
Dmel_gtf_gene_name_set = set(Dmel_gtf["gene_name"].to_list())
Dmel_gene_motif_tbl_gene_name_set = set(Dmel_gene_motif_tbl["gene_name"].to_list())
print(len(Dmel_gtf_gene_name_set)) # 23769
print(len(Dmel_gene_motif_tbl_gene_name_set)) # 645
print(len(Dmel_gtf_gene_name_set & Dmel_gene_motif_tbl_gene_name_set)) # 638
# 7 genes do not match
# %%
print(Dmel_gene_motif_tbl_gene_name_set - Dmel_gtf_gene_name_set)
# {'CG7839', 'h', 'CG4603', 'CG9650', 'CG2199', 'CG5728', 'Parp'}
# query flybase manually
# gene_name gene_id
# CG7839    FBgn0036124
# h         FBgn0001168 (corrected by gpt)
# CG4603    FBgn0035593
# CG9650    FBgn0029939
# CG2199    FBgn0035213
# CG5728    FBgn0039182
# Parp      FBgn0010247 (PARP1, corrected by gpt)
# %%
#? Which column in Dmel_gtf corresponds to the Drosophila_melanogaster column in Dmel_Amel_Ortho?
#? "gene_id" column?
Dmel_gtf_gene_id_set = set(Dmel_gtf["gene_id"].to_list())
Dmel_Amel_Ortho_Dmel_set = set()
for cell in Dmel_Amel_Ortho.iloc[:, 1].dropna():
    for gene in str(cell).split(","):
        gene = gene.strip()
        if gene:
            Dmel_Amel_Ortho_Dmel_set.add(gene)
print(len(Dmel_gtf_gene_id_set)) # 24254
print(len(Dmel_Amel_Ortho_Dmel_set)) # 9330
print(len((Dmel_gtf_gene_id_set & Dmel_Amel_Ortho_Dmel_set))) # 9330
# "gene_id" column in Dmel_gtf corresponds to the Drosophila_melanogaster column in Dmel_Amel_Ortho.
# %%
# link fruitfly gene name and fruitfly gene ID
Dmel_gtf_link = Dmel_gtf[["gene_id", "gene_name"]].drop_duplicates(subset=["gene_name", "gene_id"])
Dmel_gtf_link

Dmel_gene_motif_tbl_gene_name = Dmel_gene_motif_tbl[["gene_name"]].drop_duplicates(subset=["gene_name"])
Dmel_gene_motif_tbl_gene_name
# %%
Dmel_gname_gid = Dmel_gene_motif_tbl_gene_name.merge(
    Dmel_gtf_link, on="gene_name", how="left"
)
gene_id_fix = {
    "CG7839": "FBgn0036124",
    "h":      "FBgn0001168",
    "CG4603": "FBgn0035593",
    "CG9650": "FBgn0029939",
    "CG2199": "FBgn0035213",
    "CG5728": "FBgn0039182",
    "Parp":   "FBgn0010247",
}
for name, gid in gene_id_fix.items():
    Dmel_gname_gid.loc[
        Dmel_gname_gid["gene_name"] == name, "gene_id"
    ] = gid
Dmel_gname_gid
# %%
# link fruitfly gene ID and honeybee gene ID
Dmel_Amel_Ortho_link = Dmel_Amel_Ortho_121[["Drosophila_melanogaster", "Apis_mellifera"]].rename(columns={"Drosophila_melanogaster": "gene_id"})
Dmel_Amel_Ortho_link
# %%
Dmel_gname_gid_beegid = Dmel_gname_gid.merge(
    Dmel_Amel_Ortho_link, on="gene_id", how="left"
)
Dmel_gname_gid_beegid = Dmel_gname_gid_beegid.rename(columns={"Apis_mellifera": "Amel_gene_id"})
# %%
Dmel_gname_gid_beegid = Dmel_gname_gid_beegid[~Dmel_gname_gid_beegid["Amel_gene_id"].isna()]
Dmel_gname_gid_beegid
# %%
Dmel_gname_gid_beegid.to_csv("./metadata/Dmel_gname_gid_beegid.tsv", sep="\t")
# 394 bee genes have motifs in Dmel_gene_motif_tbl
# %%
# get bee motifs
Dmel_gname_beegid = Dmel_gname_gid_beegid[["gene_name", "Amel_gene_id"]]
Dmel_gname_beegid
# %%
Bee_gene_motif_tbl = Dmel_gene_motif_tbl.merge(
    Dmel_gname_beegid, on="gene_name", how="left"
)
Bee_gene_motif_tbl = Bee_gene_motif_tbl[~Bee_gene_motif_tbl["Amel_gene_id"].isna()]
Bee_gene_motif_tbl
# %%
Bee_gene_motif_tbl.to_csv("./metadata/Bee_gene_motif_tbl.tsv", sep="\t")
# %%
# Bee_gene_motif_tbl = pd.read_csv("./metadata/Bee_gene_motif_tbl.tsv", sep="\t")

# %%
#? What is the relationship between column motif ID and .cb prefix?
Dmel_gene_motif_tbl["#motif_id"].nunique() # 19895
# %%
Dmel_motif_id_set = set(Dmel_gene_motif_tbl["#motif_id"].unique())
# %%
from pathlib import Path

cb_dir = Path("./v10nr_clust_public/singletons")
cb_paths = sorted(cb_dir.glob("*.cb"))
# 去掉 .cb 后缀，例如 bergman__Kr.cb -> bergman__Kr
cb_ids_set = {path.stem for path in cb_paths}
print("Number of .cb files:", len(cb_paths)) # 10249
print("Number of unique .cb basenames:", len(cb_ids_set)) # 10249
# %%
print(len(Dmel_motif_id_set & cb_ids_set)) # 3711
# %%
# bee gene ID -> (motif-to-TF tbl) -> bee motif
# select the injection between column #motif_id and .cb file prefix

# %%
print(Bee_gene_motif_tbl["#motif_id"].nunique()) # 16752
Bee_motif_id_set = set(Bee_gene_motif_tbl["#motif_id"].unique())
print(len(Bee_motif_id_set & cb_ids_set)) # 3096
# %%
# <---
Bee_cb_interset = Bee_motif_id_set & cb_ids_set

# %%

bee_cb_df = pd.DataFrame({
    "bee_cb_id": pd.Series(list(Bee_cb_interset)),
})
bee_cb_df.to_csv("./metadata/Bee_motif_cb_ids.txt", index=False, header=False)
Bee_cb_df = pd.read_csv("./metadata/Bee_motif_cb_ids.txt", header=None)
# %%

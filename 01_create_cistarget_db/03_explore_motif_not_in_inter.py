# %%
import pandas as pd
from pathlib import Path
# %%
Bee_gene_motif_tbl = pd.read_csv("./metadata/Bee_gene_motif_tbl.tsv", sep="\t")

cb_dir = Path("./v10nr_clust_public/singletons")
cb_paths = sorted(cb_dir.glob("*.cb"))
# 去掉 .cb 后缀，例如 bergman__Kr.cb -> bergman__Kr
# %%
Bee_motif_id_set = set(Bee_gene_motif_tbl["#motif_id"].unique())
cb_ids_set = {path.stem for path in cb_paths}

print(len(Bee_motif_id_set)) # 16752
print(len(cb_ids_set)) # 10249
print(len(Bee_motif_id_set & cb_ids_set)) # 3096
print(len(Bee_motif_id_set - cb_ids_set)) # 13656
# %%
#? 这些仅在Bee_motif_id_set中出现的motif，其来源数据库都有哪些？
Bee_motif_only = Bee_motif_id_set - cb_ids_set
Bee_motif_only
# %%
Bee_gene_motif_tbl_only = Bee_gene_motif_tbl[Bee_gene_motif_tbl["#motif_id"].isin(Bee_motif_only)]
Bee_gene_motif_tbl_only
# %%
# Bee_gene_motif_tbl_only["source_name"].value_counts()
Bee_gene_motif_tbl_only[["#motif_id", "source_name"]].drop_duplicates(subset=["#motif_id", "source_name"])["source_name"].value_counts()
# factorbook          4226
# cisbp               3440
# transfac_pro        2822
# desso               2028
# swissregulon         557
# taipale              186
# hocomoco             148
# taipale_cyt_meth      67
# flyfactorsurvey       57
# kznf                  45
# homer                 29
# stark                 13
# transfac_public       10
# taipale_tf_pairs      10
# c2h2_zfs               7
# bergman                6
# nitta                  2
# jaspar                 2
# yetfasco               1
# Name: source_name, dtype: int64
# %%
Bee_gene_motif_tbl_only[Bee_gene_motif_tbl_only["#motif_id"].str.startswith("metacluster")]["source_name"].value_counts()
# transfac_pro    715
# ↑一个有意思的现象：以metacluster开头的motif全部来自付费的transfac_pro数据库。
# %%
Bee_gene_motif_tbl_only.to_csv("./metadata/03_motif_notin_cbs/Bee_gene_motif_tbl_only.tsv", sep="\t", index=False)
# %%
#! 到目前为止，我确定了那些“在#motif_id列中出现，但在.cb前缀中未出现”的motif名称，并将其信息（包括motif来源）保存至01_create_cistarget_db/metadata/03_motif_notin_cbs/Bee_gene_motif_tbl_only.tsv

# %%
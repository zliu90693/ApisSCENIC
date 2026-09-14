"""
进行pyscenic grn前的准备, 包括将果蝇的TF list中的名称转换为蜜蜂的一对一同源基因
"""
# %%
import pandas as pd
"""
Dmel TF list -> (?) -> OrthoFinder Dmel gene_id -> OrthoFinder Acer gene_id (Amel TF list)
"""
# %%
dm_TFlist = pd.read_csv("./metadata/allTFs_dmel.txt", header=None)
dm_TFset = set(dm_TFlist[0].to_list())

dm_ac_ortho = pd.read_csv("./Orthologues_Drosophila_melanogaster/Drosophila_melanogaster__v__Apis_cerana.tsv", sep="\t")
dm_ac_ortho_121 = dm_ac_ortho[
    ~dm_ac_ortho["Drosophila_melanogaster"].str.contains(",", na=False)
    & ~dm_ac_ortho["Apis_cerana"].str.contains(",", na=False)
]
dm_ac_ortho_121_dmset = set(dm_ac_ortho_121["Drosophila_melanogaster"].to_list())

# dm_gtf = pd.read_csv("../01_create_cistarget_db/gtf/Drosophila_melanogaster.tsv", sep="\t")
# dm_gtf_gname_set = set(dm_gtf["gene_name"].to_list())
# %%
#! 果蝇 TF 与 gene_id 的对应关系已在 01_Apis_mellifera/02_run_pySCENIC 中求得，无需重复计算：
TF_gid_all = pd.read_csv("./metadata/TF_flygid.tsv", sep="\t")[["gene_name", "gene_id"]]
TF_gid_all
# %%
dm_ac_link = dm_ac_ortho_121[["Drosophila_melanogaster", "Apis_cerana"]].rename(columns={"Drosophila_melanogaster": "gene_id"})
# %%
# TF_gid_all_beegid: 三列，果蝇TF-果蝇gid-蜜蜂gid
TF_gid_all_beegid = TF_gid_all.merge( 
    dm_ac_link, on="gene_id", how="left"
)
# %%
TF_gid_all_beegid
# %%
TF_gid_all_beegid = TF_gid_all_beegid[~TF_gid_all_beegid["Apis_cerana"].isna()]
TF_gid_all_beegid.to_csv("./metadata/TF_flygid_beegid.tsv", sep="\t")
# %%
#? 我最终找到了多少个西方蜜蜂对应的TF？
TF_gid_all_beegid["Apis_cerana"].nunique() # 567
# %%
#? 前人找到了多少个西方蜜蜂对应的TF？
dmel_acer_TF_HY = pd.read_csv("/home/liuzhiyu/Projects/neo_caste/ApisSCENIC/.reference/data_from_LZU/GRN/allTFs_dmel_acer.txt", encoding="utf-16",
    sep="\t",)
dmel_acer_TF_HY = dmel_acer_TF_HY[~dmel_acer_TF_HY["acer"].isna()]
dmel_acer_TF_HY["acer"].nunique() # 540
# %%
TF_gid_all_beegid["Apis_cerana"].drop_duplicates().to_csv("./metadata/TF_bee.txt", header=False, index=False)
# %%
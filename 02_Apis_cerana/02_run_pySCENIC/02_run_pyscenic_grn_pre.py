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

dm_gtf = pd.read_csv("../01_create_cistarget_db/gtf/Drosophila_melanogaster.tsv", sep="\t")
dm_gtf_gname_set = set(dm_gtf["gene_name"].to_list())
# %%
#! 根据 01_Apis_mellifera/02_run_pySCENIC/02_run_pyscenic_grn_pre.py，可知 Dmel TF list 与 GTF 中的 gene_id 列完全不对应，
#! 与 gene_name 列部分对应，因此或许需要手动处理
print(len(dm_TFset)) # 841
print(len(dm_gtf_gname_set)) # 23769
print(len(dm_TFset & dm_gtf_gname_set)) # 786
# %%
print(dm_TFset - dm_gtf_gname_set)
# %%

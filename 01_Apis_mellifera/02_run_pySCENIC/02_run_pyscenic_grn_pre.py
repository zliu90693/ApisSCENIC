"""
进行pyscenic grn前的准备, 包括将果蝇的TF list中的名称转换为蜜蜂的一对一同源基因
"""
# %%
import pandas as pd
"""
Dmel TF list -> (?) -> OrthoFinder Dmel gene_id -> OrthoFinder Amel gene_id (Amel TF list)
"""
# %%
#? 果蝇的TF list可能对应OrthoFinder结果中果蝇的gene_id吗？
dm_TFlist = pd.read_csv("./metadata/allTFs_dmel.txt", header=None)
dm_TFset = set(dm_TFlist[0].to_list())
# %%
dm_am_ortho = pd.read_csv("./Orthologues_Drosophila_melanogaster/Drosophila_melanogaster__v__Apis_mellifera.tsv", sep="\t")
dm_am_ortho
# %%
dm_am_ortho_121 = dm_am_ortho[
    ~dm_am_ortho["Drosophila_melanogaster"].str.contains(",", na=False)
    & ~dm_am_ortho["Apis_mellifera"].str.contains(",", na=False)
]
dm_am_ortho_121
# %%
dm_am_ortho_121_dmset = set(dm_am_ortho_121["Drosophila_melanogaster"].to_list())
print(len(dm_am_ortho_121_dmset & dm_TFset)) # 0
#! 果蝇的TF list对应的并非果蝇的gene_id，有可能是gene_name，需要验证
# %%


# %%
#? 果蝇的TF list可能对应GTF中果蝇的gene_name吗？
dm_gtf = pd.read_csv("../01_create_cistarget_db/gtf/Drosophila_melanogaster.tsv", sep="\t")
dm_gtf_gname_set = set(dm_gtf["gene_name"].to_list())
# %%
print(len(dm_TFset)) # 841
print(len(dm_gtf_gname_set)) # 23769
print(len(dm_TFset & dm_gtf_gname_set)) # 786
#! 确实对应GTF中果蝇的gene_name，但并非完全匹配，有841-786=55个基因在GTF的gene_name列中未出现
# %%

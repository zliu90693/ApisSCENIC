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


# %%
"""
通过查询Biomi及其他来源, 得知可以通过s3ftp.flybase.org来源的 tsv 以确定这些 TF 名称对应的 gene_id, 在 01_get_data.md 中补充下载
接下来将解析 tsv 以确定 TF 身份
"""
dm_TF_notin_GTF_set = dm_TFset - dm_gtf_gname_set # 未出现在 GTF 的 gene_name 列中的 TF 名称，共 55 个
dm_TF_notin_GTF_set
# %%
fbgn_annotation = pd.read_csv("./metadata/fbgn_annotation_ID_fb_2026_02.tsv", sep="\t", skiprows=4) # 上文指的就是这个tsv
fbgn_annotation
# %%
fbgn_annotation_sub = fbgn_annotation[fbgn_annotation["annotation_ID"].isin(dm_TF_notin_GTF_set)]
fbgn_annotation_sub.shape # (36, 6) 共识别出了 55 个 TF 名称中的 36 个，还有 19 个未识别
# %%
# gene_map_table[gene_map_table["cytogenetic_loc"].isin(dm_TF_notin_GTF_set)]
# %%
dm_TF_notin_GTF_set_1found = set(fbgn_annotation_sub["annotation_ID"])
dm_TF_notin_GTF_set_1notfound = dm_TF_notin_GTF_set - dm_TF_notin_GTF_set_1found
dm_TF_notin_GTF_set_1notfound
# %%
# 手动从 FlyBase 中（重点查看 Also Known As 名称）查询剩余 19 个 TF （即 dm_TF_notin_GTF_set_1notfound）的 gene_id：
# TF列表中的名称    当前FlyBase符号    FBgn ID
# Argk  Argk1   FBgn0000116
# CstF-64   CstF64  FBgn0027841
# DNApol-iota   Poll    FBgn0037554
# Ef1beta   eEF1β   FBgn0028737
# Eip71CD   MsrA    FBgn0000565
# 
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
# 手动从 FlyBase 中查询剩余 19 个 TF （即 dm_TF_notin_GTF_set_1notfound）的 gene_id：
#! 重点查看 FlyBase 中的 Also Known As 名称!!!
# TF列表中的名称    当前FlyBase符号    FBgn ID
# Argk  Argk1   FBgn0000116
# CstF-64   CstF64  FBgn0027841
# DNApol-iota   Poll    FBgn0037554
# Ef1beta   eEF1β   FBgn0028737
# Eip71CD   MsrA    FBgn0000565
# Gpdh   Gpdh1   FBgn0001128
# Ime4  Mettl3  FBgn0039139
# Mes4  PolE4   FBgn0034726
# Parp  Parp1  FBgn0010247
# Pepck  Pepck1 FBgn0003067
# RpII215  Polr2A   FBgn0003277
# Scsalpha  Scsα1   FBgn0004888
# Thiolase  Mtpβ    FBgn0025352
# e(y)1 Taf9    FBgn0000617
# eIF-5A  eEF5  FBgn0285952
# fd64A FoxL1 FBgn0004895
# h hry FBgn0001168
# lid   Kdm5    FBgn0031759
# nos   nanos   FBgn0002962
# %%
dm_TF_notin_GTF_set_2found = pd.read_csv("./metadata/TF_gid_manual.csv")
dm_TF_notin_GTF_set_2found
# %%
"""
至此, 全部 841 个 TF 已确定到 gene_id, 其中 786 个在 GTF 中已确定, 36 个在 fbgn_annotation 中已确定, 19 个通过手动查询 FlyBase 已确定
"""
TF_gid_in_GTF = dm_gtf[dm_gtf["gene_name"].isin(dm_TFset)][["gene_name", "gene_id"]].drop_duplicates()
TF_gid_in_fbgn_annotation = fbgn_annotation_sub[["annotation_ID", "primary_FBgn#"]].rename(columns={"annotation_ID": "gene_name", "primary_FBgn#": "gene_id"})
TF_gid_in_manual = dm_TF_notin_GTF_set_2found[["TF", "FBgn_ID"]].rename(columns={"TF": "gene_name", "FBgn_ID": "gene_id"})
TF_gid_all = pd.concat([TF_gid_in_GTF, TF_gid_in_fbgn_annotation, TF_gid_in_manual], ignore_index=True)
TF_gid_all
# %%

# %%
gid_dup_8 = {"FBgn0032130", "FBgn0036126", "FBgn0032430", "FBgn0004895", "FBgn0032016", "FBgn0039139", "FBgn0038549", "FBgn0030687"}

# %%
dmel_acer_TF_HY = pd.read_csv("/home/liuzhiyu/Projects/neo_caste/ApisSCENIC/.reference/data_from_LZU/GRN/allTFs_dmel_acer.txt", encoding="utf-16",
    sep="\t",)
print(dmel_acer_TF_HY[dmel_acer_TF_HY["dmel"].isin(dm_TF_notin_GTF_set_1notfound)]) # 除了nos外都是missing，但是HY的果蝇nos竟然和中蜂有同源基因？
# %%
print(dmel_acer_TF_HY[dmel_acer_TF_HY["dmel"].isin(dm_TF_notin_GTF_set_1found)]) # 全部为missing

#? 我的OrthoFinder步骤是否存在问题？(指的是nos的同源基因在HY的结果中找得到但在我的OrthoFinder结果中找不到) 
#! 或许与Acer在OrthoFinder中默认使用protein_id而不是gene_id有关
#? HY采用了怎样的标准处理那些找不到gene_id的TF？手动核对还是直接丢弃了？
# %%

"""
在使用create_cistarget_motif_databases.py构建cistarget数据库时, 应该选取基因组中的哪些基因?
1. 选GTF中的全部基因? 可能导致feather中特定motif的排名信息中出现一些表达矩阵中不存在的基因, 如果这些在表达矩阵中不存在的基因集中出现在motif排名前列, 可能会降低表达矩阵中存在的基因的NES评分
2. 选仅在表达矩阵中出现的基因? 可能会导致原本在motif排名信息中靠后的基因因为没有“表达矩阵中不存在的基因”的阻隔而出现在靠前的位置, 使得NES评分虚高

在之前的人的分析中, feather中包含哪些基因?
"""
# %%
import scanpy as sc
import pandas as pd
# %%
HY_amel = sc.read_h5ad("/data/share/data/Zhou_lab_seq_data/20251022_scRNA_lzy/1_LZU/ori_h5ad/amel_all_concat_clustered_annotation.h5ad")
h5ad_genes_set = set(HY_amel.var["gene_ids"].to_list())
# HY_amel.var.shape[0] # 11793
# %%
HY_feather = pd.read_feather("../../.reference/data_from_LZU/GRN/database/Amel_cistarget_motif.regions_vs_motifs.rankings.feather")
HY_feather
# %%
HY_feather_genes = HY_feather.columns
len(HY_feather_genes) # 12362
# %%
# from matplotlib_venn import venn2
# import matplotlib.pyplot as plt

# h5ad_genes_set = set(HY_amel.var["gene_ids"].to_list())
feather_genes_set = set(HY_feather_genes)
feather_genes_set.remove("motifs")
# %%
# venn2([h5ad_genes_set, feather_genes_set], set_labels=("h5ad_genes", "feather_genes"))
# plt.show()
# # %%
# h5ad_genes_set - feather_genes_set 
# {'GeneID_807690',
#  'GeneID_807691',
#  'GeneID_807692',
#  'GeneID_807693',
#  'GeneID_807694',
#  'GeneID_807695',
#  'GeneID_807696',
#  'GeneID_807697',
#  'GeneID_807698',
#  'GeneID_807699',
#  'GeneID_807700',
#  'GeneID_807701',
#  'GeneID_807702'}
# 13个线粒体基因
# %%
# feather_genes_set - h5ad_genes_set
# %%
import pyranges as pr

Amel_gtf = pr.read_gtf("../../01_Apis_mellifera/01_create_cistarget_db/gtf/Apis_mellifera.gtf")
Amel_gtf = Amel_gtf.df
# Amel_gtf[Amel_gtf["gene_id"].isin(h5ad_genes_set)]["gene_biotype"].unique() # 'protein_coding', 'lncRNA'
# %%
# %%
gtf_allgene_set = set(Amel_gtf["gene_id"].to_list())
print(len(gtf_allgene_set)) # 12398
print(len(feather_genes_set)) # 12361
print(len(gtf_allgene_set & feather_genes_set)) # 12361 feather中基因是GTF中全部基因的子集
print(len(gtf_allgene_set - feather_genes_set)) # 37
# %%
# GTF中哪些基因未被选入feather？
Amel_gtf_notin_feather = Amel_gtf[~Amel_gtf["gene_id"].isin(feather_genes_set)]
Amel_gtf_notin_feather
# %%
Amel_gtf_notin_feather["gene_id"].nunique() # 37
# %%
Amel_gtf_notin_feather["gene_name"].nunique() # 13
# %%
Amel_gtf_in_feather = Amel_gtf[Amel_gtf["gene_id"].isin(feather_genes_set)]
Amel_gtf_in_feather["gene_biotype"].unique() 
# 'protein_coding', 'lncRNA', 'miRNA', 'pre_miRNA', 'snRNA', 'tRNA','snoRNA', 'pseudogene', 'rRNA', 'nontranslating_CDS', 'guide_RNA'
# %%
"""
答案解开了, HY将全部GTF中除了线粒体基因外其他所有基因都用于生成feather
"""
# %%
import pandas as pd
import scanpy as sc
# %%
# 表达矩阵中的基因名称对应的是gene_name还是gene_id？
# %%
Amel_adata = sc.read_h5ad("/data/share/data/Zhou_lab_seq_data/20251022_scRNA_lzy/1_LZU/ori_h5ad/amel_all_concat_clustered_annotation.h5ad")
Amel_adata
# %%
Amel_gene_set = set(Amel_adata.var["gene_ids"])
# %%
Amel_gtf = pd.read_csv("./01_create_cistarget_db/gtf/Apis_mellifera.tsv", sep="\t")
Amel_gtf
# %%
Amel_gtf_geneid_set = set(Amel_gtf["gene_id"].to_list())
Amel_gtf_geneid_set
# %%
print(len(Amel_gene_set))
print(len(Amel_gtf_geneid_set))
print(len(Amel_gene_set & Amel_gtf_geneid_set))
# %%
print(len(Amel_gtf_geneid_set - Amel_gene_set))
# %%
Amel_adata_me = sc.read_h5ad("../downstream_analysis/Zhang_iScience_2022_Amel/data/7_cluster-output/concat.h5ad")
Amel_adata_me
# %%
Amel_gene_me_set = set(Amel_adata_me.var["gene_ids"])
# %%
print(len(Amel_gene_me_set))
print(len(Amel_gtf_geneid_set))
print(len(Amel_gene_me_set & Amel_gtf_geneid_set))
# %%
print(len(Amel_gtf_geneid_set - Amel_gene_me_set))
# 奇怪了，形成表达矩阵过程中，var_name究竟是GTF中的什么？gene_id？

# %%
Amel_gtf_genename_set = set(Amel_gtf["gene_name"].to_list())
Amel_gtf_genename_set
# %%
print(len(Amel_gene_set))
print(len(Amel_gtf_genename_set))
print(len(Amel_gene_set & Amel_gtf_genename_set))
# %%
print(len(Amel_gtf_genename_set - Amel_gene_set))
# %%
#! 得到结论：adata.var["gene_ids"]来源于GTF的gene_id列。adata.var_names来源于什么不知道，但肯定跟["gene_ids"]不一样
# %%

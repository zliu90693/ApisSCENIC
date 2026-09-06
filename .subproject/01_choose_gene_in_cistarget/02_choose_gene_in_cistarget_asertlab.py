"""
仿照01_choose_gene_in_cistarget.py, 看看asertlab中果蝇的feather保留了GTF中的哪些基因
"""
# %%
import scanpy as sc
import pandas as pd
import pyranges as pr
from matplotlib_venn import venn3
from matplotlib_venn import venn2
import matplotlib.pyplot as plt
# %%
dm_feather = pd.read_feather("../../01_Apis_mellifera/01_create_cistarget_db/feather/dm6_v10_clust.genes_vs_motifs.rankings.feather")
feather_genes_set = set(dm_feather.columns)
feather_genes_set.remove("motifs")
# %%
dm_GTF = pr.read_gtf("../../01_Apis_mellifera/01_create_cistarget_db/gtf/Drosophila_melanogaster.gtf").df
gtf_allgene_set = set(dm_GTF["gene_id"].to_list())
gtf_allgenename_set = set(dm_GTF["gene_name"].to_list())
# %%
# feather中的基因名称对应GTF中的哪一列?
venn3([feather_genes_set, gtf_allgene_set, gtf_allgenename_set], set_labels=("feather_gene", "gtf_geneid", "gtf_genename"))
plt.show()
# %%
# %%
"""
无法进一步实验, 因为无法确定feather中的基因名称对应GTF中的哪一列, gene_id列和gene_name列都不能完美对应
"""
# %%
#? GTF和feather交集中的基因的biotype是怎样的？
feather_gtf_inter = gtf_allgenename_set & feather_genes_set
dm_GTF_inter = dm_GTF[dm_GTF["gene_name"].isin(feather_gtf_inter)] 
dm_GTF_inter["gene_biotype"].unique() # 'protein_coding', 'snoRNA', 'ncRNA', 'pseudogene', 'tRNA', 'snRNA', 'rRNA'
# %%
#? GTF中的线粒体基因有出现在feather中吗？
mt_genename = set(dm_GTF[dm_GTF["Chromosome"]=="mitochondrion_genome"]["gene_name"].to_list())
# %%
venn2([mt_genename, feather_genes_set], set_labels=("mt", "feather")) # feather中没有任何线粒体基因
# %%
"""
目前只能确定feather中没有线粒体基因 但是不确定有没有人为删去miRNA、pre_miRNA、nontranslating_CDS、guide_RNA等
"""
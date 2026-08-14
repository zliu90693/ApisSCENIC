"""
在这一issue中: https://github.com/aertslab/create_cisTarget_databases/issues/57, 提问者提出了与我类似的问题：
官方提供的小鼠.feather数据库中, 有大概5000个motif, 但只有约3500个出现在motif集合中。
我很好奇, 官方提供的果蝇.feather数据库中, 有多少个motif? 
这些motif又与TF-motif对照表中的“#motif_id”列, 以及cb文件前缀的关系是怎样的?
"""
# wget https://resources.aertslab.org/cistarget/databases/drosophila_melanogaster/dm6/flybase_r6.02/mc_v10_clust/gene_based/dm6_v10_clust.genes_vs_motifs.rankings.feather
# %%
import pandas as pd
# %%
dm_feather = pd.read_feather("./feather/dm6_v10_clust.genes_vs_motifs.rankings.feather")
dm_feather_motif_id_set = set(dm_feather["motifs"].to_list())
# %%
from pathlib import Path

cb_dir = Path("./v10nr_clust_public/singletons")
cb_paths = sorted(cb_dir.glob("*.cb"))
# 去掉 .cb 后缀，例如 bergman__Kr.cb -> bergman__Kr
cb_ids_set = {path.stem for path in cb_paths}
# %%
dm_motif_TF_tbl = pd.read_csv("./v10nr_clust_public/snapshots/motifs-v10-nr.flybase-m0.00001-o0.0.tbl", sep="\t")
dm_motif_TF_tbl_motifID_set = set(dm_motif_TF_tbl["#motif_id"].to_list())

# %%
#! 与.cb文件前缀
# 官方feather中的motif与.cb文件前缀的交集
print(len(dm_feather_motif_id_set)) # 1378
print(len(cb_ids_set)) # 10249
print(len(cb_ids_set & dm_feather_motif_id_set)) # 1255
# %%
# 官方feather中的motif中，有哪些.cb文件前缀不存在的内容？
dm_feather_motif_id_set - cb_ids_set # 全是metacluster和transfac_pro
# %%
#! 与TF-motif对照表中的“#motif_id”列
# 官方feather中的motif与TF-motif对照表中的“#motif_id”列的交集
print(len(dm_motif_TF_tbl_motifID_set)) # 19895
print(len(dm_motif_TF_tbl_motifID_set & dm_feather_motif_id_set)) # 1378
# %%
# 官方feather中的motif中，有哪些“#motif_id”列不存在的内容？
dm_feather_motif_id_set - dm_motif_TF_tbl_motifID_set # set()
# 没有
# %%
from matplotlib_venn import venn3
import matplotlib.pyplot as plt

venn3([dm_feather_motif_id_set, cb_ids_set, dm_motif_TF_tbl_motifID_set], set_labels=("feather_motif", "cb_motif", "tbl_motif"))
plt.show()
# %%

# # %%
# dm8_feather = pd.read_feather("./feather/dm6-5kb-upstream-full-tx-11species.mc8nr.genes_vs_motifs.rankings.feather")
# dm8_feather_motif_id_set = set(dm8_feather["motifs"].to_list())
# # %%
# venn3([dm8_feather_motif_id_set, cb_ids_set, dm_motif_TF_tbl_motifID_set], set_labels=("8feather_motif", "cb_motif", "tbl_motif"))
# plt.show()
# %%

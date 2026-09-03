"""
由之前项目可知, 官方提供的果蝇feather中有1378个motif
但是, 果蝇的motif-TF对照表和cb文件前缀的交集包括3711个motif
为什么会差这么多?   
可能是因为官方构建feather前对cb文件进行了筛选吗? 筛选标准是什么? 
可能是motif-TF对照表和cb文件前缀的交集(3711)对应的gene_name与pyscenic grn中使用的TF_list中的TF交集对应的motif吗?
"""
# %%
import pandas as pd
from pathlib import Path
# %%
Dmel_tbl = pd.read_csv("./v10nr_clust_public/snapshots/motifs-v10-nr.flybase-m0.00001-o0.0.tbl", sep="\t")
tbl_motif_id_set = set(Dmel_tbl["#motif_id"].to_list())
tbl_motif_id_set
# %%
cb_dir = Path("./v10nr_clust_public/singletons")
cb_paths = sorted(cb_dir.glob("*.cb"))
cb_set = {path.stem for path in cb_paths}
# %%
tbl_cb_inter = tbl_motif_id_set & cb_set
len(tbl_cb_inter) # 3711
# %%
Dmel_tbl_sub = Dmel_tbl[Dmel_tbl["#motif_id"].isin(tbl_cb_inter)]
Dmel_tbl_sub
# %%
Deml_TFlist = pd.read_csv("https://resources.aertslab.org/cistarget/tf_lists/allTFs_dmel.txt", header=None)
Deml_TF_set = set(Deml_TFlist[0].to_list())
Deml_TF_set
# %%
"""
按照之前的假定推测, 官方可能将Dmel_tbl_sub的gene_name列内容与Deml_TF_set取交集,
得到的结果可能是feather motif中去除付费数据库的部分, 接下来进行验证: 
"""
Assumed_feather_motif_set = set(Dmel_tbl_sub[Dmel_tbl_sub["gene_name"].isin(Deml_TF_set)]["#motif_id"].to_list())
Assumed_feather_motif_set
# %%
print(len(Assumed_feather_motif_set)) # 3508
# %%
dm_feather = pd.read_feather("./feather/dm6_v10_clust.genes_vs_motifs.rankings.feather")
dm_feather_motif_id_set = set(dm_feather["motifs"].to_list())
# %%
from matplotlib_venn import venn3
import matplotlib.pyplot as plt
# %%
venn3([dm_feather_motif_id_set, tbl_motif_id_set, cb_set],
      set_labels=("feather_motif", "tbl_motif", "cb_motif"))
plt.show()
# %%
venn3([dm_feather_motif_id_set, Assumed_feather_motif_set, tbl_motif_id_set & cb_set],
      set_labels=("feather_motif", "assumed_feather_motif", "inter_motif"))
plt.show()
# %%
"""
根据结果, motif-TF对照表和cb文件前缀的交集(3711)对应的gene_name与TF_list交集对应的motif共3508个, 仅略小于3711, 与真实的feather motif完全不近似
因此, 推测不成立, 官方并非使用"3711对应的gene_name与TF_list交集对应的motif"生成feather
接下来, 将使用蜜蜂中的交集正式进行建库
"""
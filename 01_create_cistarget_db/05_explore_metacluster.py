"""
保险起见, 我需要知道对照表中的#motif_id列是怎样处理前缀为metacluster的cb文件的? 
(1) #motif_id列直接原样保存了metacluster.cb文件的前缀 (理想结果)
(2) #motif_id列分开保存了metacluster.cb文件内部的多个PWM名称 (不太希望看见)
"""
# %%
import pandas as pd
from pathlib import Path

# %%
Dmel_tbl = pd.read_csv("./v10nr_clust_public/snapshots/motifs-v10-nr.flybase-m0.00001-o0.0.tbl", sep="\t")
Dmel_tbl
# %%
cb_dir = Path("./v10nr_clust_public/singletons")
cb_paths = sorted(cb_dir.glob("metacluster*.cb"))
# 提取 metacluster 中每个文件里以 ">" 开头的标题行，生成 [文件名, motif标题] 两列表格
records = []
for cb_path in cb_paths:
    with open(cb_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                # 去掉开头的 ">"，得到标题
                records.append({"cb_file": cb_path.name, "title": line[1:]})

title_tbl = pd.DataFrame(records, columns=["cb_file", "title"])
title_tbl
# %%
title_tbl["cb_prefix"] = title_tbl["cb_file"].str[:-3]
title_tbl
# %%
# 提取title_tbl中，metacluster中全部标题名的集合
title_set = set(title_tbl["title"].to_list())
title_set
# %%
# 提取motif-TF tbl中，#motif_id的集合
tbl_motif_id_set = set(Dmel_tbl["#motif_id"].to_list())
tbl_motif_id_set
# %%
# 理想情况下，如果#motif_id列仅原样保存metacluster名称而不保存metacluster中的标题名称，那么title_set本应该不存在重合tbl_motif_id_set
print(len(title_set)) # 9440
print(len(tbl_motif_id_set)) # 19895
print(len(title_set & tbl_motif_id_set)) #! 1 ??????
# %%
title_set & tbl_motif_id_set # homer__ATGCATAATTCA_Pit1+1bp
# %%
#! 检查一下这个homer__ATGCATAATTCA_Pit1+1bp是否会出现在#motif_id与全部cb前缀的交集中，没有则不用担心
all_cb_paths = sorted(cb_dir.glob("*.cb"))
all_cb_ids_set = {path.stem for path in all_cb_paths}
"homer__ATGCATAATTCA_Pit1+1bp" in (all_cb_ids_set & tbl_motif_id_set) # False
# %%
"""
可以认为, 真实情况近似等同于我的推测(1)
"""
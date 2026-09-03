# %%
import pandas as pd

TF_motif_v9 = pd.read_csv("./motifs-v9-nr.flybase-m0.001-o0.0.tbl", sep="\t")
TF_motif_v9
# %%
TF_motif_v9["#motif_id"].nunique()
# %%
v9_motif_id_set = set(TF_motif_v9["#motif_id"].unique())
# %%
from pathlib import Path

cb_dir = Path("./01_Apis_mellifera/01_create_cistarget_db/v10nr_clust_public/singletons")
cb_paths = sorted(cb_dir.glob("*.cb"))
# 去掉 .cb 后缀，例如 bergman__Kr.cb -> bergman__Kr
cb_ids = {path.stem for path in cb_paths}
print("Number of .cb files:", len(cb_paths))
print("Number of unique .cb basenames:", len(cb_ids))
# %%
print(len(v9_motif_id_set & cb_ids)) 
# %%

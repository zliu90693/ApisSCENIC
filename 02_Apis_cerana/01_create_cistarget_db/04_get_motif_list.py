"""
获取create_cistarget_motif_databases.py的-m参数对应的motif列表(即蜜蜂tbl中的#motif_id与cb文件前缀的交集), 并整理为文本格式
"""
# %%
import pandas as pd
from pathlib import Path
# %%
Bee_gene_motif_tbl = pd.read_csv("./metadata/Bee_gene_motif_tbl.tsv", sep="\t")
Bee_motif_id_set = set(Bee_gene_motif_tbl["#motif_id"].unique())
# %%
cb_dir = Path("./v10nr_clust_public/singletons")
cb_paths = sorted(cb_dir.glob("*.cb"))
cb_ids_set = {path.stem for path in cb_paths}
# %%
Bee_cb_interset = Bee_motif_id_set & cb_ids_set
# %%
Bee_cb_interset_filename = {f'{cb}.cb' for cb in Bee_cb_interset}
# %%
bee_cb_df = pd.DataFrame({
    "bee_cb_id": pd.Series(list(Bee_cb_interset_filename)),
})
bee_cb_df.to_csv("./metadata/Bee_motif_cb_ids.txt", index=False, header=False)
# %%

```bash
conda activate create_cistarget_databases
```
```bash
create_cistarget_databases_dir='./.reference/create_cisTarget_databases'
# ${create_cistarget_databases_dir}/create_cistarget_motif_databases.py --help
${create_cistarget_databases_dir}/create_fasta_with_padded_bg_from_bed.sh --help
${create_cistarget_databases_dir}/create_cistarget_motif_databases.py --help
```

```python
import sys
interpreter_path = sys.executable
print(f"当前解释器路径: {interpreter_path}")
```
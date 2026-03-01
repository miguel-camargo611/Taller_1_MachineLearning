import json
with open('taller1.ipynb', encoding='utf-8') as f:
    nb = json.load(f)
with open('taller1_code.py', 'w', encoding='utf-8') as f:
    f.write('\n# --- CELL ---\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code'))

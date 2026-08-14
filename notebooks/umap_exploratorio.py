from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from umap import UMAP

base = Path(__file__).resolve().parent
input_file = base / 'dataset_caracteristicas_IA.xlsx'
output_plot = base / 'umap_exploratorio.png'
output_csv = base / 'umap_coordenadas.csv'

features = [
    'Media_basal',
    'Std_basal',
    'Umbral',
    'N_candidatos',
    'N_eventos_pre_peak',
    'Duracion_promedio_eventos',
    'Duracion_maxima_eventos',
    'Amplitud_promedio_eventos',
    'Amplitud_maxima_eventos',
    'Distancia_primer_evento_al_peak',
]

df = pd.read_excel(input_file)
df_ml = df.copy()

X = df_ml[features].fillna(0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

umap = UMAP(n_neighbors=15, min_dist=0.3, n_components=2, random_state=42)
X_umap = umap.fit_transform(X_scaled)

df_ml['UMAP1'] = X_umap[:, 0]
df_ml['UMAP2'] = X_umap[:, 1]

color_codes = df_ml['Archivo'].astype('category').cat.codes

plt.figure(figsize=(8, 6))
plt.scatter(df_ml['UMAP1'], df_ml['UMAP2'], c=color_codes, cmap='tab10', s=70, alpha=0.9)
for _, row in df_ml.iterrows():
    plt.text(row['UMAP1'], row['UMAP2'], str(row['ROI']), fontsize=7)

plt.xlabel('UMAP 1')
plt.ylabel('UMAP 2')
plt.title('UMAP de características pre-peak por ROI')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(output_plot, dpi=200, bbox_inches='tight')
plt.close()

df_ml[['Archivo', 'ROI', 'UMAP1', 'UMAP2']].to_csv(output_csv, index=False)

print(f'Plot guardado en: {output_plot}')
print(f'Coordenadas guardadas en: {output_csv}')
print(df_ml[['Archivo', 'ROI', 'UMAP1', 'UMAP2']].head().to_string(index=False))

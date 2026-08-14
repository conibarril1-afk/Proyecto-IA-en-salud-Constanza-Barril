import json
from pathlib import Path

path = Path(r'c:\Users\cabs2\Documents\Proyecto IA\Analisis_ROI\ROI.ipynb')
nb = json.loads(path.read_text(encoding='utf-8'))

new_source = '''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Elegir curvas representativas por cluster
# =========================

if 'analisis_nuevo' not in globals():
    raise NameError('No existe la variable analisis_nuevo con las curvas ΔF/F₀.')

if 'X_scaled' not in globals():
    raise NameError('No existe X_scaled para medir la distancia al centro del cluster.')

if 'Cluster' not in df_ml.columns:
    raise ValueError('df_ml no tiene la columna Cluster.')

# Preparar la tabla de curvas
if 'normalizar_nombres_roi' in globals():
    analisis_plot = normalizar_nombres_roi(analisis_nuevo.copy())
else:
    analisis_plot = analisis_nuevo.copy()


def resolver_columna_roi(roi_name, df):
    if roi_name in df.columns:
        return roi_name

    if roi_name.startswith('dF_F0_ROI'):
        alternativo = roi_name.replace('dF_F0_ROI', 'dF_F0_Mean', 1)
        if alternativo in df.columns:
            return alternativo
    elif roi_name.startswith('dF_F0_Mean'):
        alternativo = roi_name.replace('dF_F0_Mean', 'dF_F0_ROI', 1)
        if alternativo in df.columns:
            return alternativo

    sufijo = ''.join(ch for ch in roi_name if ch.isdigit())
    for col in df.columns:
        if col.startswith('dF_F0_') and ''.join(ch for ch in col if ch.isdigit()) == sufijo:
            return col

    return None


def pendiente_absoluta(series):
    series = pd.to_numeric(series, errors='coerce').dropna()
    if len(series) < 2:
        return np.nan
    x = np.arange(len(series))
    return abs(np.polyfit(x, series, 1)[0])


def obtener_frame_peak(roi_name):
    col = resolver_columna_roi(roi_name, analisis_plot)
    if col is None:
        return None

    if 'analizar_pre_peak' in globals():
        df_local = analisis_plot[['Frame', col]].copy()
        resultado = analizar_pre_peak(
            df_local,
            roi=col,
            n_baseline=30,
            ventana_suavizado=3,
            umbral_factor=2.0,
            min_frames=2,
            mostrar=False,
            solo_pre_peak=False,
        )
        if resultado.get('frame_peak') is not None:
            return int(resultado['frame_peak'])

    if 'df_resumen_pre_peak' in globals():
        summary = globals()['df_resumen_pre_peak']
        if 'ROI' in summary.columns and 'Frame_peak' in summary.columns:
            match = summary[summary['ROI'] == roi_name]
            if not match.empty:
                return int(match['Frame_peak'].iloc[0])

    series = pd.to_numeric(analisis_plot[col], errors='coerce').replace([np.inf, -np.inf], np.nan)
    if series.dropna().empty:
        return None

    peak_idx = int(np.nanargmax(series.to_numpy()))
    return int(analisis_plot['Frame'].iloc[peak_idx])

# Mantener solo las ROIs de df_ml que sí existen en las curvas actuales
mask_plot = df_ml['ROI'].apply(lambda roi: resolver_columna_roi(roi, analisis_plot) is not None)
plot_df = df_ml.loc[mask_plot].copy()
plot_df['Cluster'] = plot_df['Cluster'].astype(int)

if plot_df.empty:
    raise ValueError('No hay ROIs de df_ml que puedan mapearse a las curvas disponibles en analisis_nuevo.')

clusters = sorted(plot_df['Cluster'].unique())

textos_cluster = {
    0: 'actividad pre-peak frecuente y sostenida de baja amplitud',
    1: 'eventos pre-peak escasos pero de alta amplitud',
    2: 'actividad pre-peak leve o moderada, patrón predominante',
}

representantes = []

for cluster_id in clusters:
    cluster_rows = plot_df[plot_df['Cluster'] == cluster_id].copy()
    if cluster_rows.empty:
        continue

    opciones = []
    for _, row in cluster_rows.iterrows():
        col = resolver_columna_roi(row['ROI'], analisis_plot)
        if col is None:
            continue
        serie = analisis_plot[col].astype(float).replace([np.inf, -np.inf], np.nan).dropna()
        if serie.empty:
            continue
        slope = pendiente_absoluta(serie)

        if cluster_id == 0:
            score = (
                row['N_eventos_pre_peak'] * 1.1
                + row['Duracion_promedio_eventos'] * 0.2
                - row['Amplitud_maxima_eventos'] * 0.25
                - slope * 0.1
            )
        elif cluster_id == 1:
            score = (
                row['Amplitud_maxima_eventos'] * 1.2
                + row['N_eventos_pre_peak'] * 0.15
                - slope * 0.25
            )
        else:
            score = (
                -row['N_eventos_pre_peak'] * 0.8
                - row['Amplitud_maxima_eventos'] * 0.25
                - slope * 0.1
            )

        opciones.append({
            'ROI': row['ROI'],
            'Columna': col,
            'score': score,
            'amplitud': row['Amplitud_maxima_eventos'],
            'eventos': row['N_eventos_pre_peak'],
            'duracion': row['Duracion_promedio_eventos'],
            'slope': slope,
        })

    if not opciones:
        continue

    opciones_df = pd.DataFrame(opciones).sort_values('score', ascending=False)
    representativa = opciones_df.iloc[0]
    frame_peak = obtener_frame_peak(representativa['ROI'])

    representantes.append({
        'Cluster': int(cluster_id),
        'ROI_representativa': representativa['ROI'],
        'Columna_representativa': representativa['Columna'],
        'frame_peak': frame_peak,
        'score_representativa': float(representativa['score']),
    })

representantes_df = pd.DataFrame(representantes).sort_values('Cluster').reset_index(drop=True)
representantes_df.to_excel('representantes_clusters.xlsx', index=False)
print(representantes_df)

# Figura principal: una curva representativa limpia por cluster
fig, axes = plt.subplots(len(representantes_df), 1, figsize=(12, 3.2 * len(representantes_df)), sharex=True)
if len(representantes_df) == 1:
    axes = [axes]

for ax, row in zip(axes, representantes_df.itertuples(index=False)):
    ax.plot(
        analisis_plot['Frame'],
        analisis_plot[row.Columna_representativa],
        color='#440154',
        linewidth=2,
        label=f'Representativa: {row.ROI_representativa}'
    )

    if row.frame_peak is not None:
        ax.axvspan(analisis_plot['Frame'].min(), row.frame_peak, color='gray', alpha=0.10)
        ax.axvline(row.frame_peak, color='red', linestyle='--', linewidth=1.6, label=f'Peak en frame {row.frame_peak}')

    ax.axhline(0, color='black', linewidth=0.8, alpha=0.5)
    titulo = textos_cluster.get(int(row.Cluster), 'patrón de actividad')
    ax.set_title(f'Cluster {row.Cluster} — {titulo}')
    ax.set_ylabel('ΔF/F₀')
    ax.grid(alpha=0.3)
    ax.legend(loc='upper right', fontsize=8)

axes[-1].set_xlabel('Frame')
fig.suptitle('Curvas ΔF/F₀ representativas por cluster', fontsize=14, y=0.995)
plt.tight_layout()
plt.savefig('curvas_representativas_clusters.png', dpi=300, bbox_inches='tight')
plt.show()
'''

for cell in nb['cells']:
    src = ''.join(cell.get('source', []))
    if 'def obtener_frame_peak(roi_name):' in src and 'representantes_df.to_excel' in src:
        cell['source'] = new_source.splitlines(keepends=True)
        break
else:
    raise SystemExit('No se encontró la celda objetivo')

path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
print('Notebook patched')

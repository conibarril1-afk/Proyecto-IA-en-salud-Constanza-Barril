# Analisis de actividad basal/pre-peak en senales de fluorescencia celular mediante IA no supervisada

## Descripcion del proyecto

Este proyecto analiza senales de fluorescencia celular asociadas a dinamica de calcio, con enfasis en la actividad basal o pre-peak previa al peak principal de la senal.

El objetivo fue construir un pipeline computacional capaz de extraer senales desde regiones de interes (ROIs), normalizarlas mediante dF/F0, detectar eventos pre-peak, construir una matriz de caracteristicas e identificar patrones mediante inteligencia artificial no supervisada.

El analisis se realizo principalmente sobre datos propios de fluorescencia celular y se complemento con un dataset externo de senales GCaMP6m como validacion exploratoria.

## Objetivo general

Analizar la actividad basal/pre-peak en senales de fluorescencia celular mediante procesamiento de imagenes, extraccion de caracteristicas e inteligencia artificial no supervisada.

## Pipeline general

El flujo de trabajo implementado fue:

1. Seleccion de ROIs en Fiji/ImageJ.
2. Extraccion de intensidad media por frame.
3. Normalizacion mediante dF/F0.
4. Deteccion del peak principal.
5. Analisis de la ventana basal/pre-peak.
6. Extraccion de caracteristicas cuantitativas.
7. Construccion de matriz de caracteristicas por ROI.
8. Reduccion de dimensionalidad mediante UMAP.
9. Agrupamiento mediante K-means.
10. Analisis de correlacion entre actividad basal/pre-peak y peak principal.
11. Validacion exploratoria con dataset externo.

## Estructura del repositorio

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── src/
├── notebooks/
├── data/
├── results/
└── report/
```

## Requisitos de software

Se recomienda utilizar Python 3.10 o superior.

Las principales librerias utilizadas son:

- numpy
- pandas
- matplotlib
- scikit-learn
- umap-learn
- openpyxl
- scipy
- jupyter

## Instalacion

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
cd NOMBRE_DEL_REPOSITORIO
```

Crear un entorno virtual:

```bash
python -m venv venv
```

Activar el entorno virtual:

En Windows:

```bash
venv\Scripts\activate
```

En macOS/Linux:

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Datos

Los datos originales no se incluyen en el repositorio debido a su tamano.

Los archivos propios deben ubicarse en:

```text
data/raw/
```

El dataset externo debe descargarse desde:

[https://doi.gin.g-node.org/10.12751/g-node.2gxcrx/](https://doi.gin.g-node.org/10.12751/g-node.2gxcrx/)

y ubicarse en:

```text
data/external/
```

## Ejecucion del proyecto

Para reproducir el analisis principal, ejecutar el notebook:

```text
notebooks/analisis_principal.ipynb
```

Tambien se pueden ejecutar los modulos desde `src/` segun la etapa del pipeline:

```bash
python src/preprocessing.py
python src/feature_extraction.py
python src/clustering.py
python src/correlation_analysis.py
```

El analisis del dataset externo se encuentra en:

```bash
python src/external_dataset_analysis.py
```

## Resultados

Los resultados generados se almacenan en:

```text
results/figures/
results/tables/
```

Entre los principales resultados se incluyen:

- curvas normalizadas dF/F0;
- matriz de caracteristicas por ROI;
- proyeccion UMAP;
- clusters obtenidos mediante K-means;
- curvas representativas por cluster;
- correlaciones entre actividad pre-peak y peak principal;
- analisis exploratorio con dataset externo.

## Informe

El informe final se encuentra en:

```text
report/main.tex
report/referencias.bib
report/informe_final.pdf
```

El informe fue redactado en LaTeX y contiene la descripcion del problema, solucion propuesta, implementacion, metodologia experimental, resultados, analisis critico, conclusiones y trabajo futuro.

## Principales hallazgos

El analisis mostro que la actividad basal/pre-peak no fue homogenea entre las ROIs. Se identificaron tres patrones principales:

- actividad frecuente y sostenida de baja amplitud;
- eventos menos frecuentes, pero de mayor amplitud;
- actividad leve/moderada predominante.

Ademas, se observo una correlacion positiva fuerte entre la amplitud de los eventos pre-peak y la magnitud del peak principal, tanto en los datos propios como en el dataset externo. Esta relacion se interpreta como exploratoria y no causal.

## Limitaciones

El proyecto presenta limitaciones asociadas al numero reducido de registros propios, seleccion manual de ROIs, ausencia de etiquetas biologicas confirmadas y diferencias entre los datos propios y el dataset externo.

## Trabajo futuro

Como trabajo futuro se propone:

- aumentar el numero de registros y ROIs;
- automatizar segmentacion con CaImAn o Suite2p;
- incorporar correccion de movimiento, drift y fotoblanqueamiento;
- validar los clusters con informacion biologica adicional;
- explorar modelos mas avanzados como autoencoders o redes neuronales supervisadas si se cuenta con etiquetas confiables;
- aplicar bootstrap o Monte Carlo para evaluar robustez.

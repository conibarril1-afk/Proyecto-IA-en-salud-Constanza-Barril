# Datos del proyecto

Los datasets completos no se incluyen en este repositorio debido a su tamano.

## Datos propios

Los registros originales de fluorescencia deben ubicarse manualmente en:

```text
data/raw/
```

Estos archivos corresponden a senales de fluorescencia celular asociadas a indicadores como GCaMP, GCaMP6 y jRGECO.

En esta version del proyecto, el material de trabajo interno y los archivos fuente pequenos se organizan en:

```text
data/raw/interno/
```

Eso incluye CSV y ODS exportados desde Fiji/ImageJ, asi como archivos de entrada usados para generar las tablas y figuras del analisis interno.

## Dataset externo

El dataset externo utilizado corresponde a registros publicos de calcium imaging con GCaMP6m en corteza auditiva de raton.

Enlace del dataset externo:

[https://doi.gin.g-node.org/10.12751/g-node.2gxcrx/](https://doi.gin.g-node.org/10.12751/g-node.2gxcrx/)

Para reproducir el analisis externo, descargar los archivos correspondientes y ubicarlos en:

```text
data/external/
```

En el repositorio local se organizo como:

```text
data/external/dataset_publico/
```

Esa carpeta contiene la estructura del dataset externo, el manifest `overview_all.csv` y material de apoyo.

## Resultados procesados

Los resultados generados por los scripts se guardan en:

```text
results/figures/
results/tables/
```

Las tablas y figuras incorporadas al repositorio quedaron separadas en resultados internos y externos para facilitar la revision.

# P10 · Concordancia entre métodos de explicabilidad

**Revista destino:** Computer Science AGH
**Línea:** A · **GPU:** Baja · **Días asignados:** 20-21 ago

## Estado
- [ ] Ficha de revista completa (JOURNAL.md)
- [x] Datos descargados (data/raw/) — OULAD, Dropout, German Credit, Rice
- [ ] Experimento ejecutado (día 1)
- [ ] Redacción y figuras (día 2)
- [ ] Endurecimiento: DOIs verificados
- [ ] Endurecimiento: revisión adversarial ronda 1
- [ ] Endurecimiento: revisión adversarial ronda 2
- [ ] Revisión cruzada
- [ ] Repositorio en GitHub
- [ ] Publicado en Zenodo (DOI)
- [ ] Carta de presentación y declaraciones
- [ ] Entregado al responsable académico

## Protocolo

**Revista destino:** Computer Science (AGH University of Science and Technology)
**Fecha de inicio:** 18/08
**Responsable:** Juan (línea A)

### Pregunta de investigación
¿SHAP, LIME y la importancia por permutación coinciden al identificar las variables relevantes, y esa coincidencia se mantiene al cambiar de modelo, de partición y de dominio?

### Hipótesis
La concordancia es alta entre particiones del mismo modelo (τ > 0,8) pero baja entre métodos distintos (τ < 0,6): la conclusión de un análisis de explicabilidad depende del método elegido.

### Variables
- Independientes: modelo (Random Forest, Gradient Boosting, Regresión Logística), método de explicabilidad (SHAP, LIME, importancia por permutación), dataset, fold
- Dependientes: τ de Kendall entre rankings de variables
- Controladas: preprocesamiento (idéntico para los 3 modelos)

### Diseño
- Condiciones experimentales: 3 modelos × 4 datasets × 10 folds × 3 métodos = 360 rankings
- Repeticiones por condición: 10 folds
- Semilla aleatoria: 42
- Validación: TreeSHAP exacto para modelos de árbol; submuestreo para LIME; documentar explícitamente la agregación de LIME (es local por diseño)

### Prueba estadística
τ de Kendall entre pares de rankings (entre folds, entre métodos, entre modelos) con IC bootstrap; ANOVA sobre τ.
- Tamaño del efecto a reportar: τ de Kendall promedio por eje de comparación

### Criterio de interés
- Si la hipótesis se confirma: elegir el método de explicabilidad cambia materialmente la conclusión — riesgo metodológico que la comunidad debe declarar.
- Si se refuta: los tres métodos son razonablemente robustos entre sí, lo que respalda su uso intercambiable.

### Datasets
| Nombre | Fuente | Licencia | Verificado |
|--------|--------|----------|------------|
| OULAD | UCI Machine Learning Repository (id 349) | CC BY 4.0 | Sí — descargado 18/08, 8 archivos, se usará principalmente `studentInfo.csv` (target: `final_result`) |
| Predict Students' Dropout and Academic Success | UCI (id 697) | CC BY 4.0 | Sí — descargado 18/08, `data.csv` |
| Statlog German Credit Data | UCI (id 144) | CC BY 4.0 | Sí — descargado 18/08, `german.data` |
| Rice (Cammeo and Osmancik) — dominio agrícola | UCI (id 545) | CC BY 4.0 | Sí — descargado 18/08, `Rice_Cammeo_Osmancik.arff` |

Nota: `studentVle.csv` de OULAD (clickstream, ~450 MB) no se usará en este estudio tabular — el target y las features vienen de `studentInfo.csv`.

### Citas obligatorias de la revista destino
1. (pendiente — extraer de trabajos sobre aprendizaje automático, interpretabilidad y metodología experimental publicados en Computer Science AGH)
2.
3.

## Bitácora

## 18/08 - Montaje
- Hecho: estructura de carpetas creada, plantilla de figuras copiada, repositorio Git inicializado.
- Bloqueado en: pendiente ficha de revista y descarga de datos.
- Siguiente: completar JOURNAL.md y descargar dataset.
- Tiempo de computo consumido: 0h

## 18/08 - Día 1: descarga de datos
- Hecho: `01_download.py` escrito y ejecutado. Los 4 datasets descargados desde UCI ML Repository (OULAD id 349, Dropout id 697, German Credit id 144, Rice id 545 como el dataset agrícola). Todos con licencia CC BY 4.0.
- Bloqueado en: nada.
- Siguiente: `02_preprocess.py` — codificación de categóricas, imputación, escalado (mismo preprocesamiento para los 3 modelos).
- Tiempo de computo consumido: ~5 min (descarga)

## 18/08 - Día 1: preprocesamiento
- Hecho: `02_preprocess.py` escrito y ejecutado sobre los 4 datasets. Decisión metodológica documentada: se binarizan las 4 variables objetivo a "riesgo" vs "no riesgo" (OULAD: Fail/Withdrawn vs Pass/Distinction; Dropout: Dropout vs Enrolled/Graduate; German Credit y Rice ya eran binarios) para que la comparación de τ de Kendall entre métodos de explicabilidad no dependa de la complejidad adicional de atribución multiclase — pendiente justificar esto explícitamente en la sección de metodología del manuscrito. Balances de clase razonables en los 4 (entre 30% y 57% de clase positiva). Salidas en `data/processed/` (no versionado en git, regenerable con el script).
- Bloqueado en: nada.
- Siguiente: `03_experiment.py` — 3 modelos × 4 datasets × 10 folds, generar atribuciones con SHAP, LIME e importancia por permutación.
- Tiempo de computo consumido: ~1 min

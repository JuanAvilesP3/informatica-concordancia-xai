# P10 · Concordancia entre métodos de explicabilidad

**Revista destino:** Computer Science AGH
**Línea:** A · **GPU:** Baja · **Días asignados:** 20-21 ago

## Estado
- [ ] Ficha de revista completa (JOURNAL.md)
- [x] Datos descargados (data/raw/) — OULAD, Dropout, German Credit, Rice
- [x] Experimento ejecutado (día 1) — 360 combinaciones, `results/tables/attributions_long.csv`
- [x] Figuras generadas (4/4) — falta redacción del manuscrito (día 2)
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
- Hecho: `02_preprocess.py` escrito y ejecutado sobre los 4 datasets. Primera versión binarizaba los 4 targets a "riesgo"/"no riesgo"; **revertido a pedido del responsable** — se mantienen las clases originales: OULAD con 4 (Pass, Fail, Withdrawn, Distinction), Dropout con 3 (Dropout, Enrolled, Graduate); German Credit y Rice ya eran binarios de origen. Balances de clase razonables en los 4, sin clases degeneradas. Salidas en `data/processed/` (no versionado en git, regenerable con el script).
- Bloqueado en: nada.
- Siguiente: `03_experiment.py` — 3 modelos × 4 datasets × 10 folds, generar atribuciones con SHAP, LIME e importancia por permutación. **Nota para el diseño:** OULAD y Dropout ahora son multiclase, así que SHAP/LIME producirán una atribución por clase — hay que decidir y documentar explícitamente cómo se agrega/reporta eso (mismo principio que la ficha exige para la agregación de LIME).
- Tiempo de computo consumido: ~1 min

## 18-19/08 - Día 1: experimento completo
- Hecho: `03_experiment.py` corrido con éxito sobre los 4 datasets, 10 folds, 3 modelos, 3 métodos = 360 combinaciones (13,770 filas de rankings de variables) en `results/tables/attributions_long.csv`. Tres bugs reales encontrados y corregidos en el camino:
  1. Random Forest sin límite de profundidad hacía que SHAP tardara >10 min por fold en OULAD; con `max_depth=12` bajó a ~150-215s. Documentar en limitaciones: es una regularización estándar, no cambia el tamaño de los datos.
  2. XGBoost requiere `y` numérico; se codificó con `LabelEncoder` compartido entre los 3 modelos.
  3. XGBoost prohíbe `<`, `[`, `]` en nombres de columna (OULAD tiene la categoría `age_band="55<="`); se sanean los nombres al cargar.
  4. Decisión de diseño confirmada con el responsable: NO se redujo el tamaño de ningún dataset (la ficha solo autoriza submuestreo para el cálculo de LIME, no para el entrenamiento); en su lugar se aplicó el mismo principio a SHAP y a permutation_importance vía `--eval-max-samples` (se calculan sobre una submuestra del fold de prueba, nunca se reduce el fold de entrenamiento).
- Bloqueado en: nada.
- Siguiente: `04_stats.py` — τ de Kendall entre rankings (por fold, por método, por modelo), ANOVA, IC bootstrap.
- Tiempo de computo consumido: ~50 min (mayormente OULAD)

## 19/08 - Día 1: estadística (hallazgo central confirmado)
- Hecho: `04_stats.py` corrido. Resultado limpio en los 4 datasets: τ entre folds (mismo método) alto (0.54–0.89), τ entre métodos (mismo modelo) bajo (0.28–0.47), τ entre modelos (mismo método) medio (0.50–0.55). Confirma la hipótesis del artículo: la elección del método de explicabilidad pesa más que la elección del modelo. ANOVA de dos factores (dataset × eje) significativo en ambos factores y su interacción (p < 0.001). Archivos: `kendall_tau_detail.csv` (2340 comparaciones), `kendall_tau_summary.csv`, `anova_tau.csv`.
- Bloqueado en: nada.
- Siguiente: `05_figures.py` (mapa de calor de τ, cajas por eje, top-10 paralelo, τ por dataset — ver ficha sección 6).
- Tiempo de computo consumido: ~1 min

## 19/08 - Día 1: figuras (cierre de Fase 1 para este artículo)
- Hecho: `05_figures.py` corrido — 4 figuras generadas en `results/figures/` (PDF+PNG), revisadas visualmente. Fig. 1 (la que sostiene el argumento) muestra con claridad el bloque de alta concordancia intra-método vs. la baja concordancia entre métodos. Fig. 2 y Fig. 4 confirman el patrón en los 4 datasets. Fig. 3 (top-10 en columnas paralelas) funciona pero varios nombres de variable quedan truncados — **pendiente para Fase 2 (figuras finales)**: revisar legibilidad de etiquetas largas.
- Bloqueado en: nada. **P10 tiene su versión completa: experimento, estadística y figuras. Falta la redacción del manuscrito (día 2) y luego Fase 2 (verificación de referencias + revisión adversarial).**
- Siguiente: redactar `paper/main.tex` con los resultados ya generados, o pasar a otro artículo de la línea A.
- Tiempo de computo consumido: ~1 min

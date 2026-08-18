# P10 · Concordancia entre métodos de explicabilidad

**Revista destino:** Computer Science AGH
**Línea:** A · **GPU:** Baja · **Días asignados:** 20-21 ago

## Estado
- [ ] Ficha de revista completa (JOURNAL.md)
- [ ] Datos descargados (data/raw/)
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
| OULAD | Open University Learning Analytics Dataset | Verificar | No |
| Predict Students' Dropout and Academic Success | UCI | Verificar | No |
| Statlog German Credit Data | UCI | Verificar | No |
| Cuarto dataset ambiental/agrícola tabular | UCI (por elegir) | Verificar | No |

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

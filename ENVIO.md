# Ficha de Instrucciones de Envío — Paper P10
**Proyecto:** Concordancia entre Métodos de Explicabilidad (XAI)  
**Marco Institucional:** FIE-ESPOCH 2026 (Planificación Oficial de Producción Científica)  
**Fecha de Actualización:** 28 de septiembre de 2026  

---

## 1. Identificación de la Revista y Política Editorial
- **Revista destino:** *Informatica: An International Journal of Computing and Informatics*
- **Entidad editora:** Slovenian Society Informatika (Slovensko društvo Informatika), Liubliana, Eslovenia.
- **ISSN:** 0350-5596 (Impreso) | 1854-3871 (En línea).
- **Indexación oficial:** Scopus (SJR 0.28, Q3/Q4), DOAJ, dblp computer science bibliography, EBSCO, Google Scholar.
- **Portal oficial de envíos (OJS):** [https://www.informatica.si/index.php/informatica/about/submissions](https://www.informatica.si/index.php/informatica/about/submissions)
- **Editor en Jefe:** Prof. Dr. Matjaž Gams (`editor-in-chief@informatica.si`), Jožef Stefan Institute & University of Ljubljana.
- **Modalidad de revisión por pares:** **Simple Ciego (Single-Blind Peer Review)**. La política editorial oficial de *Informatica* establece que los revisores conocen la identidad y filiación institucional de los autores; el manuscrito no debe ser anonimizado.
- **Sección / Track en OJS:** **Regular Research Paper — Track Normal (N)** (revisión regular sin recargo).
- **Cobra APC (Article Processing Charges)?:** **NO ($0 USD)**. Revista 100% Diamond Open Access, patrocinada por la Agencia Eslovena de Investigación e Innovación (ARIS). Existe una opción voluntaria "Ultra-Fast" con tarifa, pero el Track Normal (N) estándar es totalmente libre de costo ($0 USD). Evidencia documental en `JOURNAL.md`.

---

## 2. Metadatos del Manuscrito (para carga en el formulario OJS)

### Título del artículo:
```text
Agreement Among Explainability Methods: A Cross-Model, Cross-Domain Study
```

### Resumen en inglés (Abstract para OJS):
```text
Feature-attribution methods such as SHAP, LIME, and permutation importance are routinely used to justify machine learning decisions, on the implicit assumption that they largely agree on which features matter. We test that assumption directly: across four tabular datasets covering three domains (two educational, one financial, one agricultural), three model families (random forest, gradient boosting, logistic regression), and ten cross-validation folds, we compute 360 feature-importance rankings and compare them pairwise using Kendall's tau along three axes: between folds of the same method, between methods applied to the same model, and between models explained by the same method. Agreement between folds of the same method is consistently high (mean tau between 0.54 and 0.89, above 0.75 for three of the four datasets), but agreement between different explanation methods applied to the same model is substantially and significantly lower (mean tau between 0.28 and 0.47), with model-to-model agreement for a fixed method falling in between (0.50 to 0.55). Crucially, agreement drops even further (e.g., tau=0.055 on German Credit) when restricted to the top-10 features actually reported to stakeholders. A two-way ANOVA confirms both the dataset and the comparison-axis effects are highly significant (p < 10^-120), with a significant interaction. Which explanation method is chosen matters more than which model is explained, and reporting the output of a single attribution method without checking it against another can misrepresent which features a model relies on.
```

### Resumen en esloveno (Povzetek obligatorio según directrices de Informatica):
```text
Metode za razlago napovedi modelov strojnega učenja, kot so SHAP, LIME in permutacijska pomembnost, se pogosto uporabljajo ob predpostavki, da se njihove ocene pomembnosti atributov medsebojno ujemajo. V tej empirični študiji na štirih tabelaričnih naborih podatkov, treh družinah modelov in desetih rezinah prečnega preverjanja neposredno merimo skladnost med metodami s pomočjo Kendallovega koeficienta tau. Rezultati kažejo, da je stabilnost posamezne metode visoka, medtem ko je ujemanje med različnimi metodami na istem modelu bistveno nižje, kar poudarja potrebo po hkratni uporabi več metod razložljivosti v praksi.
```

### Palabras clave (Keywords):
```text
Explainable Artificial Intelligence (XAI), Feature Attribution, Concordance Analysis, Kendall's tau, Tabular Machine Learning, Model Interpretability, SHAP, LIME
```

---

## 3. Autores y Filiación Institucional Oficial (Orden Estricto)
1. **Italo Javier Tenempaguay-Granizo** (*Primer Autor y Autor de Correspondencia*)
   - *Filiación:* Facultad de Informática y Electrónica, Escuela Superior Politécnica de Chimborazo (ESPOCH), Panamericana Sur km 1 1/2, Riobamba EC060155, Ecuador.
   - *Correo electrónico:* `italo.tenempaguay@espoch.edu.ec`
   - *ORCID:* [0009-0001-5753-4279](https://orcid.org/0009-0001-5753-4279)
2. **Juan Pablo Aviles-Esparza** (*Coautor*)
   - *Filiación:* Facultad de Informática y Electrónica, Escuela Superior Politécnica de Chimborazo (ESPOCH), Panamericana Sur km 1 1/2, Riobamba EC060155, Ecuador.
   - *Correo electrónico:* `juan.aviles@espoch.edu.ec`
   - *ORCID:* [0009-0007-0058-8069](https://orcid.org/0009-0007-0058-8069)
3. **Isaac David Torres-Paredes** (*Coautor y Tutor Académico*)
   - *Filiación:* Facultad de Informática y Electrónica, Escuela Superior Politécnica de Chimborazo (ESPOCH), Panamericana Sur km 1 1/2, Riobamba EC060155, Ecuador.
   - *Correo electrónico:* `isaac.torres@espoch.edu.ec`
   - *ORCID:* [0009-0001-7057-9316](https://orcid.org/0009-0001-7057-9316)

---

## 4. Archivos a Subir en la Plataforma OJS (Paso a Paso)
- **Paso 2 de OJS (Upload Submission / Archivo de Envío Principal):**
  - Subir: `P10_Informatica_manuscript.pdf` (12 páginas compiladas bajo la plantilla oficial `informat.sty` en A4, incluye resumen en esloveno y figuras vectoriales/raster 300 DPI).
- **Paso 4 de OJS (Upload Supplementary Files / Archivos Complementarios):**
  1. `cover_letter.md` (Carta formal dirigida al Editor en Jefe Prof. Matjaž Gams).
  2. `declaraciones.md` (Declaraciones de roles CRediT, declaración de ética de IA según COPE/WAME, disponibilidad de datos en Zenodo y ausencia de conflictos).
  3. `P10_Informatica_paquete_envio.zip` (Paquete comprimido con el código fuente completo en LaTeX: `main.tex`, `refs.bib`, `informat.sty`, subcarpeta `figures/` con las 12 figuras, `README.md`, `requirements.txt`).

---

## 5. Revisores Pares Sugeridos (3 Expertos Internacionales en XAI)
1. **Prof. Dr. Przemysław Biecek**  
   - *Filiación:* Faculty of Mathematics, Informatics and Mechanics, University of Warsaw & Warsaw University of Technology, Varsovia, Polonia.  
   - *Correo electrónico:* `p.biecek@mimuw.edu.pl`  
   - *Especialidad:* Métodos de explicabilidad en modelos predictivos (autor del paquete DALEX, auditoría empírica de XAI tabular).
2. **Prof. Dr. Marko Robnik-Šikonja**  
   - *Filiación:* Faculty of Computer and Information Science, University of Ljubljana, Liubliana, Eslovenia.  
   - *Correo electrónico:* `marko.robniksikonja@fri.uni-lj.si`  
   - *Especialidad:* Selección de características, robustez de explicaciones en aprendizaje automático de caja negra (investigador referente en Eslovenia).
3. **Prof. Dr. Wojciech Samek**  
   - *Filiación:* Fraunhofer Heinrich Hertz Institute (HHI) / Technical University of Berlin, Berlín, Alemania.  
   - *Correo electrónico:* `wojciech.samek@hhi.fraunhofer.de`  
   - *Especialidad:* Benchmarking y consistencia en métodos de atribución post-hoc (LRP, XAI cuantitativo).

---

## 6. Enlaces de Reproducibilidad y Datos Abiertos
- **Repositorio público en GitHub:** [https://github.com/JuanAvilesP3/informatica-concordancia-xai.git](https://github.com/JuanAvilesP3/informatica-concordancia-xai.git)
- **Depósito permanente en Zenodo:** [https://doi.org/10.5281/zenodo.23005761](https://doi.org/10.5281/zenodo.23005761) (DOI: `10.5281/zenodo.23005761`).

---

## 7. Lista de Chequeo Previa al Envío (Directrices FIE-ESPOCH 2026)
- [x] Manuscrito compilado exactamente a 12 páginas según las directrices de *Informatica*.
- [x] Incluye resumen obligatorio en esloveno (*Povzetek*) en el comando `\abstractSi{...}`.
- [x] 12 figuras de alta resolución (vectoriales y 300 DPI) alojadas en la subcarpeta `figures/` e insertadas como `figures/figX...`.
- [x] Ninguna figura generada mediante IA de imágenes (regla dura de la Guía Metodológica).
- [x] Cero errores de compilación en `pdflatex` y `bibtex`.
- [x] 18 referencias bibliográficas con DOI activo verificado, incluyendo 3 citas de contexto de la revista *Informatica* (*Vlahek 2024, Li 2025, Yao 2025*).
- [x] Filiación institucional corregida con acentuación oficial LaTeX (`Polit\'ecnica`).
- [x] Corrección matemática del ordenamiento por longitud descendente en LIME (`key=len, reverse=True`) en `src/03_experiment.py` para prevenir colisiones de subcadenas.
- [x] Argumentación teórica de robustez ante escalamiento global en árboles y discretización continua de LIME incorporada en sección 2.
- [x] Principio de exclusividad estricta verificado: el manuscrito no está enviado a ninguna otra revista.

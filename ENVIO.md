# Ficha de Instrucciones de Envío — Paper P10

## 1. Identificación de la Revista y Política Editorial
- **Revista destino:** *Informatica: An International Journal of Computing and Informatics*
- **Entidad editora:** Slovenian Society Informatika (Slovensko društvo Informatika), Liubliana, Eslovenia.
- **ISSN:** 0350-5596 (Impreso) | 1854-3871 (En línea).
- **Indexación oficial:** Scopus (SJR 0.28, Q3/Q4), DOAJ, dblp computer science bibliography, EBSCO, Google Scholar.
- **Portal oficial de envíos (OJS):** [https://www.informatica.si/index.php/informatica/about/submissions](https://www.informatica.si/index.php/informatica/about/submissions)
- **Modalidad de revisión por pares:** **Simple Ciego (Single-Blind Peer Review)**. La política editorial oficial de *Informatica* establece que los revisores conocen la identidad y filiación de los autores; no se anonimiza el manuscrito.
- **Sección / Track en OJS:** **Regular Research Paper — Track Normal (N)** (revisión regular sin recargo de urgencia).
- **Cobra APC (Article Processing Charges)?:** **NO ($0 USD)**. Revista 100% Diamond Open Access sin cobro por procesamiento ni publicación.

---

## 2. Metadatos del Manuscrito (para carga en el formulario OJS)

### Título del artículo:
```text
Agreement Among Explainability Methods: A Cross-Model, Cross-Domain Study
```

### Resumen en inglés (Abstract):
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
1. **Italo Javier Tenempaguay-Granizo** (*Autor de correspondencia*)
   - *Filiación:* Facultad de Informática y Electrónica, Escuela Superior Politécnica de Chimborazo (ESPOCH), Panamericana Sur km 1 1/2, Riobamba EC060155, Ecuador.
   - *Correo electrónico:* `italo.tenempaguay@espoch.edu.ec`
   - *ORCID:* [0009-0001-5753-4279](https://orcid.org/0009-0001-5753-4279)
2. **Juan Pablo Aviles-Esparza**
   - *Filiación:* Facultad de Informática y Electrónica, Escuela Superior Politécnica de Chimborazo (ESPOCH), Panamericana Sur km 1 1/2, Riobamba EC060155, Ecuador.
   - *Correo electrónico:* `juan.aviles@espoch.edu.ec`
   - *ORCID:* [0009-0007-0058-8069](https://orcid.org/0009-0007-0058-8069)
3. **Isaac David Torres-Paredes**
   - *Filiación:* Facultad de Informática y Electrónica, Escuela Superior Politécnica de Chimborazo (ESPOCH), Panamericana Sur km 1 1/2, Riobamba EC060155, Ecuador.
   - *Correo electrónico:* `isaac.torres@espoch.edu.ec`
   - *ORCID:* [0009-0001-7057-9316](https://orcid.org/0009-0001-7057-9316)

---

## 4. Archivos a Subir en la Plataforma OJS (Paso a Paso)
- **Paso 2 de OJS (Upload Submission / Archivo de Envío Principal):**
  - Subir: [`paper/P10_Informatica_manuscript.pdf`](file:///c:/Users/Juan/Desktop/PAPERS/10-agh-concordancia-xai/paper/P10_Informatica_manuscript.pdf) (12 páginas compiladas bajo la plantilla oficial `informat.sty` en A4, incluye Povzetek y figuras vectoriales).
- **Paso 4 de OJS (Upload Supplementary Files / Archivos Complementarios):**
  1. `paper/cover_letter.md` (Carta formal dirigida al Editor en Jefe Prof. Matjaž Gams).
  2. `paper/declaraciones.md` (Declaraciones de Autoría CRediT, declaración ética COPE sobre uso de IA, disponibilidad de datos en Zenodo y ausencia de conflictos de interés).
  3. Paquete comprimido con fuentes completas de LaTeX: [`paquetes_envio/P10_Informatica_paquete_envio.zip`](file:///c:/Users/Juan/Desktop/PAPERS/paquetes_envio/P10_Informatica_paquete_envio.zip) (contiene `main.tex`, `refs.bib`, `informat.sty`, subcarpeta `figures/` con las 12 figuras vectoriales y raster de 300 DPI, `cover_letter.md`, `declaraciones.md`, `README.md`).

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
- **Depósito de datos y código en Zenodo:** [https://doi.org/10.5281/zenodo.22907630](https://doi.org/10.5281/zenodo.22907630) (DOI: `10.5281/zenodo.22907630`).

---

## 7. Lista de Chequeo Previa al Envío (Checklist)
- [x] Manuscrito compilado exactamente a 12 páginas según directrices de *Informatica*.
- [x] Incluye resumen en esloveno (*Povzetek*) en `bstractSi{...}`.
- [x] Figuras en alta resolución alojadas en la subcarpeta `figures/` e insertadas como `figures/figX...`.
- [x] Cero errores de compilación en `pdflatex` y `bibtex`.
- [x] 18 referencias bibliográficas con DOI activo verificado, incluyendo 3 citas de contexto de la revista *Informatica* (*Vlahek 2024, Li 2025, Yao 2025*).
- [x] Filiación institucional corregida con acentuación oficial LaTeX (`Polit\'ecnica`).
- [x] Argumentación teórica de robustez ante escalamiento global en árboles y discretización continua de LIME incorporada en sección 2.

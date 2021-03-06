## Health inequality metric: deterioration-allocation framework (DAindex)
This repo implements a **DA-AUC** (deterioration-allocation area under curve) for quantifying **inequality** between patient groups (a) embedded in datasets; or (b) induced by AI models. This is analogous to ROC-AUC for assessing performance of prediction models.

## Install `DAindex` python package
```bash
pip install DAindex
```

## Tutorials
- Check this tutorial: [DAindex-tutorial.ipynb](./DAindex-tutorial.ipynb) for basic use of DAindex.
- More tutorials will be added, including those for replicating studies on HiRID and MIMIC datasets.

## Reference
[Honghan Wu](https://knowlab.github.io/), Minhong Wang, Aneeta Sylolypavan, Sarah Wild. “Quantifying Health Inequalities Induced by Data and AI Models”. Accepted by IJCAI-ECAI2022 (April 2022). [slides](https://www.ucl.ac.uk/research-it-services/sites/research_it_services/files/quantifying_health_inequalities_induced_by_data_and_ai_models_0.pdf), [recording](https://web.microsoftstream.com/video/568b2e88-5c21-466e-9bbf-63274048161d), [arxiv](https://arxiv.org/abs/2205.01066).

## Introduction (TL; DR)
We define and quantify health inequalities in a generic resource allocation scenario using a so-called allocation-deterioration framework. The basic idea is to define two indices: allocation index and deterioration index. The allocation index is (to be derived) from the AI model of interest. Conceptually, AI models are abstracted as `resource allocators`, such as predicting the probability of Intensive Care Unit admission. Note that the models themselves do not need to be particularly designed to allocate resources, for example, it could be risk prediction of cardiovascular disease (CVD) among people with diabetes. Essentially, a resource allocator is a computational model that takes patient data as input and outputs a (normalised) score between 0 and 1. We call this score the allocation index. Deterioration index is a score between 0 and 1 to measure the deterioration status of patients. It can be derived from an objective measurement for disease prognosis (i.e., *a marker of prognosis* in epidemiology terminology), such as extensively used comorbidity scores or biomarker measurements like those for CVDs.

![Figure 1](imgs/fig1.png)

When we have the two indices, each patient can then be represented as a point in a two-dimensional space of *allocation index*, *deterioration index*. A group of patients is then translated into a set of points in the space, for which a regression model could be fitted to approximate as a curve in the space. The same could be done for another group. *The area between the two curves is then the deterioration difference between their corresponding patient groups, quantifying the inequalities induced by the `allocator`, i.e., the AI model that produces the allocation index*. The curve with the larger area under it represents the patient group which would be unfairly treated if the allocation index was to be used in allocating resources or services: a patient from this group would be deemed healthier than a patient from another group who is equally ill. The rest of this section gives technical details of realising key components of this conceptual framework.

## Contact
honghan.wu@ucl.ac.uk

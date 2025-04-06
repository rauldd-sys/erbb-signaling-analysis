# Report
**Authors**
Raul Duran de Alba
Denys Buryi

## Introduction

The ErbB (HER) signaling pathway is a critical regulator of cell proliferation and survival, with particular relevance in breast cancer. Overexpression of transmembrane tyrosine kinase (ERBB2) specifically is connected with adverse prognosis, and so it is targeted by monoclonal antibody trastuzumab in adition to the primary therapy. Unfortunatelly some cancer cells develop the *de novo* resistance to this antibody. In the attached publication, the authors presented a Boolean network approach to model ErbB dynamics and experimental testing of the resulting network in order to try to find alternative therapeutic targets for such *de novo* trastuzumab resistant cancer cells. 
Our project builds on that work by first reproducing the original Boolean network framework to confirm the published results regarding stable states and attractors. We then extend that analysis using new computational modules, such as phenotype control proposed by [Benes et al., 2023](https://dl.acm.org/doi/abs/10.1007/978-3-031-42697-1_2). 

## Original paper 

The authors chose a specific cell line with high ERBB2 expression and resistance to trastuzumab treatment at the same time. 
The authors constructed a network based on literature, linking ERBB receptor signaling to the G1/S transition of the cell cycle (pRB phosphorylation as the main readout).

They conducted in silico knockdowns of network proteins to predict which knockdowns would inhibit G1/S progression.

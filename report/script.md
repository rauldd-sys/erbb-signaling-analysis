## Title

Hello everyone, today we’ll present our project on modeling the ERBB receptor signaling network in breast cancer, specifically focusing on G1/S transition and de novo resistance to trastuzumab.

## Slide 1: Background

(Keep text minimal—short bullet points.)

- HER2 (ERBB2) Overexpression

- Trastuzumab Resistance

- Need for Alternative Targets


In breast cancer, the overexpression of ERBB2, also called HER2, often signals aggressive disease. Trastuzumab improves outcomes, but many patients show de novo or acquired resistance, creating a major clinical challenge. Hence, we need new therapeutic strategies.

**the G1/S transition is effectively the cell’s “commitment point” to begin DNA replication and MAKE MORE CANCERE CELLS**

## Slide 2: Objective

Our objective is to model how ERBB signaling drives the G1/S transition and use that network to find key nodes that might overcome resistance. Specifically, we want to see how well a Boolean approach can predict which knockdowns or inhibitors will block proliferation.

## Slide 3, 4: Paper (Sahin et al.)

    Literature-based Boolean network

    In vitro knockdowns

    c-MYC identified

    De novo resistance focus

    Cell Line: HCC1954 (Resistant)

    Boolean Network: 18 Proteins

    Knockdowns & pRB

    Refinement

The authors chose HCC1954, a HER2-overexpressing cell line that was nevertheless trastuzumab-resistant cell line (reminder, the drug works through HER2). They built a Boolean model of 18 proteins, focusing on pRB phosphorylation as a G1/S marker. 

The reason why they built the model this way was based on the rules derived from the literature. They then performed in vitro and in vivo knockdown experiments and compared the results to estimate the performance of the model. As a result they identified one rule that was too loose: CycD1 rule
They concluded that c-MYC is a candidate target in treating HER2-resistant breast cancer. This guides our work on alternative targets.

## Slide 5: Our Project Steps

    Reproduced Paper’s Boolean Model

    Compared Predicted vs. Experimental

    Explored Key Discrepancy: Cyclin E1

    Extended Analysis for Future Work

In our project, we reproduced much of the paper’s workflow. First, we implemented the original Boolean network with the same rules. We set ERBB family receptors and IGF1R as the input layer, with downstream signals feeding into cyclin D1, c-MYC, and ER-α for control of pRB phosphorylation. Analyzing stable states revealed three main outcomes, mirroring the original paper’s approach. We also ran simulated knockouts to compare with the authors’ data.

## Slide 6: Validation and Discrepancies

After, we simulated the knockouts (ER-α, c-MYC, Cyclin D1, etc.) and compared the predicted pRB status to the experimental outcomes, we found that the original network incorrectly allowed partial cell-cycle progression even without ER-α or c-MYC. In reality, those knockdowns abolish G1/S entry. This mismatch pinpointed cyclin D1’s oversimplified logic, prompting us to tighten its rule to require both ER-α and c-MYC signals. That change resolved the discrepancy.

## Slide 7: Permanent Perturbations

In this step, we tested permanent ON/OFF for each network component to see which combinations would enforce a G1/S arrest. We focused on knockout strategies targeting c-MYC or ER-α, and observed synergy when inhibiting AKT1 and MEK1 together. Some triple combos blocked the cycle consistently, highlighting potential multi-target therapies.

## Slide 8: LogicGep

Originally we wanted to use LogicGep approach to refine the Boolean rules further, but it required time-series data that we couldn't find. So took more modern literature on the network interactions, similarly to what the authors did originally. We expanded the original network by integrating a p53 stress axis. Our adjustments introduced new potential interactions and increased the model’s sensitivity to certain knockdowns. Of course to confirm the validity of these we need in vivo experiments.

## Slide 9: Conclusions

To wrap up, modeling and experimental validation are both necessary for understanding de novo trastuzumab resistance. Further refinement of Boolean rules might incorporate unmodeled feedback loops—especially for Cyclin E1. Finally, c-MYC inhibition remains a promising avenue to tackle cells that don’t respond to trastuzumab. Now we will be happy to answer your questions.


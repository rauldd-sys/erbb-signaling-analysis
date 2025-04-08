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

In this step, we tested permanent ON/OFF for each network component to see which combinations would enforce a G1/S arrest. Stand alone activations and inhibitions only yielded that the knock out of c-Myc produced sufficient cell cycle arrest in the refined model. We focused on knockout strategies targeting c-MYC or ER-α, and observed synergy when inhibiting AKT1 and MEK1 together. Some triple combos blocked the cycle consistently, highlighting potential multi-target therapies.

## Slide 8: LogicGep

Inspired by a new technique called LogicGep, we attempted a deeper refinement of the model’s logic. Since we didn’t have the live cell data needed to fully run LogicGep’s algorithm, we manually added a few plausible rules from the literature. Similarly to what the authors did originally. We expanded the original network by integrating a p53 stress response. Key refinements include: direct EGF dependence for Cyclin D1, CDK4 requirement for Cyclin E1 to reflect sequential cell cycle regulation, dependency of c-MYC on ER-α, and introduction of p53-mediated stress response activated by absent growth signals. 
Our adjustments introduced new potential interactions and increased the model’s sensitivity to certain knockdowns. Of course to confirm the validity of these we need in vivo experiments.

We reasoned that if a cell has high p53 (say, from stress or damage), it should not be happily cycling via ER-α. So in our extended model, p53 can shut down ER-α signaling. We also made Cyclin E a bit harder to get – now the model insists that Cyclin D/CDK4 must be active for Cyclin E to turn on, enforcing the idea that the cell needs to go through early G1 properly before late G1. And we even required an external growth factor (like EGF) for Cyclin D1 activation, on top of everything else, to make sure the model doesn’t assume growth signals out of thin air.”

“So what happened with all these extra conditions? Essentially, the model became super strict – it found even more scenarios that would prevent the cell from dividing. That’s what the green heatmap on the slide is showing: compared to the original and our first refined model, the LogicGep-inspired model (far right) has green in more places, meaning under more combinations of conditions the cell ends up arrested. For example, now if the model senses any DNA damage (activating p53), it will refuse to cycle (which biologically makes sense – DNA damage triggers p53 to halt the cycle). While this might be overzealous without experimental confirmation, it’s pointing out additional potential “pressure points” in the network. The diagram comparison illustrates the difference: the right-side network (LogicGep-refined) has a few more arrows – notably that new p53 node – acting as an extra brake. We have to stress: this extended model is hypothetical. It’s an exploration of “what if we make the cell even more cautious to enter S-phase?” It suggests, for instance, that a drug activating p53 (if such a thing could be done selectively) might synergize with HER2 targeting. But since we don’t have experimental data on those new rules, we consider this an exploratory bonus. The main validated refinement was the Cyclin D1 rule. Still, this exercise shows how we can systematically use logic-based approaches to propose new hypotheses – like involving the p53 pathway – for controlling cancer cell proliferation.”

## Slide 9: Conclusions

To wrap up, modeling and experimental validation are both necessary for understanding de novo trastuzumab resistance. Further refinement of Boolean rules might incorporate unmodeled feedback loops—especially for Cyclin E1. Finally, c-MYC inhibition remains a promising avenue to tackle cells that don’t respond to trastuzumab. Now we will be happy to answer your questions.

From a practical standpoint, the refined model suggests that combination treatments are likely needed for HER2-positive cancers that don’t respond to HER2 blockers alone. In silico, hitting both the AKT and MEK pathways had a big impact, as did combinations like HER2 + MEK inhibition. Interestingly, the model also flags the estrogen receptor and c-Myc as a duo – implying that perhaps a cocktail of anti-HER2, anti-estrogen, and maybe a Myc-targeted agent could be a potent mix for certain breast cancers. Looking ahead, we’d love to integrate actual time-course data and use algorithms to fine-tune the network further – maybe incorporating stress signals like p53 more robustly – to see if we can predict responses even more accurately

The big picture takeaway is that Boolean models are a handy tool: even though cells are very complex, boiling their pathways down to ON/OFF logic let us systematically test ideas and align them with lab results. This kind of iterative modeling could guide the design of multi-pronged therapies to outsmart cancer’s redundant wiring.”

---
title: "Chapter 5: Paper 4"
numbering:
  enumerator: 2.4.%s
---
### Problem statement

Research shows that Australia is a global hotspot for endemism in
plants, and that Tasmania is particularly rich in paleoendemic species
[@caiClimaticStabilityGeological2023]. However, Australia ranks among
the worst globally when it comes to adequate threat assessments for
endemic flora [@gallagherGlobalShortfallsThreat2023]. Slow growth rate
and poor dispersal are characteristics shared by many of Tasmania's
iconic paleoendemic plant species that evolved in cool and stable
environments [@mokanyPresentFutureRefugia2017]. Consequently, they all
share the same sensitivity to fire due to their inability to recover
between fire events [@blissLackReliablePostfire2021]. The intensity
and frequency of wildfires is increasing in Tasmania and around the
world [@bowmanBushfiresTasmaniaAustralia2022;
@fengGrowingHumaninducedClimate2025] and tolerable fire intervals may
already have been exceeded for some taxa
[@leonardTolerableFireIntervals2021]. Genetic diversity metrics
decreased significantly with an index of fire history for *Athrotaxis*
[@worthFireMajorDriver2017].

The IUCN Red List of Threatened Species is a global framework that aims
to assess and monitor the extinction risk of biota
[@iucnIUCNRedList2025]. The assessment uses five primary criteria
(most with sub-criteria), where taxa must meet one or more of the
primary criteria to be categorised as threatened. The criteria include
population trends, geographic range characteristics, population size,
and quantitative analyses of extinction risk
[@iucnstandardsandpetitionscommitteeGuidelinesUsingIUCN2024]. While
the IUCN Red List criteria are comprehensive, there are many compromises
and limitations which are unavoidable for a project of this scope. For
example, using future projections as justification of vulnerability is
encouraged but not mandatory if these criteria are fulfilled using
historical evidence. Critically, it is the responsibility of the
assessor to judge suitability of the population data (with approval by
peer review) used in the evaluation. These flexibilities facilitate
assessments in the absence of data -- which is common for rare and
enigmatic taxa -- but risks masking vulnerabilities in taxa with long
generation times and a lagged response. The result may be an
(unintentional) misrepresentation of the true vulnerability of the
species, which can have real world consequences for the conservation
efforts [@possinghamLimitsUseThreatened2002].

:::{table} Most recent IUCN Red List assessment results for the target taxa. LC = Least Concern; NT = Near Threatened; VU = Vulnerable.
:label: target-taxa-iucn-cat
:align: right

| Scientific Name | Common Name | Year Assessed | Category (prev.) | Criteria | Citation |
|-----------------|-------------|----------------|------------------|----------|----------|
| *Athrotaxis cupressoides* | Pencil Pine | 2012 | VU (VU) | B1ab(ii,iii,v)+2ab(ii,iii,v) | @farjonAthrotaxisCupressoides2013 |
| *Athrotaxis selaginoides* | King Billy Pine | 2012 | VU (VU) | A2cd; B1ab(ii,iii,v)+2ab(ii,iii,v) | @farjonAthrotaxisSelaginoides2013 |
| *Lagarostrobos franklinii* | Huon Pine | 2012 | LC (VU) | - | @farjonLagarostrobosFranklinii2012 |
| *Nothofagus cunninghamii* | Myrtle Beech | 2017 | VU (none) | A4bce | @baldwinNothofagusCunninghamii2017 |
| *Nothofagus gunnii* | Tanglefoot | 2018 | NT (none) | B1ab(iii) | @baldwinNothofagusGunnii2018 |

:::

Regarding the most recent IUCN Red List assessments for our target taxa
![](#target-taxa-iucn-cat). The habitat data used for the three conifers was generated
between 24 to 8 years prior to the assessment in 2012/13 and does not
use future projections of habitat suitability. Additionally, the refer
to the resilience of these taxa on account of their ability to resprout,
and the significant habitat coverage by protected areas (e.g. Tasmanian
Wilderness World Heritage Area). The *Nothofagus spp.* assessments are
more recent and comprehensive: exploiting species occurrence databases
and research modelling habitat suitability in future climates.
Importantly, the conifers were assessed prior to the bushfire events in
2015-2016 and all assessments were made prior to the 2019/2020 bushfires
[@bowman2016TasmanianWilderness2021;
@leonardFireSeverityMapping2021].

The aim of this chapter is not to critique the IUCN Red List or revise
the vulnerability category of these taxa. Rather, these IUCN assessments
are presented as examples to illustrate that even major conservation
organisations like the IUCN are working with and drawing conclusions
from incomplete data. Predictably, research shows that "garbage in,
garbage out" is true for conservation planning and the "garbage out" is
in the form of poor conservation outcomes
[@biggsImplementationCrisisConservation2011; @friessBadDataEquals2011;
@wilsonSensitivityConservationPlanning2005].

### Proposed methods

The objective of this chapter is to uncover vulnerabilities of sensitive
vegetation on a local scale, demonstrate the importance of local scale
dynamics, and the limitations of coarse vegetation mapping for this
purpose. To achieve this, we will develop species distribution models
(SDMs) using MaxEnt [@phillipsMaximumEntropyModeling2006] to predict
habitat suitability for both mature trees and recruitment habitat (i.e.
seedling nurseries) under current and projected climate scenarios. The
SDMs will include environmental predictors related to climate, fire,
topography, and geology. We create three SDMs each using a different
occurrence dataset.

- **SDM1**: DL-derived occurrences
- **SDM2:** TASVEG vegetation communities
  [@departmentofnaturalresourcesandenvironmenttasmaniaTASVEG402020]
- **SDM3:** ALA occurrences [@AtlasLivingAustralia2025]

We will assess vulnerability by implementing a spatial multi-criteria
decision analysis (MCDA) using the variable weights generated by the
MaxEnt SDM [@rodriguez-merinoCombiningMulticriteriaDecision2020].
Habitat connectivity analysis will be performed using circuit theory
approaches implemented in Circuitscape [@mcraeUsingCircuitTheory2008]
to assess dispersal corridors between suitable mature tree habitat and
potential recruitment areas. Model performance will be evaluated using
area under the curve (AUC) metrics, and spatial cross-validation
techniques to account for spatial autocorrelation in occurrence data.
Results will be validated against independent field survey data
collected in the study area.

We will use the resulting vulnerability maps and the associated variable
weightings for each of the three SDMs to characterise the threats to the
local population and how these may inform short- and long-range
management strategies. The characterisations will enable us to identify
the strengths and limitations of the three different datasets as a basis
for informing management practices. Acknowledging that the results of
this analysis cannot be generalised beyond the target subpopulation, we
will draw comparisons between our findings and existing vulnerability
evaluations at the population scale (e.g. IUCN Red List) and how
automated inventories can add value.

This research will require collaborations with key Tasmanian
institutions to ensure access to high-quality datasets and local
expertise. The University of Tasmania Climate Futures Research Group
will provide climate projections specifically developed for Tasmania,
including temperature and precipitation scenarios under multiple
representative concentration pathways. These collaborations will ensure
access to the most recent climate modelling outputs at appropriate
spatial resolutions for a study-site-scale suitability model. Natural
Resources and Environment Tasmania (NRE Tas) will contribute expert
ecological knowledge on the target taxa, particularly regarding
species-specific habitat requirements, fire tolerance thresholds, and
observed recruitment patterns across different landscape contexts.
Additionally, NRE Tas will provide access to the most current TASVEG
mapping data. The Tasmania Fire Service (TFS) will assist with bushfire
triage parameters, such as accessibility for preventative and active
firefighting.

### Key innovations

This chapter presents three key innovations in local-scale vulnerability
assessment for endemic Tasmanian flora. First, we demonstrate a novel
comparative framework for evaluating the relative strengths and
limitations of different occurrence datasets (automated population
inventory, manual community-level mapping, and citizen science records)
in vulnerability modelling, providing practical guidance for
conservation practitioners working with heterogeneous data sources.
Second, we integrate habitat connectivity analysis with multi-criteria
vulnerability assessment to identify not only where species are most at
risk, but also which populations serve as critical source habitats and
dispersal corridors for long-term persistence. Third, we develop a
methodology for translating local-scale vulnerability assessments into
actionable management recommendations by incorporating operational
constraints such as firefighting accessibility and protected area
boundaries.
Second, we integrate habitat connectivity analysis with multi-criteria
vulnerability assessment to identify not only where species are most at
risk, but also which populations serve as critical source habitats and
dispersal corridors for long-term persistence. Third, we develop a
methodology for translating local-scale vulnerability assessments into
actionable management recommendations by incorporating operational
constraints such as firefighting accessibility and protected area
boundaries.

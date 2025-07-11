---
title: Problem statement
numbering:
  enumerator: 1.%s
---

Tasmania is a known hotspot for plant biodiversity, due to the
relatively cool, wet, and stable environment over many long-range
climate cycles [@harrisonEndemismHotspotsAre2017;
@macphailVegetationClimatesSouthern1979;
@readComparativeResponsesTemperature1988]. However, rapid changes to
the environment are eroding these refugial habitats faster than ever
before, posing an existential threat to the ancient species persisting
within [@mokanyPresentFutureRefugia2017]. The threat to these
vegetation communities generally is well understood
[@blissLackReliablePostfire2021; @fletcherInfluenceClimaticChange2021;
@worthGondwananConiferClones2016], but there is little insight into
the vulnerabilities at a population level needed to inform targeted
conservation planning. Targeted and adaptive conservation planning is
non-trivial, as it requires comprehensive species inventories,
identifying and quantifying vulnerabilities, and ongoing monitoring at
temporal intervals appropriate for the target
[@mccarthyActiveAdaptiveManagement2007;
@williamsTechnicalChallengesApplication2016]. This is a challenge that
extends beyond Tasmania, with research showing that adequate
conservation assessments for endemic flora species fall short of
requirements globally [@gallagherGlobalShortfallsThreat2023].

Population inventories are a fundamental parameter for effective
conservation planning, but the immense complexity of natural terrestrial
ecosystems can make it challenging to gather data that accurately
represents a population and the changes over time
[@burgObservationBiasIts2015; @goodAddressingDataDeficiency2006]. The
approaches employed by the Department of Natural Resources and
Environment for mapping vegetation are centred around manual aerial
photo interpretation
[@departmentofnaturalresourcesandenvironmenttasmaniaTASVEG402020].
While this method is effective for mapping vegetation at the community
level at a regional scale, it is insufficient for monitoring threats to
individual trees and changes to populations over time. The need for
detailed and timely data of these trees was made obvious in February
2025, when bushfires burned within metres of Huon pines estimated to be
3000 years old [@lohbergerAerialsRevealHow2025]. These objectives are
particularly important to the conservation outcomes of long-lived tree
species with multi-century generations
[@leonardFireSeverityMapping2021; @leonardTolerableFireIntervals2021;
@lindenmayerGlobalDeclineLarge2012].

Remote sensing and deep learning technologies have the potential to
revolutionise automated species inventories at a regional scale, but the
substantial training data requirements combined with variably in sensor
hardware, configuration, conditions, and target definitions make the
approaches challenging to deploy in real world scenarios
[@brandtHighresolutionSensorsDeep2025]. Many of these challenges have
well established solutions and are already integrated into systems we
use daily [@safonovaTenDeepLearning2023]. Knowledge distillation is
one approach offers a promising pathway to overcome these limitations by
transferring learned representations from high-fidelity datasets to
low-fidelity datasets, yet this approach remains largely unexplored in
vegetation mapping applications [@zhongReviewTreeSpecies2024].
Similarly, while multimodal approaches that integrate environmental and
ecological contextual information have demonstrated improved performance
in species distribution modelling, their application to dense
segmentation tasks for flora remains limited, with virtually no research
examining how models utilise this domain knowledge
[@brodrickUncoveringEcologicalPatterns2019;
@harmonImprovingRareTree2023; @tielMultiscaleMultimodalSpecies2025].

Yet the complexity of both remote sensing data and the target/objective
(i.e. vegetation), mean these techniques remain inaccessible to decision
makers. The convergence of conservation needs for flora in Tasmania and
worldwide, technological maturity of RS with DL approaches, and critical
knowledge gaps in operational implementation creates a unique research
opportunity to develop scalable, species-level monitoring frameworks
that can provide the spatial detail, temporal frequency, and demographic
information required for adaptive conservation planning of these
vulnerable trees.

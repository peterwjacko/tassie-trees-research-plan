---
title: "Chapter 4: Paper 3"
numbering:
  enumerator: 2.3.%s
---

## Problem statement

Remote sensing and conservation scientists have access to more earth
observation data than ever before, but the feature data is only one
piece of the puzzle in realising the full potential of this vast
resource. As with any model of a physical system, meaningful and robust
ground truth data is essential to reliable predictions. Robust datasets
(target-feature pairs) are readily available for common targets in
common contexts such as street trees in urban environments and
demonstrate remarkable performance when leveraged by deep learning
algorithms. However, developing a high-quality dataset of sufficient
size that catalogues the entire diversity of plant species alone is a
monumental task, and this is without considering the many aspects of
diversity possible to each species.

A skilled botanist can rapidly learn to visually identify a previously
unseen species with only a handful of examples by leveraging existing
knowledge of categories combined with contextual information. Moreover,
the probability of a species occurring in a particular location is
strongly influenced by environmental factors like elevation, aspect,
soil type, and climate variables [@porfirioImprovingUseSpecies2014].
However, current deep learning segmentation approaches treat vegetation
mapping as purely a spectral-spatial problem, without considering
contextual information about the surrounding landscape or the target
taxa. This is particularly important in situations where training data
is limited [@safonovaTenDeepLearning2023;
@sumbulFinegrainedObjectRecognition2018].

## Proposed methods

Develop a multimodal DNN architecture with separate encoding branches
for each different mode of information.

We will include variables such as:

- Terrain: elevation, slope, aspect
- Climate: temperature, precipitation, humidity, solar radiation
- Geology: soil, watercourse proximity
- Contextual: coordinates, systematics, date
- Physical: spectral signatures

Implement cross-attention mechanisms between spectral and environmental
features to enable inter-modal relationships. Conduct ablation studies
removing individual environmental variables to quantify their
contribution. Compare against baseline models using stacked
preprocessing and single-encoder approaches
[@audebertRGBVeryHigh2018].

### Key innovations

This research will pioneer true multimodal vegetation segmentation
models, moving beyond simple data stacking. Additionally, we will
quantify the relative importance of environmental context compared to
spectral information for species detection. Lastly, this research will
determine how models integrate ecological knowledge, potentially
revealing new ecological insights about species-environment
relationships.

---
title: "Chapter 3: Paper 2"
numbering:
  enumerator: 2.2.%s
---

*Evaluating vision transformers and state space models for hyperspectral species-level vegetation mapping in complex forest canopies*

## Problem statement

Deep learning applied to hyperspectral remote sensing (RS) data has
demonstrated potential in automated vegetation mapping applications
[@govenderReviewHyperspectralRemote2009;
@zhongIdentificationTreeSpecies2022]. The enhanced spectral depth is
particularly valuable in discriminating plant species in complex forest
canopies [@pereiramartins-netoTreeSpeciesClassification2023]. For the
last decade, Convolutional Neural Network (CNN) architectures have set
the standard for computer vision tasks, in both RS and in general.
However, the inductive biases on CNNs include localised receptive fields
and translational equivariance, constraining their capacity to model
long-range spatial dependencies and global spectral context. This
represents a meaningful limitation in densely structured forest
canopies, where species discrimination may depend on contextual
relationships that extend well beyond the local neighbourhood captured
by a convolutional kernel.

Vision Transformers (ViTs) and their derivatives have emerged as
powerful successors to CNNs in computer vision, demonstrating strong
performance on tasks requiring global context modelling through
self-attention mechanisms. More recently, state space models (SSMs) have
attracted significant attention as computationally efficient
alternatives capable of capturing long-range dependencies with linear
rather than quadratic complexity
[@shaoSTMambaSyncComplementPower2025]. Despite their demonstrated
strengths in natural image tasks, the application of these architectures
to hyperspectral remote sensing for fine-grained vegetation segmentation
is limited.

There is consequently a critical knowledge gap regarding whether the
global context modelling capacity of Transformer-based and SSM-based
architectures confers meaningful advantages over CNN baselines for
species-level segmentation using hyperspectral data. It remains unclear
whether self-attention or selective state space mechanisms are better
suited to capturing the spectral-spatial relationships that underpin
vegetation discrimination, and whether these differences are consistent
across varying forest structural complexity. Addressing this gap is
essential for guiding architecture selection in operational remote
sensing workflows.

## Proposed method

Airborne data collection will employ fixed-wing aircraft platforms to
acquire co-registered RGB optical and hyperspectral imagery across all
study sites. Hyperspectral data will be collected simultaneously using
Specim FX10 (400-1000 nm, 224 bands) and AFX17 (900-1700 nm, 224 bands)
sensors. Ground truth data of tree crowns will be established through a
combination of field data and desktop-based annotations by a domain
expert annotation.

The analytical framework will systematically compare four architecture
families for hyperspectral semantic segmentation: a CNN baseline, a
hybrid CNN-ViT, a pure ViT, and a Vision Mamba SSM. All models will be
evaluated on identical training and test splits under consistent
hyperparameter tuning protocols to ensure fair comparison. Where
architectures admit 3D variants capable of jointly processing spatial
and spectral dimensions, these will also be evaluated to assess the
additional value of explicit spectral modelling relative to treating
bands as additional input channels. Cross-validation across
geographically distinct study sites will provide estimates of model
transferability, a practically important consideration for operational
deployment.

Model performance will be assessed using pixel-wise accuracy metrics
appropriate for semantic segmentation tasks in remote sensing contexts
[@maxwellAccuracyAssessmentConvolutional2021]. Cross-validation
strategies will ensure robust performance estimates and evaluate model
transferability across different study sites. Model explainability and
cross-architecture feature comparison will employ a tiered analytical
strategy designed to be applicable across all architecture families
while also leveraging architecture-native methods where appropriate.
Integrated gradients will serve as the primary attribution method,
providing a theoretically grounded and architecture-agnostic estimate of
input feature importance that can be computed consistently across CNN,
Transformer, and SSM architectures.

## Key innovation

This study provides systematic benchmark of Vision Transformer and
Vision Mamba architectures against CNN baselines for species-level
hyperspectral vegetation segmentation in Tasmanian temperate rainforest.
ViTs and SSM-based architectures have shown promise in agricultural and
urban remote sensing contexts, but their performance in fine-grained
forest species mapping has not been established. The application of
Vision Mamba architectures to hyperspectral remote sensing remains at an
early stage globally, and their efficiency compared to ViTs is
compelling from an operational perspective.

A second contribution is the mechanistic investigation of how different
architectural inductive biases shape the spectral-spatial
representations learned by models. By combining integrated gradients,
attention rollout, and centred kernel alignment across all
architectures, this research will characterise whether global context
modelling captures qualitatively different information from local
convolutional features, and whether spectral or spatial relationships
are the primary drivers of species discrimination. This moves beyond
black-box benchmarking to provide actionable, evidence-based guidance on
architecture selection for operational vegetation mapping.

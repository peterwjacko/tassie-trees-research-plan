---
title: "Chapter 2: Paper 1"
numbering:
  enumerator: 2.1.%s
---

*Evaluating deep learning architectures and domain-specific weights for mapping Tasmanian rainforest trees*

## Problem statement

DNNs applied to ultra-high spatial resolution imagery offer robust
capabilities for fast and granular canopy mapping
[@cavender-baresIntegratingRemoteSensing2022]. Convolutional Neural
Networks (CNNs) efficiently extract multiscale features through
inductive biases like spatial locality, and architectures such as U-Net
have proven highly effective for tree crown segmentation in RGB imagery
[@kattenbornConvolutionalNeuralNetworks2019;
@kattenbornReviewConvolutionalNeural2021;
@ronnebergerUNetConvolutionalNetworks2015]. However, these same
inductive biases, spatial locality and hierarchical feature extraction,
make CNNs favour texture cues over structural shape information and
prone to shortcut learning
[@kattenbornSpatiallyAutocorrelatedTraining2022]. In contrast, ViTs
utilise global self-attention to dynamically model complex and
long-range spatial relationships
[@dosovitskiyImageWorth16x162020]. ViTs condition predictions on global
context, whereas CNN predictions are constrained by the spatial extent
of the receptive field. While ViTs may outperform CNNs in many
benchmarks, they are also more "data-hungry" and compute heavy than
CNNs. These characteristics present considerable limitations when
working with the sparse, domain-specific datasets typical of specialised
remote sensing tasks.

Transfer learning offers a key strategy for improving model performance
under data scarcity, whereby weights learned during training on a large
source dataset are transferred to initialise a model for a target task.
This may involve feature extraction, which involves freezing all
pre-trained weights and training only a task-specific head. Or taking it
a step further with fine-tuning, where the higher-level layers are
selectively retrained to adapt representations to the target domain.
These principles have motivated the development of domain-specific
weights derived from remote sensing imagery, which are known to improve
convergence and accuracy over general-purpose initialisations such as
ImageNet. Critically, however, the datasets underpinning these remote
sensing weights typically reflect broad land cover classes sampled from
North America or Europe [@bastaniSatlasPretrainLargescaleDataset2022],
and there is little research into how this impacts performance in the
Australian context.

Consequently, there is a critical need to systematically compare model
architecture, pre-training strategy, and their interaction under
conditions of data scarcity. Current literature lacks rigorous ablation
studies that quantify the computational and data-efficiency trade-offs
between localised (CNN) and global (ViT) feature extraction across
varied training set sizes and weight initialisations. Establishing best
practices requires a structured, factorial comparison of these
architectures and initialisations to determine whether the superior
contextual awareness of Transformers justifies their greater data
requirements in sparse, domain-specific applications.

## Proposed method

Tree crown segmentation will be performed on RGB aerial imagery
(0.03 m GSD) with field-validated crown masks across three species:
Huon pine, Myrtle beech, and Blackwood. A fixed chip size of 1,024 px
will be applied across all treatments, yielding 11,264 samples from 44
input tiles, with an 80/20 train-validation split sampled randomly from
the pooled dataset. Data augmentation will be applied dynamically via
Kornia, employing remote sensing-specific techniques that preserve
spatial context while introducing realistic transformations to reduce
overfitting including Flip-n-Slide
[@abrahamsConciseTilingStrategy2024] and Sat-SlideMix
[@hopkinsDataAugmentationApproaches2025].

A systematic ablation study will compare four common segmentation
architectures (U-Net, U-Net++, SegFormer, and Swin Transformer) across
a factorial matrix of encoder backbones, weight initialisations
(ImageNet, Satlas, and Clay LINZ), and optimisation strategies.
CNN-based models will be optimised using Adam with momentum
[@kingmaAdamMethodStochastic2014], while transformer-based
architectures will use AdamW with weight decay regularisation
[@loshchilovDecoupledWeightDecay2018]. For pre-trained initialisations,
a two-stage fine-tuning strategy will be employed: an initial warm-up
phase freezing the encoder while training the decoder and segmentation
head, followed by end-to-end fine-tuning at a reduced learning rate.

Model performance will be evaluated on full orthomosaics using a sliding
window approach with Gaussian-weighted kernel aggregation to minimise
edge artefacts. Assessment will be conducted using Overall Accuracy,
mean Intersection over Union (mIoU), and mean F1-Score, alongside
per-class metrics, enabling direct comparison of architectural and
initialisation trade-offs across species
[@wangRevisitingEvaluationMetrics2023a].

## Key innovation

This study presents one of the first systematic evaluations of CNN and
Vision Transformer architectures for fine-grained, species-level tree
crown segmentation in Tasmanian temperate rainforest. By framing the
comparison as a controlled ablation across architectures, backbones, and
weight initialisations, the study will produce transferable guidance on
architecture selection under data-scarce, domain-specific conditions.

A central innovation is the structured evaluation of geospatial
foundation model weights, specifically Satlas and Clay LINZ, against
conventional ImageNet initialisations in a high-resolution RGB
segmentation context. While domain-adaptive pre-training has
demonstrated value in broad land cover classification, its utility for
fine-grained species delineation at centimetre resolution remains poorly
characterised, particularly outside North American and European training
distributions. This study directly interrogates that gap, providing the
first assessment of these initialisations in an Australian ecological
context.

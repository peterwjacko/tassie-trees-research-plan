---
title: "Chapter 3: Paper 2"
numbering:
  enumerator: 2.2.%s
---

## Problem Statement

High-resolution hyperspectral imagery enables precise discrimination of
vegetation classes in complex forest canopies through detailed spectral
signatures [@modzelewskaTreeSpeciesIdentification2020]. However,
hyperspectral data is seldom used for regional-scale mapping and
monitoring in operational contexts due to the cost of sensors and
processing complexity [@santosGeometricCalibrationHyperspectral2022].
The imagery used for regional-scale vegetation mapping is typically
supplied by aerial imagery vendors in proximity to the area of interest.
Contemporary aerial imaging platforms are typically equipped with frame
cameras sensitive to red, green, blue (RGB), and occasionally near
infrared (NIR) wavelengths. Most operational imagery programmes target a
spatial resolution of around 0.10 m, striking a balance between survey
coverage and spatial detail. Satellite imagery has similar trade-offs,
where the broad temporal, spatial, and spectral coverage come at the
cost of spatial resolution. Some commercial satellite programs offer
multispectral imagery with sub-metre spatial resolution, but the cost of
these datasets can be prohibitive in many cases.

This disparity creates a critical gap between research-grade datasets
optimised for algorithm development and the operational imagery
available for conservation management applications. Without effective
domain adaptation strategies, advances in deep learning-based species
mapping remain confined to controlled research environments, limiting
their application to real-world conservation practice where they are
most needed.

## Proposed methods

This research will develop a progressive domain adaptation framework
employing spectral knowledge distillation and multi-resolution training
strategies. The approach will utilise paired hyperspectral-multispectral
datasets to train teacher-student architectures, where
hyperspectral-trained models guide the learning of spectrally and
spatially constrained networks.

The framework will be evaluated using both synthetically degraded
datasets and authentic operational imagery to assess real-world
performance. Synthetically degraded datasets will aim to emulate common
data characteristics from aerial imagery programs such as the Tasmanian
Imagery Program, and from high resolution satellite programs such as
WorldView-3. This approach will enable controlled ablation studies while
validating the generalisability in genuine datasets.

## Key innovations

This work will establish a framework for leveraging the rich
spatial-spectral information in hyperspectral datasets to make accurate
dense predictions of vegetation type in lower-fidelity, but universally
accessible imagery. The proposed dual-encoder architecture represents a
novel approach to leveraging rich training data while maintaining
compatibility with standard aerial platforms. By developing systematic
knowledge transfer protocols, this research will support the widespread
deployment of advanced deep learning methods using readily available
imagery, expanding the practical impact of remote sensing technologies
in conservation management.

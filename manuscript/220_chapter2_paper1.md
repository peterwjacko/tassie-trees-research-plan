# Chapter 2 - Paper 1

> Semantic segmentation of Tasmanian vegetation species in complex scenes using deep neural networks and very high-resolution hyperspectral imagery

## Problem Statement

Hyperspectral remote sensing has demonstrated potential in automated vegetation mapping applications [@govenderReviewHyperspectralRemote2009; @zhongIdentificationTreeSpecies2022]. In addition to condition monitoring, the enhanced spectral depth is particularly valuable in discriminating plant species in complex forest canopies [@pereiramartins-netoTreeSpeciesClassification2023]. Despite the increasing accessibility of hyperspectral sensors, they are rarely deployed in real-world conservation scenarios due to their cost and complexity.

In recent years, deep learning algorithms have emerged as powerful tools for computer vision tasks and offer several key advantages over traditional classification approaches in the context of vegetation mapping. DL algorithms have proven highly effective in semantic segmentation tasks targeting vegetation species using high resolution hyperspectral data [@zhangThreedimensionalConvolutionalNeural2020]. Likewise, studies using high resolution RGB-only datasets for similar task and targets have also achieved high accuracy with deep learning approaches [@egliCNNBasedTreeSpecies2020; @garzon-lopezSpeciesClassificationTropical2020].

Despite strong evidence showing that deep learning is effective in species-level vegetation mapping tasks without access to rich spectral information, there are limited studies comparing the two input feature sets [@nezamiTreeSpeciesClassification2020]. Studies comparing high-resolution RGB and hyperspectral datasets typically focus on assessing plant condition in agricultural scenarios, where the additional spectral depth significantly improves accuracy [@xuDeepLearningModel2025].

Research comparing the performance of deep learning segmentation models trained on RGB imagery versus those informed by hyperspectral data, particularly in complex forest canopies. Furthermore, there is limited understanding of the underlying mechanisms driving performance differences between these approaches—specifically whether improved accuracy stems from the additional spectral information content itself, or from the complex spectral-spatial relationships that deep learning models can exploit within hyperspectral datasets.

## Proposed method

Airborne data collection will employ fixed-wing aircraft platforms to acquire co-registered optical and hyperspectral imagery across all study sites. Flight operations will target 500 metres above ground level to optimise the balance between spatial resolution and survey efficiency. This altitude specification will yield ground sampling distances of approximately 0.03 metres for RGB imagery and 0.40 metres for hyperspectral data.

Optical imagery acquisition will utilise a PhaseOne PAS 150 frame camera system, with subsequent processing into three-band orthomosaics using photogrammetric workflows. Hyperspectral data collection will employ simultaneous deployment of Specim FX10 and AFX17 sensors. The FX10 is sensitive to near-infrared (NIR) wavelengths (400-1000 nm) across 224 spectral bands, while the AFX17 is sensitive to shortwave infrared (SWIR) wavelengths (900-1700 nm) across 224 bands

Co-registration between hyperspectral and RGB datasets will leverage the methodology developed by, Haynes et al., [@haynesCoRegistrationMultiModalUAS2025] which utilised the same sensor combination as we propose. The two datasets will be stacked into a multiband raster during preprocessing.

Ground truth data will be established through manual delineation of individual tree crowns for target species using geographic information system software. Crown boundary annotation will be performed on the analysis-ready imagery by expert botanists. To ensure annotation accuracy and reduce interpretation bias, a randomly selected subset of desktop-derived annotations will undergo field validation through direct ground-based observation.

The initial reference dataset will be augmented using established data augmentation techniques [@mumuniDataAugmentationComprehensive2022] to increase sample size and improve model robustness.

The analysis will evaluate the contribution of spectral information to species-level semantic segmentation accuracy through systematic comparison of two-dimensional (2D) and three-dimensional (3D) implementations of established deep learning architectures. This comparison will isolate the value of spatial-spectral relationships in hyperspectral data while controlling for architectural differences.

The analysis will concentrate on 2D and 3D variants of U-Net architectures [@ronnebergerUNetConvolutionalNetworks2015], which have demonstrated established efficacy in remote sensing applications, particularly for vegetation segmentation in high-resolution imagery [@floodUsingUnetConvolutional2019; @schieferMappingForestTree2020]. By constraining the comparison to a single architectural family, the contribution of spatial-spectral relationships can be isolated without confounding effects from different network designs.

Model performance will be assessed using pixel-wise accuracy metrics appropriate for semantic segmentation tasks in remote sensing contexts [@maxwellAccuracyAssessmentConvolutional2021a]. Cross-validation strategies will ensure robust performance estimates and evaluate model transferability across different study sites.

To understand the spectral and spatial features driving species discrimination, model interpretation will employ multiple explainability techniques. Gradient-weighted Class Activation Mapping (Grad-CAM) will identify spatial regions most influential for species classification decisions [@onishiExplainableIdentificationMapping2021]. Shapley Additive Explanations (SHAP) values will quantify the contribution of individual spectral bands to model predictions [@huangSurveySafetyTrustworthiness2020]. These interpretation methods will provide insights into whether spectral relationships are as critical as spatial relationships for accurate species identification.

## Key Innovations

This research addresses three critical knowledge gaps in remote sensing-based vegetation mapping. First, it will determine which deep neural network architecture yields the most accurate segmentation of Tasmanian vegetation species using hyperspectral imagery. Second, it will quantify the spectral requirements for accurate vegetation segmentation, specifically evaluating the potential of RGB-only datasets as alternatives to hyperspectral data for operational mapping applications. Third, it will investigate whether spectral relationships are as important as spatial relationships for species identification, providing fundamental insights into the mechanisms underlying deep learning-based vegetation discrimination.

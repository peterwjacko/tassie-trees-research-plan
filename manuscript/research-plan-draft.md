---
title: "Research Plan Draft"
author: "Peter Jackson"
reference-section-title: "References"
---
# Introduction

## Background
 <!--
 - Begin with a statement of the broad context, then narrow to your specific topic.
 - Outline the setting and scope of the research field.
 - Explain why this topic demands investigation now.
 -->

<!-- ### Ecological significance -->
- The target species (huon pine + pencil pine + King Billy pine)
  - They are extremely slow growing
  - Their range/distribution is restricted by temperature and moisture. E.g. the huon pine habitat is effectively a fire refugium [@gibsonEcologyLagarostrobosFranklinii1991].
  - A warming and drying climate will increase the probability of fires in huon pine (and others) habitat
  - Recruitment of new individuals may be reduced in areas where it is drying and warming (and burning more)
  - Ecological role??

<!-- ### Limitations of current approach -->
- The current mapping of the target species is limited.
  - It is generated with an outdated method (mostly aerial photo interpretation)
  - It is generated infrequently
  - It is coarse
  - It's limited to accessible areas
  - It's costly (lots of human expert hours required)
  - It doesn't support monitoring health/condition
- The result is a misrepresentation of the condition and status of the species ( huon pine is currently listed as IUCN "Least Concern")

<!-- ### Limitations of common automated techniques -->
- Hardware limitations
  - Spatial resolution of data is coarse.
  - Spectral resolution of data is narrow.
  - Structural data is often missing due to cost.
- Software (algo) limitations
  - pixel-based approaches are limited with high res data.
  - OBIA approaches require target-specific segmentation and feature engineering.
  - This limits the ability to generalise between sites (e.g. when using random-forest, support-vector-machine) which can be addressed by neural nets if done correctly.
- Logistical limitations for specialised data/hardware
  - The cost of data acquisition increases with the spatial/spectral resolution.
  - The cost of data processing and storage increases with the spatial/spectral resolution.
  - Increasing spatial resolution (GSD) typically reduces the survey size.
  - Specialised data requires expertise to interpret and analyse.
  - Projects are less likely to have ongoing support if they are expensive and inaccessible.
- Logistical limitations of advanced algorithms
  - Deep learning algorithms require a lot of training data.
  - Deep learning approaches are expensive to create (compute time).
  - Deep learning approaches require expertise to create.
- General logistical limitations
  - Cloud cover limits acquisition
  - Sun angle limits acquisition (especially for huon pine which is found on river banks often with high relief)

<!-- ### Proposed solution -->
- Although deep learning has some considerable drawbacks, they are mostly of a logistical nature. The performance and flexibility of deep neural networks make them more applicable than traditional ML approaches for this problem and similar applications.
- Therefore we will develop a deep neural network model to find and map the target tree species in remote sensing imagery.
- Using this map/inventory we can quantify:
  - Population
  - Condition
  - Threat of bushfire
  - Threat of climate change

# Aim and objectives

The overarching aim of this project is to assess the value of remote sensing and deep learning for ecosystem monitoring by investigating the accuracy, applicability, accessibility, and scalability of these technologies. The research will target four species of plants endemic to Tasmania and their associated vegetation communities.

To achieve this aim, we will focus on the following objectives:

1. Investigate the role of hyperspectral data in generating accurate segmentations of native vegetation classes in complex forest canopies by comparing the performance of model architectures that capture the spatial-spectral relationships in the data with architectures that only consider the spatial relationships.
2. Quantify the impact of data quality parameters (spatial resolution, spectral resolution, structural data, addition of extra-modal information) on the performance of semantic segmentation models to inform operational standards.
3. Develop a deep learning model to estimate the condition of the target species that can be used to identify and monitor vulnerable subpopulations.
4. Apply techniques such as transfer learning or model fine-tuning to exploit established data repositories with statewide coverage such as the Tasmanian Imagery Program or the Sentinel-2 mission.

# Methods

## Overview

This research employs a thesis by compilation approach, comprising four analysis chapters (published or submitted journal articles) and two thesis chapters.

### Chapter 1: Introduction

Chapter 1 will introduce the project by describing the ecological context, the availabile technologies, and the research gap.

The chapter will follow the structure below:

1. Background and motivation
2. Problem statement
3. Aim and objectives
4. Thesis structure

### Chapter 2: Paper 1

#### Problem statement

- Mapping veg is important for effective conservation and management efforts.
- Remote sensing and machine learning is ideal for creating maps automatically.
- Traditionally(?) understood that high spectral detail (hyperspectral) is required for species-level mapping in complex forest canopies.
- However, these sensors are expensive and require expertise to operate and interpret the data.
- This creates a barrier for its use which means we are missing out on using this tech.
- Traditional methods with lower spectral res fall short in accuracy and generalisation.
- Deep learning has potential to create accurate species-level mapping with less spectral information and better generalisation.
- Deep learning also has potential to investigate the relationships between spectra for a given species. This will help us determine if the specral depth is important for mapping veg to species level.

#### Proposed method

- Aerial imaging of known target-species habitat
  - RGB (~3 cm)
    - Photogrammetry
  - HSI (~40 cm)
    - VNIR (400 – 1000 nm)
    - SWIR (900 – 1700 nm)
- Coregister RGB and HSI
- Dataset generation
  - In-situ surveys of species presence.
  - Create masks of species via AIP/desktop analysis.
- Develop and compare DL architectures
  - Possibly focus on U-Net only to keep it simple (unless another good option comes up)
  - 2D-CNN (spatial *(xy)* relationships only)
  - 3D-CNN (spatial and spectral *(xyz)* relationships)
  - Hybrid CNN-transformer models
  - Vision Transformers
- Evaluate performance
  - Pixel-wise evaluation of accuracy
  - F1-score
- Model interpretation
  - Gradient-weighted class activation mapping (Grad-CAM)
  - Shapley Additive Explanations (SHAP)
  - Attention heatmaps

#### Study area and datasets

Study areas:

- Southern Tarkine
  - Wilson River
  - Harman river
  - Stanley River
- Southwest
  - Davey River
  - Gordon River
  - Mount Read
  - Frenchmans Cap

Datasets:

- RGB photogrammetry (PhaseOne)
- HSI (Specim FX10, AFX17)

#### Key innovation

- Determine which DNN architecture yields the most accurate segmentation of Tasmanian vegetation with HSI data
- Determine which spectra are necessary for accurate segmentation of Tasmanian vegetation, and the potential of RGB-only datasets
- Determine if the *relationships* of the spectra are as important as the spatial relationships for species identification

### Chapter 3: Paper 2

#### Problem statement

- The accuracy of automated vegetation segmentation to species level is known to improve with more information (e.g. structural, spectral, high resolution, contextual)
- However, increasing the amount of information used in a model incurs various operational costs
  - Sensor hardware must be acquired (e.g. lidar, hyperspectral)
  - Increasing GSD will increase acquisition time
  - Additional sensors and high spatial resolution of data will increase preprocessing costs
  - Specialised instruments require expertise
  - Contextual information must be generated by experts or additional models
  - Additional dimensions increase compute time for model training and inference
  - Additional training data is expensive
- Additionally, it's more difficult to generalise models trained on niche information (cite)
- Meanwhile, aerial surveys typically acquire data with the following specs
  - GSD: 0.1 m to 0.25 m
  - Spectra: RGBNIR
- Highest res satellites ~0.5 m with RGBNIR
- Open access satellite imagery 10 m to 30 m
- Cutting edge approaches are often designed in "ideal" conditions and are not aligned with operational constraints

> **Consider skipping the "ablation" part and focus on transfer learning to TIP data?**

#### Proposed method

- Using the lessons from Chapter 2 (which model architecture works best with which spectral information)
- Derive a realistic set of requirements using ablation:
  - Emulate a range of typical spatial resolutions (0.5 m to 10 m GSD)
  - Emulate a range of spectral resolutions (RGB, multispectral, hyperspectral)
  - Training sample size
  - Fusion of other remote sensing data (SAR, other?)
  - Fusion of contextual datasets (climate, soil, other?)
- Evaluate the effect of training samples
  - Minimum sample size
  - Augmentation techniques
- Analyse cost-benefit relationships between data quality and classification accuracy using statistical modelling approaches.

#### Study area and datasets

Study areas:

- Listed in Chapter 2.

Datasets:

- Datasets listed in Chapter 2.
- Datasets available from
  - Tasmanian Imagery Program
  - Sentinel-2
  - Planet/Maxar (wishlist)
  - Other?

#### Key innovation

- Hmmm?

### Chapter 4: Paper 3

#### Problem statement

- Population count/inventory is the start, but health and condition assessment is critical for conservation management of threatened species
- Bushfires are the main threat to all the target species
- Existing condition assessment methods for the target species are essentially non-existent (cite/confirm)
- Regular field based monitoring of the target species' condition is challenging due to the remote locations and fragmentation of suitable habitat
- Consequently, rapid changes to threat models are difficult to detect in a timely fashion
- Additionally, …I forgot the point I was adding
- Early detection of environmental stressors is crucial for conservation intervention
- Traditional field-based monitoring cannot provide the spatial and temporal coverage needed for effective conservation management

#### Proposed method

- Deep learning model development
    - Time series analysis
    - Populations at risk of bushfire
- Still formulating this idea

#### Study area and datasets

Study areas:

- Listed in Chapter 2.

Datasets:

- Datasets listed in Chapter 2 & 3
- Field validation data
- Environmental variables
  - Climate data
  - Soil information
  - Topographic variables

#### Key innovation

- Deep learning approach to bushfire threat in Tasmania
- Deep learning approach to triage/threat/vulnerability modelling for vegetation

### Chapter 5: Paper 4

#### Problem statement

- High-resolution specialised sensors can create detailed, species level maps
- But lack the temporal resolution for timely and effective monitoring
    - This even applies to operational aerial imagery programs
    - TIP does not have complete coverage of the state (Tas) since it's initiation in ~2012. Coverage is mostly around populated areas.
- Challenges in adapting models trained on high-resolution data to operational datasets because the target is not visible
- Need for scalable monitoring systems that can leverage existing data infrastructure
- Massive, pre-trained models are available for use under open source licenses
- Lack of meaningful ways to link the insights from fine-spatiospectral-scale models and their outputs to coarse-spatiospectral-scale datasets (and models) 
    - For both population inventory applications and condition assessment applications
    - e.g. can we use something as proxy for population count?
    - e.g. can we assess condition at a community scale in course data and get a meaningful result? What is that variable?
    - e.g. other?

#### Proposed method

- Use transfer learning
- Use fine tuning
- Fine tune pre-trained self-supervised models

#### Study area and datasets

Study areas:

- Statewide Tasmania analysis
- Focus areas from Papers 1-3 for validation

Datasets:

- Sentinel-2
- Landsat
- Tasmanian Imagery Program
- Open-source foundation models
    - Clay
    - Prithvi-2
    - Other?

#### Key innovation

- First operational-scale deep learning implementation for endemic vegetation monitoring
- Scalable framework for transitioning from research to operational systems
- Integration of multiple satellite data streams for comprehensive monitoring
- Demonstration of transfer learning effectiveness across spatial and temporal domains

### Chapter 6: Synthesis and Conclusion

#### Synthesis

- Integration of findings across all four research papers
- Evaluation of remote sensing and deep learning value for ecosystem monitoring
- Analysis of trade-offs between key performance criteria:
  - Accuracy: How well do the methods perform?
  - Applicability: Where and when can they be used?
  - Accessibility: How easy are they to implement?
  - Scalability: Can they be applied at operational scales?
- Comparison of different approaches across the research objectives:
  - Spatial-spectral relationships vs spatial-only (Paper 1)
  - Data quality requirements vs operational constraints (Paper 2)
  - Condition assessment capabilities and limitations (Paper 3)
  - Research-to-operational transferability (Paper 4)
- Implications for conservation management of endemic Tasmanian species:
  - Population monitoring capabilities
  - Early warning systems for environmental stress
  - Cost-effective monitoring solutions
  - Integration with existing conservation frameworks
- Broader applications to ecosystem monitoring:
  - Transferability to other species and regions
  - Methodological contributions to remote sensing science
  - Guidelines for operational implementation
- Recommendations for implementation:
  - Optimal sensor configurations
  - Data processing workflows
  - Validation and quality control procedures
  - Stakeholder engagement strategies

#### Conclusions

- Recap of overarching research aim:
  - Assessment of remote sensing and deep learning value for ecosystem monitoring
  - Focus on accuracy, applicability, accessibility, and scalability
- Address each research objective with key findings:
  - **Objective 1** (Hyperspectral spatial-spectral relationships):
    - Key contributions and findings
    - Implications for sensor selection
  - **Objective 2** (Data quality parameters):
    - Quantified relationships between data quality and performance
    - Evidence-based operational guidelines
  - **Objective 3** (Condition assessment models):
    - Automated landscape-scale health monitoring capabilities
    - Early detection and intervention frameworks
  - **Objective 4** (Transfer learning applications):
    - Operational scalability demonstrations
    - Integration with existing data infrastructure
- Summary of key methodological contributions:
  - Novel deep learning architectures for vegetation monitoring
  - Multi-modal data fusion techniques
  - Transfer learning frameworks for operational scaling
  - Standardised condition assessment protocols
- Summary of practical challenges encountered:
  - Data acquisition and processing limitations
  - Model interpretability and validation challenges
  - Operational deployment considerations
  - Stakeholder engagement and adoption barriers
- Opportunities for future research:
  - Extension to other endemic species and ecosystems
  - Integration with climate change monitoring
  - Real-time monitoring system development
  - Citizen science and community engagement applications
  - Policy and management framework development

# Timeline
<!-- Brief description of timeline -->

<!-- figure (gantt chart) or reference to gantt chart in appendices -->

[[project-timeline]]

# Resources and Budget
<!-- List essential equipment, software, travel, and any funding requirements. Keep it high-level, with ballpark figures if known. -->

# Data Management and Ethics
<!-- Explain how you will store, share, and secure data, plus any ethical approvals needed. -->

# Risk Assessment and Contingencies
<!-- Identify key risks (e.g. weather delays, equipment failure) and outline fallback plans. -->

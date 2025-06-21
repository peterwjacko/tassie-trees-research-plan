---
title: PhD Research Plan
subtitle: "Protecting the Old with the New: Finding and Monitoring Tasmania's Prehistoric Conifers Using Remote Sensing and Deep Learning"
authors:
  - name: Peter Jackson
    affiliations:
      - University of Tasmania
    orcid: 0009-0005-9630-3501
    email: p.jackson@utas.edu.au
license: CC-BY-4.0
keywords: deep-learning, remote-sensing, ecology
---

## Introduction

### Background

#### Patterns of ecosystem vulnerability in Tasmania

The impact of human activity on the natural environment is far-reaching, rapid, and undeniable [@crutzenAnthropocene2000; @steffenAnthropoceneAreHumans2007]. Consequently, there is an urgent global imperative for comprehensive ecosystem monitoring at scales necessary for effective conservation management [@farriorDominanceSuppressedPowerlaw2016; @keppelCapacityRefugiaConservation2015]. This challenge is particularly acute for endemic species, which often occupy restricted habitats and exhibit limited adaptive capacity to environmental change, yet conservation assessments for endemic species remain inadequate globally [@gallagherGlobalShortfallsThreat2023]. The persistence of ancient lineages in geographically restricted refugia represents a critical conservation priority, as these climatically stable areas function as both evolutionary museums and potential sources for future biotic radiation [@caiClimaticStabilityGeological2023; @harrisonEndemismHotspotsAre2017; @jetzCoincidenceRarityRichness2004]. Understanding these systems is increasingly urgent given the theory of alternative stable states, where ecosystems may be unable to return to their original ecological condition once critical thresholds are exceeded [@lamotheLinkingBallandcupAnalogy2019].

Tasmania exemplifies global patterns of paleoendemism, harbouring exceptional concentrations of ancient lineages with highly restricted contemporary distributions. The island's temperate vegetation communities include numerous iconic paleoendemic species such as *Lagarostrobos franklinii* (Huon pine), *Athrotaxis selaginoides* (King Billy pine), *Athrotaxis cupressoides* (pencil pine), and *Nothofagus gunnii* (tanglefoot beech). While *Nothofagus cunninghamii* (myrtle beech) is not endemic to Tasmania, it shares many similar characteristics and habitat with the endemics. These species represent broader patterns of Tasmanian paleoendemism, persisting through the use of different climate refugia strategies: wet rainforest refugia support Huon pine and myrtle beech [@buckleyChangingTemperatureResponse1997; @drewDynamicsSeasonalGrowth2022; @lindenmayerFactorsAffectingPresence2000], while cool alpine environments provide habitat for tanglefoot beech and *Athrotaxis* species. Both *Athrotaxis* and *Lagarostrobos* are exceptionally long lived but with extremely slow growth rates [@allen1700yearAthrotaxisSelaginoides2017; @allenPotentialReconstructBroadscale2011; @gibsonDescriptionHuonPine1988; @gibsonConservationManagementHuon1986].

These resilient species have persisted for millions of years, yet their sensitivity to fire—stemming from slow growth rates and limited recruitment capacity—confines them to refugial habitats. Historical anthropogenic impacts have disrupted this delicate balance through intensive logging, habitat inundation from hydroelectric development, and altered fire regimes [@horneEcologicalSensitivityAustralian1991]. Contemporary climate change compounds these pressures through warming and drying trends that increase fire risk and penetrate historically fire-free refugia [@bowmanFireCausedDemographic2019; @holzPopulationCollapseRetreat2020; @worthFireMajorDriver2017]. Evidence of local extinctions and population collapses demonstrates the vulnerability of these slow-growing species to changing fire regimes [@blissLackReliablePostfire2021; @bowman2016TasmanianWilderness2021; @fletcherChangingRoleFire2018]. Additional stressors such as habitat fragmentation and introduced pathogens like *Phytophthora* further compromise population viability [@khaliqPhytophthoraSpeciesIsolated2019]. The combination of historical population reduction and accelerated environmental change has created conditions where slow-growing species lack sufficient time for natural recruitment and recovery [@coleRecoveryResilienceTropical2014], highlighting the critical need for precise spatial monitoring of species distributions and habitat condition.

#### Identifying and quantifying vulnerable areas

Current vegetation mapping approaches employed by Natural Resources and Environment Tasmania (NRE Tasmania) reflect methodological constraints that limit their utility for contemporary conservation challenges. The primary approach relies on manual interpretation of aerial photography, utilising limited spectral information and subjective visual cues to delineate vegetation boundaries [@departmentofnaturalresourcesandenvironmenttasmaniaTASVEG402020]. Temporal resolution represents a critical constraint, with mapping updates occurring irregularly—the most recent TASVEG v4.0 released in 2020 represents the first major update since 2013, with an average of five years between major versions since 2004 [@departmentofnaturalresourcesandenvironmenttasmaniaTASVEG402020]. This temporal lag prevents detection of rapid changes in population extent or condition, particularly problematic when current distributions may represent ecological "echoes" of past conditions where recruitment of new individuals is no longer possible due to altered fire regimes [@keppelCapacityRefugiaConservation2015]. Spatial resolution limitations force reliance on community-level classifications rather than species-level discrimination, masking important ecological patterns within populations and compromising targeted management interventions.

Ground validation protocols introduce systematic sampling bias through preferential access to readily accessible areas, typically excluding remote terrain where many endemic populations persist [@burgObservationBiasIts2015; @clarkeNondetectionErrorsSurvey2012; @morrisonObserverErrorVegetation2016]. The labour-intensive nature of manual interpretation creates scalability constraints, limiting monitoring frequency and extent. Additionally, the methodology provides no information about vegetation health, demographic structure, or population trends—critical parameters for adaptive management given that old and large individual trees are essential to ecosystem health [@lindenmayerGlobalDeclineLarge2012; @lindenmayerNewPoliciesOld2014], population size data are necessary for designing effective conservation areas [@burgmanMethodSettingSize2001], and the quality of presence data directly affects species distribution modelling accuracy [@feiQualityPresenceData2016].

#### The promise of remote sensing and machine learning for ecosystem monitoring

Remote sensing revolutionised automated ecosystem monitoring and at broader spatial scales than possible with traditional field methods [@roughgardenWhatDoesRemote1991]. Early vegetation mapping applications utilised broad-band multispectral sensors such as Landsat and SPOT imagery [@rouseMonitoringVegetationSystems1973; @rousejrThreeExamplesApplied1975], achieving reasonable success for broad vegetation class discrimination. However, the spatial resolution of the datasets limited the types of objects that could be discriminated in scenes with high spectral variance such as forests [@woodcockFactorScaleRemote1987]. Both @fisherPixelSnareDelusion1997 and @cracknellSynergyRemoteSensingwhats1998 stressed the importance the pixel-object relationship, and the problem of mixed signals of sub-IFOV objects. @treitzHighSpatialResolution2000 found that the spatial variation of the classes must be resolvable in the imagery and that multiple spatial scales should be considered when aiming to discriminate forest ecosystems in multispectral imagery. Similarly, @cochraneUsingVegetationReflectance2000 demonstrated that spectral responses in vegetation are "non-unique" in hyperspectral data with a 10 m spatial resolution, and suggests that multiple high spatial resolution samples from a single individual may mitigate this problem.

The pixel-based approach to classification is not suitable for high spatial resolution imagery, where within-class spectral variance can exceeded between-class differences due to shadowing, illumination effects, and sub-pixel heterogeneity [@wulderHighSpatialResolution2004]. Object-based image analysis (OBIA) addressed some of these limitations by accounting for the spatial characteristics of a target [@blaschkeGeographicObjectBasedImage2014; @blaschkeObjectBasedImage2010]. Treating the target as an object captures the within-class spectral variability mitigates the so called "salt and pepper" effect when using pixel-based classification methods in high resolution imagery [@yuObjectbasedDetailedVegetation2006]. OBIA outperforms pixel-based approaches for vegetation discrimination tasks in very high-resolution imagery in many cases [@immitzerTreeSpeciesClassification2012; @sibaruddinComparisonPixelbasedObjectbased2018]. However, @dinglerobertsonComparisonPixelObjectbased2011 found no significant difference between the two approaches, emphasising that the performance of OBIA greatly depends on an effective segmentation and feature engineering.

Machine learning approaches, such as Random Forest (RF) and Support Vector Machine (SVM) algorithms, improved classification accuracy over the physically-based Spectral Angle Mapper (SAM) in early demonstrations [@clarkHyperspectralDiscriminationTropical2005] in both pixel and object-based approaches. While a data driven approach significantly improved the accuracy of species discrimination, these techniques struggled with the multi-scale spatial-spectral characteristics of organic targets such as vegetation [@dinglerobertsonComparisonPixelObjectbased2011].

#### The rise of deep neural networks and representation learning in remote sensing

The advent of deep neural networks fundamentally transformed remote sensing applications by enabling representation learning—the automatic discovery of hierarchical features directly from raw sensor data without manual feature engineering [@lecunDeepLearning2015]. Convolutional neural networks (CNNs) revolutionised dense segmentation tasks through architectures such as fully convolutional networks [@longFullyConvolutionalNetworks2015] and U-Net [@ronnebergerUNetConvolutionalNetworks2015], while more recent Vision Transformers (ViTs) have demonstrated superior performance in image classification tasks compared to traditional CNNs [@kolesnikovImageWorth16x162021]. These learned representations consistently outperform engineered spectral indices by capturing complex spatial-spectral patterns that are difficult to encode manually, particularly for fine-grained species discrimination [@zhongReviewTreeSpecies2024]. However, the substantial data requirements of deep learning models initially posed significant challenges for remote sensing applications, where labelled training data is often scarce and expensive to acquire.

Deep learning has demonstrated remarkable success in tree species segmentation by automatically learning hierarchical spatial-spectral features that capture complex patterns invisible to traditional methods. Notable achievements include the mapping of over 1.8 billion individual trees across 1.3 million km² using U-Net architectures with satellite imagery [@brandtUnexpectedlyLargeCount2020], and fine-grained vegetation mapping achieving 84% accuracy from high-resolution RGB imagery alone [@kattenbornConvolutionalNeuralNetworks2019]. Three-dimensional convolutional neural networks (3D-CNNs) have proven particularly effective for hyperspectral data, simultaneously exploiting both spatial context and spectral relationships to achieve classification accuracies exceeding 95% [@zhangThreedimensionalConvolutionalNeural2020]. However, these advances come with significant challenges: deep learning models require vast amounts of training data across diverse acquisition conditions  [@brandtUnexpectedlyLargeCount2020; @brandtHighresolutionSensorsDeep2025], suffer from limited interpretability as "black box" systems, and often struggle with generalisation beyond their training domains.

The challenge of model transferability across different sensors, geographic locations, and temporal conditions represents a critical bottleneck in operational remote sensing applications. Domain shift—arising from sensor characteristics, atmospheric conditions, seasonal variations, and geographic differences—can severely compromise model performance when deployed beyond training conditions [@brandtHighresolutionSensorsDeep2025]. Spatial autocorrelation in training data further exacerbates this issue, with studies demonstrating that violations of spatial independence can inflate apparent model performance by up to 30%, leading to overly optimistic assessments of generalisation capability [@kattenbornSpatiallyAutocorrelatedTraining2022]. Knowledge distillation (KD) has emerged as a promising solution for cross-sensor learning, enabling the transfer of knowledge from high-fidelity (spatial and spectral) teacher models to lower-fidelity student networks [@himeurApplicationsKnowledgeDistillation2025]. @shinMultispectraltoRGBKnowledgeDistillation2023 showed that KD from a MS-trained teacher model improves the accuracy of a RGB-trained student model by approximately 2% (OA = 94.04%). However, it is necessary to highlight that the teacher and student models in @shinMultispectraltoRGBKnowledgeDistillation2023 share the same RGB dataset which is a spectral subset of the Sentinel-2 based EuroSAT dataset [@helberEuroSATNovelDataset2019]. The teacher uses multiple modalities with an encoder branch for: RGB, NIR, RE, SWIR, whereas the student uses a single encoder branch: RGB. This presents an opportunity for further research into inter-sensor KD. Meta-learning approaches and process-aware learning for vegetation monitoring [@safonovaTenDeepLearning2023].

Multimodal data fusion represents a critical advancement beyond single-sensor approaches, combining complementary information from spectral, structural, and temporal domains to enhance species discrimination capabilities. True multimodal fusion extends beyond feature-level fusion (data stacking) [@zhongReviewTreeSpecies2024], towards architectures that process each modality through dedicated pathways before integration. Late-fusion strategies, where modality-specific streams are processed independently at their native resolutions before final combination, have demonstrated superior performance in species classification tasks compared to unimodal-multi-source models [@hongMoreDiverseMeans2021; @tielMultiscaleMultimodalSpecies2025]. While these approaches have demonstrated the value of integrating multi-source remote sensing data, the true potential of multimodality is in the ability to integrate symbolic or contextual information [baltrušaitis2017multimodalmachinelearningsurvey]. This can be by integrating OpenStreetMap information [@hongMoreDiverseMeans2021], or semantic vegetation attributes and hierarchical taxonomy [@sumbulFineGrainedObjectRecognition2018]. Harmon *et al.* [@harmonImprovingRareTree2023] demonstrates that incorporating domain knowledge through rule-based constraints improves the classification of rare tree species in RGB imagery.

The integration of ecological understanding and environmental context represents a paradigm shift from pure computer vision approaches towards ecologically informed deep learning models. By incorporating environmental variables such as climate, soil properties, and topographic characteristics, these models can leverage the fundamental ecological principle that species distributions are constrained by environmental niches and habitat suitability [@brodrickUncoveringEcologicalPatterns2019]. This approach enables DNNs to move beyond simple biophysical component identification towards the direct recognition of ecological patterns and processes at scales previously impossible to consider [@brodrickUncoveringEcologicalPatterns2019]. The combination of remote sensing imagery and environmental datasets in multimodal DNNs for improving and finding patterns in SDMs [@ryoExplainableArtificialIntelligence2021; @tielMultiscaleMultimodalSpecies2025].

### Problem statement

Tasmania's endemic species face unprecedented threats from climate change and altered fire regimes, yet current mapping approaches are inadequate for conservation planning [@gallagherGlobalShortfallsThreat2023]. Existing methods rely on infrequent aerial photo interpretation that produces coarse, community-level classifications decades apart, providing no information on species-level distributions, population condition, or change detection [@departmentofnaturalresourcesandenvironmenttasmaniaTASVEG402020]. This temporal and spatial resolution mismatch prevents adaptive management responses to rapidly changing environmental conditions.

Deep learning approaches show promise for automated species-level discrimination using remote sensing data, but critical knowledge gaps limit operational application. Most studies focus on classification accuracy rather than understanding which spectral features enable species discrimination, particularly for hyperspectral data. Additionally, the scalability challenge remains unresolved—how to transfer knowledge from high-resolution research datasets to operational monitoring systems using readily available satellite imagery.

Current multi-modal integration approaches employ simple data stacking rather than sophisticated fusion architectures that could leverage complementary spectral, structural, and environmental information streams [@zhongReviewTreeSpecies2024]. The integration of ecological theory and landscape context into deep learning models remains largely unexplored, despite potential for improving both accuracy and ecological realism of species predictions.

This research addresses these gaps by developing hyperspectral deep learning approaches for endemic species mapping, investigating knowledge transfer techniques for operational scalability, and demonstrating integration with conservation planning frameworks. The focus on Tasmania's endemic species provides a critical test case for global paleoendemism conservation while advancing methodological approaches applicable worldwide.

The overarching aim of this project is to develop advanced approaches to automated vegetation mapping by combining remote sensing and deep learning technologies. This research will investigate the accuracy, applicability, accessibility, and scalability of these technologies using Tasmania’s vulnerable vegetation communities as a case study.

To achieve this aim, we will focus on the following objectives:

1. Investigate the role of hyperspectral information for dense prediction tasks of native vegetation target classes in complex forest canopies by comparing the performance of deep neural network architectures that capture the spatial-spectral relationships in the data with architectures that only consider the spatial relationships.
2. Objective 2: on model generalisation and knowledge distillation
3. Objective 3: on DNNs using ecological context and how they exploit ecological patterns
4. Objective 4: on using RS-derived tree inventories to inform better conservation outcomes

## Study area

The proposed study areas ([](#proposed-study-sites)) are concentrated along the west and southwest coasts of Tasmania, encompassing known habitats of the target endemic species. Study site selection was guided by occurrence records from the Atlas of Living Australia [@AtlasLivingAustralia2025], vegetation mapping data from TASVEG 4.0 [@departmentofnaturalresourcesandenvironmenttasmaniaTASVEG402020], and consultation with local botanical experts. Several sites contain documented populations of target species but lack detailed, contemporary mapping products.

:::{figure} ./figures/proposed_study_sites_tasveg_ala_600dpi.png
:label: proposed-study-sites
:align: center

Proposed study sites for this project. **Map a:** The proposed study sites with TASVEG 4.0 [@departmentofnaturalresourcesandenvironmenttasmaniaTASVEG402020] vegetation communities (grouped by dominant species). **Map b:** The proposed study sites with ALA species occurrence records of the target taxa [@AtlasLivingAustralia2025].
:::

Drought conditions over the 2024/25 summer led to series of bushfires initiated by dry lightning strikes in February of 2025. One of these fires burned within proximity to a known Huon Pine population along the Wilson and Harman rivers. This presented us with a unique opportunity to acquire remote sensing data of a marginal population immediately post-fire. As a result, we planned three study sites along the Stanley River, Harman River, and Wilson River ([](#proposed-study-sites): Study Area 1, 2, and 3).

Data acquisition was completed for these three southern Tarkine sites as of April 2025. Additionally, data acquisition for the Davey River site ([](#proposed-study-sites): Study Area 13) was completed in February 2023 using a sensor configuration consistent with this project.

## Proposed methods and thesis structure

### Overview

This research employs a thesis by compilation approach, comprising four analysis chapters (published or submitted journal articles) and two thesis chapters.

#### Chapter 1: Introduction

Chapter 1 will introduce the project by describing the ecological context, the available technologies, and the research gap.

The chapter will follow the structure below:

1. Background and motivation
2. Problem statement
3. Aim and objectives
4. Thesis structure

#### Chapter 2 - Paper 1

*Semantic segmentation of Tasmanian vegetation species in complex scenes using deep neural networks and very high-resolution hyperspectral imagery*

###### Problem Statement

Hyperspectral remote sensing has demonstrated potential in automated vegetation mapping applications [@govenderReviewHyperspectralRemote2009; @zhongIdentificationTreeSpecies2022]. In addition to condition monitoring, the enhanced spectral depth is particularly valuable in discriminating plant species in complex forest canopies [@pereiramartins-netoTreeSpeciesClassification2023]. Despite the increasing accessibility of hyperspectral sensors, they are rarely deployed in real-world conservation scenarios due to their cost and complexity.

In recent years, deep learning algorithms have emerged as powerful tools for computer vision tasks and offer several key advantages over traditional classification approaches in the context of vegetation mapping. DL algorithms have proven highly effective in semantic segmentation tasks targeting vegetation species using high resolution hyperspectral data [@zhangThreedimensionalConvolutionalNeural2020]. Likewise, studies using high resolution RGB-only datasets for similar task and targets have also achieved high accuracy with deep learning approaches [@egliCNNBasedTreeSpecies2020; @garzon-lopezSpeciesClassificationTropical2020].

Despite strong evidence showing that deep learning is effective in species-level vegetation mapping tasks without access to rich spectral information, there are limited studies comparing the two input feature sets [@nezamiTreeSpeciesClassification2020]. Studies comparing high-resolution RGB and hyperspectral datasets typically focus on assessing plant condition in agricultural scenarios, where the additional spectral depth significantly improves accuracy [@xuDeepLearningModel2025].

Research comparing the performance of deep learning segmentation models trained on RGB imagery versus those informed by hyperspectral data, particularly in complex forest canopies. Furthermore, there is limited understanding of the underlying mechanisms driving performance differences between these approaches—specifically whether improved accuracy stems from the additional spectral information content itself, or from the complex spectral-spatial relationships that deep learning models can exploit within hyperspectral datasets.

##### Proposed method

Airborne data collection will employ fixed-wing aircraft platforms to acquire co-registered optical and hyperspectral imagery across all study sites. Flight operations will target 500 metres above ground level to optimise the balance between spatial resolution and survey efficiency. This altitude specification will yield ground sampling distances of approximately 0.03 metres for RGB imagery and 0.40 metres for hyperspectral data.

Optical imagery acquisition will utilise a PhaseOne PAS 150 frame camera system, with subsequent processing into three-band orthomosaics using photogrammetric workflows. Hyperspectral data collection will employ simultaneous deployment of Specim FX10 and AFX17 sensors. The FX10 is sensitive to near-infrared (NIR) wavelengths (400-1000 nm) across 224 spectral bands, while the AFX17 is sensitive to shortwave infrared (SWIR) wavelengths (900-1700 nm) across 224 bands

Co-registration between hyperspectral and RGB datasets will leverage the methodology developed by, Haynes et al., [@haynesCoRegistrationMultiModalUAS2025] which utilised the same sensor combination as we propose. The two datasets will be stacked into a multiband raster during preprocessing.

Ground truth data will be established through manual delineation of individual tree crowns for target species using geographic information system software. Crown boundary annotation will be performed on the analysis-ready imagery by expert botanists. To ensure annotation accuracy and reduce interpretation bias, a randomly selected subset of desktop-derived annotations will undergo field validation through direct ground-based observation.

The initial reference dataset will be augmented using established data augmentation techniques [@mumuniDataAugmentationComprehensive2022] to increase sample size and improve model robustness.

The analysis will evaluate the contribution of spectral information to species-level semantic segmentation accuracy through systematic comparison of two-dimensional (2D) and three-dimensional (3D) implementations of established deep learning architectures. This comparison will isolate the value of spatial-spectral relationships in hyperspectral data while controlling for architectural differences.

The analysis will concentrate on 2D and 3D variants of U-Net architectures [@ronnebergerUNetConvolutionalNetworks2015], which have demonstrated established efficacy in remote sensing applications, particularly for vegetation segmentation in high-resolution imagery [@floodUsingUnetConvolutional2019; @schieferMappingForestTree2020]. By constraining the comparison to a single architectural family, the contribution of spatial-spectral relationships can be isolated without confounding effects from different network designs.

Model performance will be assessed using pixel-wise accuracy metrics appropriate for semantic segmentation tasks in remote sensing contexts [@maxwellAccuracyAssessmentConvolutional2021a]. Cross-validation strategies will ensure robust performance estimates and evaluate model transferability across different study sites.

To understand the spectral and spatial features driving species discrimination, model interpretation will employ multiple explainability techniques. Gradient-weighted Class Activation Mapping (Grad-CAM) will identify spatial regions most influential for species classification decisions [@onishiExplainableIdentificationMapping2021]. Shapley Additive Explanations (SHAP) values will quantify the contribution of individual spectral bands to model predictions [@huangSurveySafetyTrustworthiness2020]. These interpretation methods will provide insights into whether spectral relationships are as critical as spatial relationships for accurate species identification.

##### Key Innovations

This research addresses three critical knowledge gaps in remote sensing-based vegetation mapping. First, it will determine which deep neural network architecture yields the most accurate segmentation of Tasmanian vegetation species using hyperspectral imagery. Second, it will quantify the spectral requirements for accurate vegetation segmentation, specifically evaluating the potential of RGB-only datasets as alternatives to hyperspectral data for operational mapping applications. Third, it will investigate whether spectral relationships are as important as spatial relationships for species identification, providing fundamental insights into the mechanisms underlying deep learning-based vegetation discrimination.

#### Chapter 3 - Paper 2

*Using inter-sensor domain adaptation to address operational constraints of remote sensing datasets*

##### Problem statement

High-resolution hyperspectral imagery enables precise discrimination of vegetation classes in complex forest canopies through detailed spectral signatures [@modzelewskaTreeSpeciesIdentification2020]. However, hyperspectral data is seldom used for regional-scale mapping and monitoring in operational contexts due to the cost of sensors and processing complexity [@santosGeometricCalibrationHyperspectral2022]. The imagery used for regional-scale vegetation mapping is typically supplied by aerial imagery vendors in proximity to the area of interest. Contemporary aerial imaging platforms are typically equipped with frame cameras sensitive to red, green, blue (RGB), and occasionally near infrared (NIR) wavelengths. Most operational imagery programmes target a spatial resolution of around 0.10 m, striking a balance between survey coverage and spatial detail. Satellite imagery has similar trade-offs, where the broad temporal, spatial, and spectral coverage come at the cost of spatial resolution. Some commercial satellite programs offer multispectral imagery with sub-metre spatial resolution, but the cost of these datasets can be prohibitive in many cases.

This disparity creates a critical gap between research-grade datasets optimised for algorithm development and the operational imagery available for conservation management applications. Without effective domain adaptation strategies, advances in deep learning-based species mapping remain confined to controlled research environments, limiting their application to real-world conservation practice where they are most needed.

##### Proposed methods

This research will develop a progressive domain adaptation framework employing spectral knowledge distillation and multi-resolution training strategies. The approach will utilise paired hyperspectral-multispectral datasets to train teacher-student architectures, where hyperspectral-trained models guide the learning of spectrally constrained networks. Key methodological components include: (1) progressive spectral masking during training to simulate operational sensor limitations; (2) dual-encoder architectures with shared spatial feature extraction and late fusion; (3) knowledge distillation techniques to transfer learned spectral-spatial representations from hyperspectral to RGBNIR models.

The framework will be evaluated using both synthetically degraded datasets and authentic operational imagery to assess real-world performance. Synthetically degraded datasets will aim to emulate common data characteristics from aerial imagery programs such as the Tasmanian Imagery Program, and from high resolution satellite programs such as WorldView-3. This approach will enable controlled ablation studies while validating the generalisability in genuine datasets.

##### Key innovations

This work will establish a framework for leveraging the rich spatial-spectral information in hyperspectral datasets to make accurate dense predictions of vegetation type in lower-fidelity, but highly accessible imagery. The proposed dual-encoder architecture represents a novel approach to leveraging rich training data while maintaining compatibility with standard aerial platforms. By developing systematic knowledge transfer protocols, this research will support the widespread deployment of advanced deep learning methods using readily available imagery, expanding the practical impact of remote sensing technologies in conservation management.

#### Chapter 4 - Paper 3

Integrating environmental contextual information in multimodal networks for dense prediction tasks

##### Problem statement

Current deep learning segmentation approaches treat vegetation mapping as purely a spectral-spatial problem, without considering the context of the landscape. However, species distributions are strongly influenced by environmental factors like elevation, aspect, soil type, and climate variables [@porfirioImprovingUseSpecies2014]. This is particularly important in situations where training data is limited [@safonovaTenDeepLearning2023; @sumbulFineGrainedObjectRecognition2018]. Failing to incorporate this contextual information may limit model performance, generalisability, and interpretability.

##### Proposed methods

Develop a multimodal DNN architecture with separate encoding branches for spectral imagery and each group of environmental variables.

We will include variables such as:

- Terrain: elevation, slope, aspect
- Climate: temperature, precipitation, humidity, solar radiation
- Geology: soil, watercourse proximity

Implement cross-attention mechanisms between spectral and environmental features to enable inter-modal relationships. Conduct ablation studies removing individual environmental variables to quantify their contribution. Compare against baseline models using stacked preprocessing and single-encoder approaches.  

##### Key innovations

This research will pioneer true multimodal vegetation segmentation models, moving beyond simple data stacking. Additionally, we will quantify the relative importance of environmental context compared to spectral information for species detection. Lastly, this research will determine how models integrate ecological knowledge, potentially revealing new ecological insights about species-environment relationships.

#### Chapter 5 - Paper 4

##### Problem statement

Climate change poses significant threats to Tasmania's endemic species, but current vulnerability assessments rely on coarse distribution data. The detailed segmentation maps from previous chapters provide unprecedented spatial resolution for species inventories. However, translating these high-resolution distributions into actionable conservation priorities requires integrating climate projections, fire risk models, and landscape connectivity metrics.

##### Proposed method

Apply optimised segmentation models from Chapters 3-4 to generate comprehensive species inventories across Tasmania. Integrate downscaled climate projections (temperature, precipitation, fire weather indices) for 2030, 2050, and 2070 scenarios. Develop spatially-explicit vulnerability indices combining exposure (climate change magnitude), sensitivity (species traits), and adaptive capacity (connectivity, refugia). Implement graph-based connectivity analysis to identify critical corridors and climate refugia. Generate priority maps for conservation intervention.

##### Key innovations

Create the first high-resolution, deep learning-derived vulnerability assessment for Tasmanian endemic conifers. Develop novel metrics linking segmentation uncertainty to conservation planning confidence. Demonstrate the cascade from methodological advances (Chapters 2-4) to real-world conservation outcomes, establishing a reproducible framework for climate adaptation planning.

#### Chapter 6: Synthesis and Conclusion

This chapter will conclude the thesis by highlighting the key findings of the analysis chapters, how they address the research objectives, and their contributions to the broader field. It critically reflects on the study’s implications, limitations, and the significance of the results. Finally, it offers recommendations for future research, practical applications, and summarises the overall impact of the work.

## Timeline

- [ ] TODO

## Resources and Budget

- [ ] TODO

## Data Management and Ethics

- All remote sensing and field data will be transferred to the TerraLuma data directory on the UTAS Share Drive (R:/CoSE/GPSS/TerraLuma/_data). Including copies of the raw data and processing milestones.
- Working datasets will be saved on an external SSD drive and with routine (weekly) backups to an additional location on the UTAS Share Drive (R:/).
- Manuscripts will be stored in a combination of a UTAS OneDrive account, Overleaf, and GitHub.
- Code for data processing and analysis will be stored remotely on GitHub.
- Trained models will be stored on GitHub or Hugging Face.

Official Data Management Plan attached in Appendix 2.

Research Data Portal Management Plan ID: 703

## Risk Assessment and Contingencies

- [ ] TODO

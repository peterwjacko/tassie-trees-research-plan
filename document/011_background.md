---
title: Background
numbering:
  enumerator: 1.%s
---

## Patterns of ecosystem vulnerability in Tasmania

The impact of human activity on the natural environment is far-reaching,
rapid, and undeniable [@crutzenAnthropocene2006;
@steffenAnthropoceneAreHumans2021]. Consequently, there is an urgent
global imperative for comprehensive ecosystem monitoring at scales
necessary for effective conservation management
[@farriorDominanceSuppressedPowerlaw2016;
@keppelCapacityRefugiaConservation2015]. This challenge is
particularly acute for endemic species, which often occupy restricted
habitats and exhibit limited adaptive capacity to environmental change,
yet conservation assessments for endemic species remain inadequate
globally [@gallagherGlobalShortfallsThreat2023]. The persistence of
ancient lineages in geographically restricted refugia represents a
critical conservation priority, as these climatically stable areas
function as both evolutionary museums and potential sources for future
biotic radiation [@caiClimaticStabilityGeological2023;
@harrisonEndemismHotspotsAre2017;
@jetzCoincidenceRarityRichness2004]. Understanding these systems is
increasingly urgent given the theory of alternative stable states, where
ecosystems may be unable to return to their original ecological
condition once critical thresholds are exceeded
[@lamotheLinkingBallandcupAnalogy2019].

Tasmania exemplifies global patterns of paleoendemism, harbouring
exceptional concentrations of ancient lineages with highly restricted
contemporary distributions. The island's temperate vegetation
communities include many iconic paleoendemic species such as
*Lagarostrobos franklinii* (Huon pine), *Athrotaxis selaginoides* (King
Billy pine), *Athrotaxis cupressoides* (Pencil pine), and *Nothofagus
gunnii* (tanglefoot beech). While *Nothofagus cunninghamii* (Myrtle
beech) is not endemic to Tasmania, it shares many similar
characteristics and habitat with the endemics. These species represent
broader patterns of Tasmanian paleoendemism, persisting through the use
of different climate refugia strategies: wet rainforest refugia support
Huon pine and Myrtle beech [@buckleyChangingTemperatureResponse1997;
@drewDynamicsSeasonalGrowth2022;
@lindenmayerFactorsAffectingPresence2000], while cool alpine
environments provide habitat for tanglefoot beech and *Athrotaxis*
species. Both *Athrotaxis* and *Lagarostrobos* are exceptionally long
lived but with extremely slow growth rates
[@allen1700yearAthrotaxisSelaginoides2017;
@allenPotentialReconstructBroadscale2011;
@gibsonDescriptionHuonPine1988;
@gibsonConservationManagementHuon1986].

Despite these species persisting for millions of years, their slow
growth rates and poor dispersal confine them to refugial habitats.
Historical anthropogenic impacts have disrupted this delicate balance
through intensive logging, habitat inundation from hydroelectric
development, and altered fire regimes
[@horneEcologicalSensitivityAustralian1991]. Contemporary climate
change compounds these pressures through warming and drying trends that
increase fire risk and penetrate historically fire-free refugia
[@bowmanFireCausedDemographic2019; @holzPopulationCollapseRetreat2020;
@worthFireMajorDriver2017]. Evidence of local extinctions and
population collapses demonstrates the vulnerability of these
slow-growing species to changing fire regimes
[@blissLackReliablePostfire2021; @bowman2016TasmanianWilderness2021;
@fletcherChangingRoleFire2018]. Additional stressors such as habitat
fragmentation and introduced pathogens like *Phytophthora* further
compromise population viability
[@khaliqPhytophthoraSpeciesIsolated2019]. The combination of
historical population reduction and accelerated environmental change has
created conditions where slow-growing species lack sufficient time for
natural recruitment and recovery
[@coleRecoveryResilienceTropical2014], highlighting the critical need
for precise spatial monitoring of species distributions and habitat
condition.

## Identifying and quantifying vulnerable areas

Current vegetation mapping approaches employed by Natural Resources and
Environment Tasmania (NRE Tasmania) reflect methodological constraints
that limit their utility for contemporary conservation challenges. The
primary approach relies on manual interpretation of aerial photography,
utilising limited spectral information and subjective visual cues to
delineate vegetation boundaries
[@departmentofnaturalresourcesandenvironmenttasmaniaTASVEG402020].
Critically, the resources required by these approaches limit the
frequency at which the mapping can be updated. For example, the most
recent TASVEG dataset, v5.0 released in 2025 represents the first major
update since 2010 and an average of five years between major versions
since 2004
[@departmentofnaturalresourcesandenvironmenttasmaniaTASVEG502025].
This temporal lag prevents detection of rapid changes in population
extent or condition, particularly problematic when current distributions
may represent ecological "echoes" of past conditions where recruitment
of new individuals is no longer possible due to altered fire regimes
[@keppelCapacityRefugiaConservation2015]. Spatial resolution
limitations force reliance on community-level classifications rather
than species-level discrimination, masking important ecological patterns
within populations and compromising targeted management interventions.

Ground validation protocols introduce systematic sampling bias through
preferential access to readily accessible areas, typically excluding
remote terrain where many endemic populations persist
[@burgObservationBiasIts2015; @clarkeNondetectionErrorsSurvey2012;
@morrisonObserverErrorVegetation2016]. The labour-intensive nature of
manual interpretation creates scalability constraints, limiting
monitoring frequency and extent. Additionally, these approaches provide
little to no information about vegetation health, demographic structure,
population trends, and neglect the value significant individual trees.
These attributes are critical to adaptive conservation planning given
that old and large individual trees are essential to ecosystem health
[@lindenmayerGlobalDeclineLarge2012; @lindenmayerNewPoliciesOld2014],
population size data are necessary for designing effective conservation
areas [@burgmanMethodSettingSize2001], and the quality of presence
data directly affects species distribution modelling accuracy
[@feiQualityPresenceData2016].

## The promise of remote sensing and machine learning for ecosystem monitoring

Remote sensing revolutionised automated ecosystem monitoring and at
broader spatial scales than possible with traditional field methods
[@roughgardenWhatDoesRemote1991]. Early vegetation mapping
applications utilised broad-band multispectral sensors such as Landsat
and SPOT imagery [@rouseMonitoringVegetationSystems1973;
@rousejrThreeExamplesApplied1975], achieving reasonable success for
broad vegetation class discrimination. However, the spatial resolution
of the datasets limited the types of objects that could be discriminated
in scenes with high spectral variance such as forests
[@woodcockFactorScaleRemote1987]. Both Fisher
[@fisherPixelSnareDelusion1997] and Cracknell
[@cracknellReviewArticleSynergy1998] stressed the importance the
pixel-object relationship, and the problem of mixed signals of sub-IFOV
objects. Treitz and Howarth [@treitzHighSpatialResolution2000] found
that the spatial variation of the classes must be resolvable in the
imagery and that multiple spatial scales should be considered when
aiming to discriminate forest ecosystems in multispectral imagery.
Similarly, Cochrane [@cochraneUsingVegetationReflectance2000]
demonstrated that spectral responses in vegetation are "non-unique" in
hyperspectral data with a 10 m spatial resolution, and suggests that
multiple high spatial resolution samples from a single individual may
mitigate this problem.

The pixel-based approach to classification is not suitable for high
spatial resolution imagery, where within-class spectral variance can
exceeded between-class differences due to shadowing, illumination
effects, and sub-pixel heterogeneity
[@wulderHighSpatialResolution2004]. Object-based image analysis (OBIA)
addressed some of these limitations by accounting for the spatial
characteristics of a target [@blaschkeGeographicObjectbasedImage2014;
@blaschkeObjectBasedImage2010]. Treating the target as an object
captures the within-class spectral variability mitigates the so called
"salt and pepper" effect when using pixel-based classification methods
in high resolution imagery [@yuObjectbasedDetailedVegetation2006].
OBIA outperforms pixel-based approaches for vegetation discrimination
tasks in very high-resolution imagery in many cases
[@immitzerTreeSpeciesClassification2012;
@sibaruddinComparisonPixelbasedObjectbased2018]. However, Dingle
Robertson and King [@dinglerobertsonComparisonPixelObjectbased2011]
found no significant difference between the two approaches, emphasising
that the performance of OBIA greatly depends on an effective
segmentation and feature engineering.

Machine learning approaches, such as Random Forest (RF) and Support
Vector Machine (SVM) algorithms, improved classification accuracy over
the physically-based Spectral Angle Mapper (SAM) in early demonstrations
[@clarkHyperspectralDiscriminationTropical2005] in both pixel and
object-based approaches. While a data driven approach significantly
improved the accuracy of species discrimination, these techniques
struggled with the multi-scale spatial-spectral characteristics of
organic targets such as vegetation
[@dinglerobertsonComparisonPixelObjectbased2011].

## The rise of deep neural networks and representation learning in remote sensing

The advent of deep neural networks fundamentally transformed computer
vision through the introduction of representation learning, where the
algorithm automatically discovers hierarchical features directly from
data without manual feature engineering [@lecunDeepLearning2015].
Convolutional neural networks (CNNs) revolutionised dense segmentation
tasks through architectures such as fully convolutional networks
[@longFullyConvolutionalNetworks2015] and U-Net
[@ronnebergerUNetConvolutionalNetworks2015]. More recently, Vision
Transformers (ViTs) have demonstrated superior performance compared to
CNNs in image classification tasks but require much larger datasets to
avoid overfitting [@dosovitskiyImageWorth16x162020]. These learned
representations consistently outperform engineered features by capturing
complex spatial-spectral patterns that are difficult to encode manually,
particularly for fine-grained species discrimination
[@zhongReviewTreeSpecies2024]. However, the substantial data
requirements of deep learning models initially posed significant
challenges for remote sensing applications, where labelled training data
is often scarce and expensive to acquire.

Deep learning has demonstrated remarkable success in tree species
segmentation by automatically learning hierarchical spatial-spectral
features that capture complex patterns invisible to traditional methods.
Notable achievements include the mapping of over 1.8 billion individual
trees across 1.3 million km² using U-Net architectures with satellite
imagery [@brandtUnexpectedlyLargeCount2020], and fine-grained
vegetation mapping achieving 84% accuracy from high-resolution RGB
imagery alone [@kattenbornConvolutionalNeuralNetworks2019].
Three-dimensional convolutional neural networks (3D-CNNs) have proven
particularly effective for hyperspectral data, simultaneously exploiting
both spatial context and spectral relationships to achieve
classification accuracies exceeding 95%
[@zhangThreedimensionalConvolutionalNeural2020]. However, these
advances come with significant challenges: deep learning models require
vast amounts of training data across diverse acquisition conditions
[@brandtUnexpectedlyLargeCount2020;
@brandtHighresolutionSensorsDeep2025], suffer from limited
interpretability as "black box" systems, and often struggle with
generalisation beyond their training domains.

The challenge of model transferability across different sensors,
geographic locations, and temporal conditions represents a critical
bottleneck in operational remote sensing applications. Domain shift,
arising from sensor characteristics, atmospheric conditions, seasonal
variations, and geographic differences, can severely compromise model
performance when deployed beyond training conditions
[@brandtHighresolutionSensorsDeep2025]. Spatial autocorrelation in
training data further exacerbates this issue, with studies demonstrating
that violations of spatial independence can inflate apparent model
performance by up to 30%, leading to overly optimistic assessments of
generalisation capability
[@kattenbornSpatiallyAutocorrelatedTraining2022]. Knowledge
distillation (KD) has emerged as a promising solution for cross-sensor
learning, enabling the transfer of knowledge from high-fidelity (spatial
and spectral) teacher models to lower-fidelity student networks
[@himeurApplicationsKnowledgeDistillation2025]. @shinMultispectraltoRGBKnowledgeDistillation2023 showed that KD from
a MS-trained teacher model improves the accuracy of a RGB-trained
student model by approximately 2% (OA = 94.04%). However, it is
necessary to highlight that the teacher and student models in @shinMultispectraltoRGBKnowledgeDistillation2023 share the
same RGB dataset which is a spectral subset of the Sentinel-2 based
EuroSAT dataset [@helberEuroSATNovelDataset2019]. The teacher uses
multiple modalities with an encoder branch for: RGB, NIR, RE, SWIR,
whereas the student uses a single encoder branch: RGB.

Multimodal data fusion is a critical advancement beyond single-sensor
approaches, combining complementary information from spectral,
structural, and temporal domains to enhance species discrimination
capabilities. True multimodal fusion extends beyond feature-level fusion
(data stacking) [@zhongReviewTreeSpecies2024], towards architectures
that process each modality through dedicated pathways before
integration. Late-fusion strategies, where modality-specific streams are
processed independently at their native resolutions before final
combination, have demonstrated superior performance in species
classification tasks compared to unimodal-multi-source models
[@hongMoreDiverseMeans2021; @tielMultiscaleMultimodalSpecies2025].
While these approaches have demonstrated the value of integrating
multi-source remote sensing data, the true potential of multimodality is
in the ability to integrate symbolic or contextual information
[@baltrusaitisMultimodalMachineLearning2019]. This can be by
integrating OpenStreetMap information [@hongMoreDiverseMeans2021], or
semantic vegetation attributes and hierarchical taxonomy
[@sumbulFinegrainedObjectRecognition2018]. @harmonImprovingRareTree2023 demonstrates that incorporating domain
knowledge through rule-based constraints improves the classification of
rare tree species in RGB imagery.

The integration of ecological understanding and environmental context is
a paradigm shift from pure computer vision approaches towards
ecologically informed deep learning models. By incorporating
environmental variables such as climate, soil properties, and
topographic characteristics, these models can leverage the fundamental
ecological principle that species distributions are constrained by
environmental niches and habitat suitability
[@brodrickUncoveringEcologicalPatterns2019]. This approach enables
DNNs to move beyond simple biophysical component identification towards
the direct recognition of ecological patterns and processes at scales
previously impossible to consider
[@brodrickUncoveringEcologicalPatterns2019]. The combination of remote
sensing imagery and environmental datasets in multimodal DNNs has used
to improve and finding patterns in SDMs at a regional scale
[@ryoExplainableArtificialIntelligence2021;
@tielMultiscaleMultimodalSpecies2025], but there is limited research
on how this information can be exploited for species segmentation tasks.

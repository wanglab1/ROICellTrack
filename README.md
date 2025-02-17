# ROICellTrack

<p align="center">
  <img width="240"  src="https://github.com/wanglab1/ROICellTrack/blob/main/misc/logo.png">
</p>

A toolkit for advanced cellular and subcellular analysis using GeoMx ROI images

## Overview
Mini-bulk or single-spot spatial transcriptomic technologies, such as GeoMX Digital Spatial Profiler (DSP), have revolutionized our ability to probe spatial heterogeneity and examine transcripts at a subcellular level. However, in most GeoMX DSP studies, the spatial information obtained from multiplex immunofluorescence imaging has been primarily used for identifying the regions of interest (ROI), rather than as an integral part of the downstream transcriptomic data interpretation. To fix this missed opportunity, we developed an analytical framework to fully leverage the rich spatial context provided by the in situ imaging modality. The toolkit has two main functionalities. (1) ROI cropping and cell segmentation: the toolkit enables the automated cropping of ROI images, followed by a cell segmentation process utilizing a multi-color-optimized deep learning model pre-trained based on the TissueNet. (2) Cell typing and integrative spatial analysis: the pipeline extracts cell-level morphological features (e.g. cell size and circularity), and AI-driven characteristics. 

## Pipeline structure
<pre>
<code>
(ROICellTrack)
    └──Pipeline
       ├── A. ROI cropping and processing 
       ├── B. ROI visualization
       ├── C. ROI cell segmentation
       └── D. Spatial statistics (CKI) calculation
</code>
Instructions and examples can be found at each pipeline folder. 
</pre>

## Installation and requirements
  Please create a local folder named ROICellTrack and download all the necessary files. Place the example data as well all python scripts directly in the main directory of ROICellTrack. Follow the example code in the Jupyter Notebook in each folder for implementations. 
  
  Required python packages:
  - opencv-python
  - cellpose (>2.0)
  - matplotlib
  - pillow (optional)
  - tifffile
  - seaborn
  - scikit-learn
  - pandas

  R packages (only needed for CKI calculation):
  - spatstat
  - pracma
  - ggplot2

## References
Song X, Yu X, Moran-Segura CM, Li T, Davis JT, Grass GD, Li R, and Wang X. ROICellTrack: A deep learning framework for harnessing cellular imaging modalities in subcellular spatial transcriptomic profiling of tumor tissues. (Manuscript Under Revision). 

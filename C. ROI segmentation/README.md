## Main modules of ROICellTrack

1. For single sample processing, please follow [`StepC_CellSeg_single_sample.ipynb`](https://github.com/wanglab1/ROICellTrack/blob/35c5587b057afd5fb5210347406f74b118546149/C.%20ROI%20segmentation/StepC_CellSeg_single_sample.ipynb) (Also outputs cell-level morphological features *cell_stat*, which are useful for downstream analysis). 

2. For multiple samples, please follow `StepC_CellSeg_segmenation_batch.py` (need to specify *input_dir* and *output_dir*)

3. For cases where mask file is used to call positive cells, please follow [`StepC_CellSeg_ss_mask_pos.ipynb`](https://github.com/wanglab1/ROICellTrack/blob/1adaae763c8ef0f10c689d6d09e7a09a4fb64906/C.%20ROI%20segmentation/StepC_CellSeg_ss_mask_pos.ipynb). This is very useful when the positive cells cannot be called easily based on RGB colors (such as yellow or pink colors).

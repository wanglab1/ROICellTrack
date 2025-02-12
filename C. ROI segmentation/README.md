1. For single sample processing, please follow `StepC_CellSeg_single_sample.ipynb` (Also outputs cell-level morphological features *cell_stat*, which are useful for downstream analysis). 

2. For multiple samples, please follow `StepC_CellSeg_segmenation_batch.py` (need to specify *input_dir* and *output_dir*)

3. For cases where mask file is used to call positive cells, please follow `StepC_CellSeg_ss_mask_pos.ipynb`. This is very useful when the positive cells cannot be called easily based on RGB colors.

## Notes on Using QuPath for GeoMx ROI Image Segmentation

QuPath offers an interactive and alternative approach to cell segmentation. There are a few important considerations when using QuPath for GeoMx ROI image segmentation:

1. Pixel Width and Height Adjustment

- Pixel width and Pixel height must be adjusted to ensure accurate scaling and alignment with the ROI image.
- For GeoMx ROI outputs, a pixel size of 0.40 µm is recommended.

2. Key Parameters in "Positive Cell Detection"

- The Threshold in the Intensity parameters is the primary tuning parameter; a value of 15 was used in analyzing the public data this study.
- The Intensity threshold parameters for "Threshold 1+", "2+" should also be fine-tuned. Suggested values include 10/20/30 or 20/30/40.

3. Comparison with cellpose

- QuPath tends to detect fewer cells compared to Cellpose.
- Cells near the ROI margins are more likely to be falsely classified as positive. For example, the resuts shown in the screenshot below. 



<p align="center">
  <img width="700"  src="https://github.com/wanglab1/ROICellTrack/blob/main/misc/Qupath_example1.jpg">
</p>

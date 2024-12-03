# Object-Detection-with-Feature-Extraction
This project addresses the challenge of object detection, a core problem in computer vision that has evolved significantly with the advent of deep learning. While modern approaches leverage convolutional neural networks (CNNs) for improved accuracy, this project focuses on understanding and implementing a classic two-stage object detection framework using Local Binary Patterns (LBP) and other feature extraction techniques.

## Project Goals

### Feature Extraction with LBP:

The primary goal is to explore the use of LBP for extracting features from proposed regions of interest (ROIs). A key challenge is ensuring that the feature vector length remains constant, regardless of the region size, while maintaining high-speed feature extraction.

### Keypoint-Based Feature Methods:

Evaluate the feasibility and effectiveness of using keypoint-based methods like SIFT for feature extraction from ROIs.

### Classifier Training and Evaluation:

Complete and refine the provided code to train a classifier on the extracted features. Test the classifier on a dataset and analyze its performance, identifying any significant weaknesses.

### Integration of Regression Models (Bonus Task):

Discuss the importance of regression models in RCNN for precise object localization. Add a similar regression mechanism to your algorithm, potentially using a single model instead of multiple class-specific models.

### Non-Maximum Suppression (NMS):

Understand the role of NMS in eliminating redundant detections during post-processing to ensure the most relevant bounding boxes are retained.
(Note: No implementation is required for this step.)

## Dataset and Guideline Overview
The dataset provided contains approximately 200 images from the popular game Counter-Strike ([Counter-Strike Dataset](https://www.kaggle.com/datasets/lstmkirigaya/cstrike-detection)), labeled in the YOLO format. The dataset and the necessary scripts for reading and preparing the data are included.

The project follows a two-stage object detection framework, one of the earliest and most effective approaches. The steps are as follows:

### Region Proposal:

Generate candidate regions (ROIs) using a selective search algorithm, significantly reducing the number of regions compared to sliding window methods.

### Ground Truth Assignment:

Assign ground truth labels to the proposed regions using the IoU (Intersection over Union) criterion.

### Feature Extraction:

Extract features from the proposed regions using LBP and optionally other descriptors like HoG. Ensure consistent feature vector lengths across regions.

### Classifier Training:

Train a classifier, such as an SVM, using the extracted features to distinguish objects from the background.

### Testing and Output:

Apply the trained model to new images, classify the proposed regions, and display the detected objects with their labels on the original images.
## Project Tasks:

### 1. Feature Extraction with LBP:

Explore how to use LBP features for region proposals while ensuring feature vectors remain consistent in length, regardless of region size.
Emphasize fast feature extraction to enhance performance.

### 2. Evaluating Keypoint-Based Methods:

Assess whether keypoint-based feature extractors, like SIFT, are suitable for region proposals and their impact on detection accuracy.

### 3. Model Training and Testing:

Complete the provided code to train a classifier using the extracted features.
Evaluate the model’s performance on a test dataset and identify key weaknesses in the results.

### 4. Integration of Regression Models (Bonus Task):

Implement a regression model similar to RCNN for refining object localization.
Discuss the significance of regression models in object detection.

### 5. Non-Maximum Suppression:

Explain the role of Non-Maximum Suppression (NMS) in eliminating redundant detections during the final stage of the algorithm.
(No implementation required.)  

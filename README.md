# Object Detection with Feature Extraction
This project addresses the challenge of object detection, a core problem in computer vision that has evolved significantly with the advent of deep learning. While modern approaches leverage convolutional neural networks (CNNs) for improved accuracy, this project focuses on understanding and implementing a classic two-stage object detection framework using Local Binary Patterns (LBP) and other feature extraction techniques.

# Content
- Table of Contents
  * [Project Goals](#Project-Goals) 
  * [Dataset and Guideline Overview](#Dataset-and-Guideline-Overview)  
  * [Project Tasks](#Project-Tasks)
  * [METHOD](#Method)
    
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
## Project Tasks

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

## Method

### Task 1: Feature Extraction Using LBP (Local Binary Patterns)
In this task, I used LBP to extract features from proposed regions in the image. For each pixel in a region, I calculated the binary pattern by comparing the intensity of the central pixel with its surrounding neighbors. If a neighbor’s intensity was greater than or equal to the central pixel, it was assigned a 1; otherwise, it was assigned a 0. This binary sequence was then converted into a decimal number, creating an LBP code for the pixel.

To ensure consistent feature lengths across regions of varying sizes, I computed histograms of the LBP values. These histograms, normalized to maintain uniform dimensions, served as the feature vectors for training the classifier.

<img style="width:400px" src="https://github.com/user-attachments/assets/a7e84b98-855d-4ffa-b1e9-8286a8623b88"> 

The challenge was to maintain speed and efficiency while ensuring the robustness of the feature vectors against changes in illumination and texture. The results showed that LBP features effectively captured local texture information.


### Task 2: Evaluating Keypoint-Based Feature Extraction (SIFT)
Here, I explored the feasibility of using keypoint-based methods like SIFT for feature extraction from the proposed regions. SIFT detects distinct keypoints in an image and computes feature descriptors for each. However, a major challenge is that the number of keypoints varies across images, leading to inconsistent feature vector lengths.

To address this, I considered aggregating the keypoint descriptors or using pooling techniques to create fixed-length feature vectors. However, the inherent variability in the number of keypoints posed a limitation in applying SIFT directly for region-based feature extraction. While effective for tasks requiring sparse features, SIFT’s adaptability to dense region proposals was limited.


### Task 3: Completing Code and Training the Classifier

### Step-by-Step Breakdown

### Region Proposal Generation (Selective Search)

I used Selective Search to generate candidate regions (Region of Interest or ROIs) in the input images.
Selective Search hierarchically groups similar regions in the image based on texture, color, and size, providing fewer but more meaningful region proposals compared to sliding windows.
The generated proposals were rectangles with varying scales, ensuring coverage of potential object locations in the image.

<img style="width:225px" src="https://github.com/user-attachments/assets/0958413a-d2b7-4b8e-97f0-5c4ad31e3cd1">
<img style="width:200px" src="https://github.com/user-attachments/assets/fb4c6006-6dc0-4463-9002-1a5a7afd76be">
<img style="width:210px" src="https://github.com/user-attachments/assets/0bb81a6b-c0e1-4630-a55f-66b9317e0e1c">

### Feature Extraction with LBP

For each proposed region, I extracted LBP (Local Binary Pattern) features.
The LBP descriptor converts each region into a fixed-length feature vector by computing histograms of binary patterns for each pixel, capturing local texture information.
To handle varying sizes of regions, I ensured that all LBP histograms were normalized and of consistent length, allowing for direct comparison across regions.

<img style="width:450px" src="https://github.com/user-attachments/assets/d26b64da-3976-4efb-ab18-db94d77e88fc">
<img style="width:350px" src="https://github.com/user-attachments/assets/b733b94c-06f4-4131-9e9b-980367cf187c">

### Training the Classifier

I used a K-Nearest Neighbors (KNN) classifier to train on the extracted features.
The classifier assigned labels to each proposed region, distinguishing objects from the background and identifying object classes (e.g., weapon or background).
A five-class setup was used, including an additional background class to handle regions that did not contain objects.

### Handling Class Imbalance

Since background regions far outnumbered object regions, I applied undersampling to balance the dataset.
By selecting a limited number of background samples, I ensured that the classifier did not become biased toward predicting the background class.

### Testing and Evaluation

The trained classifier was tested on new images. For each test image:
Selective Search generated regions.
LBP features were extracted.
The trained classifier assigned labels to the regions.
I visualized the results by drawing bounding boxes around detected objects and labeling them with their predicted classes.

### Performance Analysis

The classifier achieved high accuracy, especially for well-defined objects like weapons.
Results showed that LBP was effective in distinguishing objects based on texture but struggled with overlapping objects or regions with low contrast.
Using additional features like color histograms and HoG improved classification results.

### Results:
<img style="width:500px" src="https://github.com/user-attachments/assets/e3b097fd-c932-46f6-ac92-13aa5e28bcf7"> <br>
<img style="width:500px" src="https://github.com/user-attachments/assets/a07ab57a-6909-4c86-a03d-3b6c5ff6624f"> <br>
<img style="width:500px" src="https://github.com/user-attachments/assets/ac246af7-db0d-4669-bbc5-8dd9f9dd93f3"> <br>
<img style="width:500px" src="https://github.com/user-attachments/assets/d467fa6b-f85e-4d13-993c-d43955e0b899"> 

### Task 4 (Bonus): Adding a Regression Model
I incorporated a regression model to refine object localization, inspired by the RCNN framework. The regression model predicted bounding box offsets to adjust the proposed regions, improving localization accuracy. Despite implementing this, the R² score was low, indicating that LBP features alone were insufficient for precise localization adjustments.

### Task 5: Non-Maximum Suppression (NMS)
In this task, I explained the role of Non-Maximum Suppression (NMS) in eliminating redundant bounding boxes. NMS selects the bounding box with the highest confidence score and suppresses overlapping boxes that have a high Intersection over Union (IoU) with the selected box. This step is crucial for reducing false positives and ensuring that only the most relevant detections are retained. 

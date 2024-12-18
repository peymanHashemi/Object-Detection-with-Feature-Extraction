from dataLoader import DataLoader
import skimage
from skimage.color import rgba2rgb, rgb2gray
import cv2
from skimage.feature import hog, haar_like_feature
from skimage.transform import integral_image
from os import listdir
from os.path import join, isfile
import numpy as np 
from utils import extract_candidates, extract_iou
from skimage.feature import local_binary_pattern
from tqdm import tqdm
from imblearn.under_sampling import RandomUnderSampler
from joblib import Parallel, delayed
import matplotlib.pyplot as plt

class DatasetGenerator():
    """
     This class is for creating the training dataset. the final goal is to create (features-target) pairs
     to train a classifier (extract_features_targets_pairs method), but before that, you need
     to prepare the dataset (prepareDataset).
     
     :param dataloader: The dataloader.
    """
    def __init__(self, dataloader):
        self.dataloader = dataloader
        self.image_paths,\
            self.gtBboxes,\
            self.classes,\
            self.deltas,\
            self.rois,\
            self.ious = [],[],[],[],[],[]

    """
     Extract the LBP from an image.
     
     :param image: The image to extract the LBP from.
     :param radius: See scikit-image's local_binary_pattern()
     :param n_points: See scikit-image's local_binary_pattern()
     :param method='uniform': See scikit-image's local_binary_pattern()
    """
    def extract_lbp(self, roi_image):
        lbp = local_binary_pattern(roi_image, 16, 3, method='uniform').astype('float32')
        lbp -= lbp.min()
        lbp /= lbp.max()
        hist, _ = np.histogram(lbp.ravel(), bins=16, range=(0, 1))
        hist = hist.astype("float")
        hist /= (hist.sum() + 1e-7)
        return hist
    
    """
     Extract features from a given ROI image.
     
     :param ?: ???
    """
    def extract_features_roi(self, image, roi):
        x1,y1,x2,y2 = roi
        roi_image = image[y1:y2, x1:x2]
        
        # return roi_image

        lbp_hist =  self.extract_lbp(roi_image)

        return lbp_hist

    """
     Prepares the dataset for training.
     
     :param load='dataset.npy': path to the dataset. If it's not the first time you
        call this method.
     :param save_path='dataset.npy': if you want to save the dataset, so you don't
        need to call this prolonged (!) method every time.
      Also, You can use the precomputed dataset.npy file if you think this method is slow :)
      https://drive.google.com/file/d/1SGJWgt3z6S44uo6GI9sFuX_WGvOoZ-8z/view?usp=sharing
      
    """
    def prepareDataset(self, load='dataset.npy', save_path='dataset.npy'):
        if not isfile(load): 
            print('Dataset not found! creating dataset for first time ...')
            self.prepareDataset_(save_path)
        else: 
            print('Loading Dataset ...')
            dataset = np.load(save_path ,allow_pickle='TRUE').item()
            self.image_paths = dataset['image_paths']
            self.gtBboxes = dataset['gtBboxes']
            self.classes = dataset['classes']
            self.deltas = dataset['deltas']
            self.rois = dataset['rois']
            self.ious = dataset['ious']
            print('Done')
            
    """
    I've already explained this in the homework description. Steps 1 and 2 of the proposed algorithm.
    self.delta is about the fourth question, which is optional; ignore it if you don't want to answer this question.
    
    
    """
    def prepareDataset_(self, save_path):
        
        def prepareSingleImage(data_dict):
            """
            From https://github.com/PacktPublishing/Modern-Computer-Vision-with-PyTorch
            """
            image = data_dict['image']
            gtbboxs = data_dict['bboxes']
            classes = data_dict['classes']
            image_path = data_dict['image_path']

            H, W, _ = image.shape
            candidates = extract_candidates(image)

            ious, rois, clss, deltas = [], [], [], []
            ious = np.array([[extract_iou(candidate, _bb_) for \
                candidate in candidates] for _bb_ in gtbboxs]).T
            
            for jx, candidate in enumerate(candidates):
                cx1,cy1,cx2,cy2 = candidate
                candidate_ious = ious[jx]
                best_iou_at = np.argmax(candidate_ious)
                best_iou = candidate_ious[best_iou_at]
                best_bb = _x1,_y1,_x2,_y2 = gtbboxs[best_iou_at]
                if best_iou > 0.7: clss.append(classes[best_iou_at])
                elif best_iou > 0.3: continue
                else : clss.append('0')
                delta = np.array([_x1-cx1, _y1-cy1, _x2-cx2, _y2-cy2])
                deltas.append(delta)
                rois.append(candidate)
                
                
            """ious, rois, clss, deltas are lists of corresponding items in one image,
            self.ious, self.rois, self.classes, self.deltas are lists of the above lists for all images."""     
            self.image_paths.append(image_path)
            self.ious.append(ious)
            self.rois.append(rois)
            self.classes.append(clss)
            self.deltas.append(deltas)
            self.gtBboxes.append(gtbboxs)
        
        # Use parallel computing. Call the above function on each image in the training dataset.
        Parallel(n_jobs=10, require='sharedmem')(delayed(prepareSingleImage)(data_dict)
                                                for ix, data_dict in tqdm(enumerate(self.dataloader.getAllTrainData()), total=len(self.dataloader.train_image_list)))            


        dataset = {'image_paths': self.image_paths,
                     'ious': self.ious, 
                     'rois': self.rois,
                     'classes': self.classes,
                     'deltas': self.deltas,
                     'gtBboxes': self.gtBboxes}
        np.save('dataset.npy', dataset)


    """
     Extract features-target pairs from all training data.
     
    """
    def extract_features_targets_pairs(self):
        features = []
        target_classes = []
        target_deltas = []
        """
        The number of negative samples is much more than positive samples,
            So it would help if you did UnderSampling to avoid bias in the classifier.
        """
        rus = RandomUnderSampler(random_state=42)
        for image_path, image_rois, image_classes, image_deltas in \
            tqdm(zip(self.image_paths, self.rois, self.classes, self.deltas), total=len(self.image_paths)):
            
            """
            Some images have only negative samples(background). Just simply ignore them.
            """
            if len(np.unique(image_classes)) == 1:
                continue

            array_to_undersample = np.hstack((image_rois, image_deltas))
            image_rois_image_deltas, image_classes = rus.fit_resample(array_to_undersample, image_classes)
            image_rois, image_deltas = image_rois_image_deltas[:,:4], image_rois_image_deltas[:,4:]
            # print(">", "../"+image_path)
            image = rgb2gray(rgba2rgb(skimage.io.imread("../"+image_path)))
            """
            After converting ROIS coordinates to int, some of them may have an area of zero.
                In such cases, some feature extractors may raise a ValueError. 
                We Ignore these ROIs.
            """
            res = Parallel(n_jobs=-1, require='sharedmem')([delayed(self.extract_features_roi)(image, image_rois[i])
                                                for i in range(len(image_rois))])
            for i in range(len(image_rois)):
                features.append(res[i])
                target_classes.append(image_classes[i])
                target_deltas.append(image_deltas[i])

        return features, target_classes, target_deltas, image_rois

if __name__ == '__main__':
    dl = DataLoader()
    print(dl.classes)
    dg = DatasetGenerator(dl)
    dg.prepareDataset()
    "visualize An image and its rois."
    data_dict = {}
    data_dict['image'] = skimage.io.imread(dg.image_paths[5])
    data_dict['bboxes'] = np.array(dg.rois[5])
    data_dict['classes'] = np.array(dg.classes[5])
    dl.visualize(data_dict)
    plt.show()


# Make this code parallel
# for i in range(len(image_rois)):
#                 try:
#                     # You should define this method
#                     feat = self.extract_features_roi(image, image_rois[i])
#                 except ValueError:
#                     continue
#                 features.append(feat)
#                 target_classes.append(image_classes[i])
#                 target_deltas.append(image_deltas[i])

# Make it parallel
# Parallel(n_jobs=10, require='sharedmem')(delayed(self.extract_features_roi)(image, image_rois[i])
#                                                 for i in range(len(image_rois)))

import selectivesearch
import numpy as np
import matplotlib.pyplot as plt

"""From https://github.com/PacktPublishing/Modern-Computer-Vision-with-PyTorch"""
def extract_candidates(img):
    img_lbl,regions = selectivesearch.selective_search(img, scale=200, min_size=20)
    img_area = np.prod(img.shape[:2])
    candidates = []
    for r in regions:
        if r['rect'] in candidates: continue
        if r['size'] < (0.001*img_area): continue
        if r['size'] > (1*img_area): continue
        x, y, w, h = r['rect']
        candidates.append(list(r['rect']))
    candidates = np.array([(x,y,x+w,y+h) for x,y,w,h in candidates])
    return candidates.astype(int)

"""From https://github.com/PacktPublishing/Modern-Computer-Vision-with-PyTorch"""
def extract_iou(boxA, boxB, epsilon=1e-5):
    x1 = max(boxA[0], boxB[0])
    y1 = max(boxA[1], boxB[1])
    x2 = min(boxA[2], boxB[2])
    y2 = min(boxA[3], boxB[3])
    width = (x2 - x1)
    height = (y2 - y1)

    if (width<0) or (height <0):
        return 0.0
    area_overlap = width * height
    area_a = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    area_b = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    area_combined = area_a + area_b - area_overlap
    iou = area_overlap / (area_combined+epsilon)
    return iou

if __name__ == "__main__":
    from dataLoader import DataLoader
    dl = DataLoader()
    for img in dl.getAllTestData():
        candidates = extract_candidates(img)
        dl.visualize({"image": img, "classes":np.zeros(len(candidates)), "bboxes": candidates})
        plt.show()
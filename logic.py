import numpy as np
import cv2
from skimage.color import rgb2gray
from skimage import io
from skimage.measure import shannon_entropy
import joblib

class CurrencyDetector:
    def __init__(self, model_path):
        """Initialize the detector with a trained model"""
        try:
            self.model = joblib.load(model_path)
            print("Loaded model successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            
    def extract_sobel_features(self, image_path):
        """
        Load an image from disk, convert to grayscale,
        apply Sobel edge detection, then compute
        variance, skewness, kurtosis, and entropy.
        Returns a 1×4 feature list.
        """
        # 1. Read and grayscale
        img = io.imread(image_path)
        if img.ndim == 3:
            img = rgb2gray(img)
        # 2. Resize to 400×400 (or your training size)
        img = cv2.resize(img, (400, 400))
        # 3. Sobel in X and Y
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        grad = np.hypot(sobel_x, sobel_y)
        # 4. Compute statistical features
        var = np.var(grad)
        skew = np.mean(((grad - grad.mean())/grad.std())**3)
        kurt = np.mean(((grad - grad.mean())/grad.std())**4) - 3
        ent = shannon_entropy(grad)
        return np.array([[var, skew, kurt, ent]])

    def process_image(self, image_path):
        """Process image and return edge detection result"""
        img = io.imread(image_path)
        if img.ndim == 3:
            img = rgb2gray(img)
        img = cv2.resize(img, (400, 400))
        
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        grad = np.hypot(sobel_x, sobel_y)
        
        # Normalize for display
        grad_norm = (grad * 255.0 / grad.max()).astype(np.uint8)
        return grad_norm

    def predict_banknote(self, image_path):
        """
        Given a file path, extract Sobel features,
        apply the loaded model, and return prediction details.
        """
        if self.model is None:
            return None, None, None
            
        features = self.extract_sobel_features(image_path)
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        confidence = max(probabilities) * 100
        
        result = "FAKE banknote" if prediction == 1 else "REAL banknote"
        return result, confidence, features[0] 
import torch
from torchvision import transforms
from PIL import Image
from model import CNN

class ModelEvaluator:
    MODEL_PATH = '/home/LaszloPota/Desktop/Thesis/app/model.pth'
    
    def __init__(self):
        """Initializes the model, loads weights, and sets up preprocessing."""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = CNN()
        self.model.to(self.device)
        self.model.load_state_dict(torch.load(self.MODEL_PATH, map_location=self.device))
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5], std=[0.5])
        ])
    
    def evaluate(self, image):
        """Evaluates the model on an image and returns the classification result."""
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            outputs = self.model(image_tensor)
            _, predicted = torch.max(outputs.data, 1)
        
        result = "OK" if predicted.item() == 0 else "NOK"
        confidence = torch.softmax(outputs, dim=1)[0][predicted.item()].item() * 100
        return result, confidence

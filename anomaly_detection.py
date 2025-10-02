import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from config import ANOMALY_THRESHOLD
import os

class Autoencoder(nn.Module):
    def __init__(self, input_dim, latent_dim=3):
        super().__init__()
        self.encoder = nn.Sequential(nn.Linear(input_dim, 32), nn.ReLU(), nn.Linear(32, latent_dim))
        self.decoder = nn.Sequential(nn.Linear(latent_dim, 32), nn.ReLU(), nn.Linear(32, input_dim), nn.Sigmoid())

    def forward(self, x):
        return self.decoder(self.encoder(x))

def train_model(features, model_path='models/autoencoder.pth'):
    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # Try to load existing model
    try:
        if os.path.exists(model_path):
            return torch.load(model_path)
    except Exception as e:
        print(f"Failed to load model: {e}. Retraining...")
    
    # Train new model
    train_tensor = torch.from_numpy(features).float()
    loader = DataLoader(train_tensor, batch_size=32, shuffle=True)
    model = Autoencoder(input_dim=features.shape[1])
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    for epoch in range(50):
        for batch in loader:
            output = model(batch)
            loss = criterion(output, batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    # Save the model
    torch.save(model, model_path)
    return model

def detect_anomalies(model, features):
    test_tensor = torch.from_numpy(features).float()
    with torch.no_grad():
        outputs = model(test_tensor)
        errors = torch.mean((outputs - test_tensor)**2, dim=1).numpy()
    return errors > ANOMALY_THRESHOLD, errors
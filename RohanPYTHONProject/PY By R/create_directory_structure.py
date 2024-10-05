import os

# Define the base directory for the dataset
base_dir = 'data/train'

# Define the class names
classes = ['class_1', 'class_2']

# Create the base directory
os.makedirs(base_dir, exist_ok=True)

# Create subdirectories for each class
for class_name in classes:
    os.makedirs(os.path.join(base_dir, class_name), exist_ok=True)

print(f"Directory structure created at: {os.path.abspath(base_dir)}")
from PIL import Image

# Define the number of placeholder images to create for each class
num_images = 5

for class_name in classes:
    for i in range(num_images):
        # Create a new image
        img = Image.new('RGB', (224, 224), color=(73, 109, 137))

        # Save the image in the corresponding class directory
        img.save(os.path.join(base_dir, class_name, f'placeholder_{i + 1}.jpg'))

print("Placeholder images created.")
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Create an ImageDataGenerator instance for loading and preprocessing images
train_datagen = ImageDataGenerator(rescale=1./255)  # Rescale pixel values to [0, 1]

# Load images from the 'data/train' directory
train_generator = train_datagen.flow_from_directory(
    'data/train',              # Directory with training images
    target_size=(224, 224),   # Resize images to (224, 224)
    batch_size=32,            # Number of images to return in each batch
    class_mode='binary'       # Type of label arrays (binary or categorical)
)

# Print the class indices to verify
print("Class indices:", train_generator.class_indices)

# Optional: Display a batch of images
import matplotlib.pyplot as plt

# Get a batch of images and labels
images, labels = next(train_generator)

# Plot the first 5 images in the batch
plt.figure(figsize=(10, 10))
for i in range(5):
    plt.subplot(1, 5, i + 1)
    plt.imshow(images[i])  # Display image
    plt.title(f"Label: {labels[i]}")
    plt.axis('off')
plt.show()

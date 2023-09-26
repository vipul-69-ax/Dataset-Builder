import os
from tensorflow_hub import load
from PIL import Image
import numpy as np
from tensorflow import squeeze, expand_dims, config, image, convert_to_tensor, cast, float32, clip_by_value, uint8, io

# Limit GPU memory growth
gpus = config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

def preprocess_image(image_path):
    hr_image = image.decode_image(io.read_file(image_path))
    if hr_image.shape[-1] == 4:
        hr_image = hr_image[..., :-1]
    hr_size = (convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
    hr_image = image.crop_to_bounding_box(
        hr_image, 0, 0, hr_size[0], hr_size[1])
    hr_image = cast(hr_image, float32)
    return expand_dims(hr_image, 0)


def final_process(image, title=""):
    image = np.asarray(image)
    image = clip_by_value(image, 0, 255)
    image = Image.fromarray(cast(image, uint8).numpy())
    return image


model = load("https://tfhub.dev/captain-pool/esrgan-tf2/1")


def enhance_images(path):
    images = os.listdir(path)
    images = [os.path.join(path, image) for image in images]
    images = [preprocess_image(image) for image in images]
    images = [model(image) for image in images]
    images = [squeeze(image) for image in images]
    return images


def enhance_and_replace_images(path_to_images):
    # Enhance the images
    enhanced_images = enhance_images(path_to_images)

    for original_image_path, enhanced_image in zip(os.listdir(path_to_images), enhanced_images):
        original_image_path = os.path.join(path_to_images, original_image_path)
        os.remove(original_image_path)

        enhanced_image_path = os.path.join(
            path_to_images, os.path.basename(original_image_path))
        enhanced_image = final_process(enhanced_image)
        enhanced_image.save(enhanced_image_path)

        print(f"Enhanced: {original_image_path} -> {enhanced_image_path}")


LOCATION = ""  # add path where your images are stored
enhance_and_replace_images(LOCATION)

import random
import string
from bs4 import BeautifulSoup
import requests
import csv
import os
from urllib.parse import urlparse


def generate_random_string(length=16):
    # Define the characters that can be used in the random string
    characters = string.ascii_letters + string.digits
    # Generate the random string
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

import csv

def write_array_to_csv(items, csv_filename):
    try:
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Images"])  # Write a header row if needed

            for item in items:
                if item.startswith("http"):
                    writer.writerow([item])
        
    except Exception as e:
        pass



def scrape_images(query, num_pages):
    img_urls = []
    for page in range(1, num_pages + 1):
        search_url = f"https://www.google.com/search?q={query}&tbm=isch&start={(page - 1) * 20}"

        response = requests.get(search_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')

            for img_tag in img_tags:
                img_url = img_tag.get('src')
                if img_url:
                    img_urls.append(img_url)
    return img_urls


def save_images(save_path, image_links):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for index, image_url in enumerate(image_links):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                # Get the file extension from the URL (e.g., .jpg, .png)
                image_url = urlparse(image_url)
                file_extension = os.path.splitext(image_url.path)[1]
                # Create a unique filename based on the index and file extension
                filename = f"image_{generate_random_string()}{file_extension}"+".png"
                # Specify the complete path to save the image
                image_path = os.path.join(save_path, filename)
                # Save the image to the local folder
                with open(image_path, 'wb') as img_file:
                    img_file.write(response.content)
        except Exception as e:
            pass


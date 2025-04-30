import requests
from bs4 import BeautifulSoup
import os
import time
import json

# Configuration
BASE_URL = "https://pocket.limitlesstcg.com/cards"
DECK_ID = "A3"
START_ID = 1
END_ID = 155

cards = []

# Folder to store images
images_dir = "card_images"
os.makedirs(images_dir, exist_ok=True)

for card_id in range(START_ID, END_ID + 1):
    url = f"{BASE_URL}/{DECK_ID}/{card_id}"
    print(f"Scraping {url}...")

    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Failed to retrieve card {card_id}. Status code: {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    # Get image
    img_tag = soup.find("img", class_="card shadow resp-w")
    img_url = img_tag["src"] if img_tag else None

    # Get name
    name_tag = soup.find(class_="card-text-name")
    name = name_tag.text.strip() if name_tag else f"Card_{card_id}"

    # Get type block and clean it
    type_tag = soup.find(class_="card-text-type")
    raw_type = type_tag.text.strip() if type_tag else ""
    lines = [line.strip() for line in raw_type.split("\n") if line.strip()]

    type_value = lines[0] if lines else None
    stage_value = None

    # Normalize type (e.g., "Pok\u00e9mon" → "Pokemon")
    if type_value:
        type_value = type_value.replace("Pok\u00e9mon", "Pokémon")

    # Clean and extract stage (e.g., "- Stage 1" → "Stage 1")
    for line in lines[1:]:
        if any(stage in line for stage in ["Basic", "Stage 1", "Stage 2", "Supporter"]):
            stage_value = line.lstrip("- ").strip()
            break


    # Get exclusivity info for the card
    details_div = soup.find(class_="prints-current-details")
    exclusive_text = "None"

    if details_div:
        span_tags = details_div.find_all("span") 
        if len(span_tags) > 1: 
            details_text = span_tags[1].text.strip() # I only want to get the pack exclusivity info in the 2nd span
            parts = [part.strip() for part in details_text.split("·")]
            if len(parts) >= 3:
                exclusive_text = parts[-1]

                # Remove 'pack' suffix if it exists
                if exclusive_text.lower().endswith("pack"):
                    exclusive_text = exclusive_text.rsplit("pack", 1)[0].strip()

    # Download image
    image_path = None
    if img_url:
        image_response = requests.get(img_url)
        if image_response.status_code == 200:
            image_ext = os.path.splitext(img_url)[1] or ".jpg"
            image_filename = f"{DECK_ID}_{card_id}{image_ext}"
            image_path = os.path.join(images_dir, image_filename)
            with open(image_path, "wb") as img_file:
                img_file.write(image_response.content)
        else:
            print(f"❌ Failed to download image for card {card_id}")

    # Store the result
    cards.append({
        "deck_id": DECK_ID,
        "card_id": card_id,
        "name": name,
        "type": type_value,
        "stage": stage_value,
        "image_url": img_url,
        "local_image_path": image_path,
        "exclusive": exclusive_text

    })

    time.sleep(0.5)  # Be kind to the server

# Save results to JSON
with open(f"{DECK_ID}.json", "w") as f:
    json.dump(cards, f, indent=2)

print(f"✅ Scraping complete! Data saved to {DECK_ID}.json and images saved to 'card_images/'")

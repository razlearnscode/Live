document.addEventListener("DOMContentLoaded", () => {
  const cardContainer = document.getElementById("card-container");
  setupImagePopup();
  show_wishlist();
});

function show_wishlist() {
  fetch("/wishlist")
    .then((response) => response.json())
    .then((decks) => {
      const container = document.getElementById("card-container");
      container.innerHTML = ""; // Clear previous content

      decks.forEach((deck) => {
        const section = document.createElement("section");
        section.classList.add("deck-section");

        const header = document.createElement("h2");
        header.textContent = `Deck: ${deck.deck}`;
        section.appendChild(header);

        const grid = document.createElement("div");
        grid.classList.add("card-grid");

        deck.cards.forEach((card) => {
          // Only show cards in the wishlist
          if (!card.wishlist) return;

          const cardEl = document.createElement("div");
          cardEl.classList.add("card");
          cardEl.dataset.cardId = card.id;

          cardEl.innerHTML = `
            <div class="card-content">
                <img src="/media/${card.local_image_path}" alt="${card.name}">
                <h4>${card.name}</h4>
                <p>Type: ${formatChoice(card.type)}</p>
                <p>Stage: ${formatChoice(card.stage)}</p>
            </div>
            <div class="card-overlay"></div>
            <button class="remove-btn" onclick="remove_from_wishlist(${
              card.id
            })">Remove</button>
                    `;

          grid.appendChild(cardEl);
        });

        // Only show deck if it has wishlist cards
        if (grid.children.length > 0) {
          section.appendChild(grid);
          container.appendChild(section);

        attachImagePopupHandlers(); // rebind fresh
        }
      });
    });
}

function remove_from_wishlist(card_id) {
  fetch(`/remove_from_wishlist/${card_id}`, {
    method: "DELETE",
    headers: {
      "X-CSRFToken": getCSRFToken(),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.message);

      // Remove the card from DOM on the same session
      const card_entry = document.querySelector(
        `.card[data-card-id="${card_id}"]`
      );
      if (card_entry) card_entry.remove();
    })
    .catch((error) => {
      console.error("Error removing card from wishlist:", error);
    });
}

function formatChoice(choice) {
  // Converts "POKÉMON" → "Pokémon"
  const mapping = {
    POKÉMON: "Pokémon",
    TRAINER: "Trainer",
    BASIC: "Basic",
    STAGE1: "Stage 1",
    STAGE2: "Stage 2",
    OTHERS: "Others",
  };
  return mapping[choice] || choice;
}

// CSRF Helper
function getCSRFToken() {
  const name = "csrftoken";
  const cookieValue = document.cookie
    .split("; ")
    .find((row) => row.startsWith(name + "="))
    ?.split("=")[1];
  return cookieValue || "";
}

// Click-to-enlarge image popup
function setupImagePopup() {
  const popup = document.getElementById("image-popup");
  const popupImage = document.getElementById("popup-image");

  // Close popup when clicking the background
  popup.addEventListener("click", () => {
    popup.classList.add("hidden");
    popupImage.src = "";
  });
}

// Attach to each image
function attachImagePopupHandlers() {
  document.querySelectorAll(".card-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (e) => {
      e.stopPropagation();

      const cardEl = overlay.closest(".card");
      const img = cardEl.querySelector("img");

      if (!img || !img.src) {
        console.warn("No image found in card:", cardEl);
        return;
      }

      const popup = document.getElementById("image-popup");
      const popupImage = document.getElementById("popup-image");

      popupImage.src = img.src;
      popup.classList.remove("hidden");
    });
  });
}

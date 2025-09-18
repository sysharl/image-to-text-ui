const searchInput = document.getElementById("search");
const cards = document.querySelectorAll(".card");
const visibleCount = document.getElementById("visibleCount");
const totalCount = document.getElementById("totalCount");

function filterCards() {
  const query = searchInput.value.toLowerCase().trim();
  let visible = 0;

  cards.forEach((card) => {
    const haystack = card.dataset.search; 
    if (!query || haystack.includes(query)) {
      card.style.display = "inline-block";
      visible++;
    } else {
      card.style.display = "none";
    }
  });

  visibleCount.textContent = visible;
}

searchInput.addEventListener("input", filterCards);

visibleCount.textContent = cards.length;

function copyQuote(id) {
  const quoteEl = document.getElementById(`quote-text-${id}`);
  const text = quoteEl.innerText;

  navigator.clipboard
    .writeText(text)
    .then(() => {
      alert("Quote copied! ✅");
    })
    .catch((err) => {
      console.error("Copy failed:", err);
    });
}

window.copyQuote = copyQuote;

const API_URL = "http://127.0.0.1:8000/analyze";

const analyzeBtn = document.getElementById("analyzeBtn");
const inputText = document.getElementById("inputText");
const outputDiv = document.getElementById("outputText");
const translatedDiv = document.getElementById("translatedText");

const modal = document.getElementById("wordModal");
const closeModal = document.getElementById("closeModal");

analyzeBtn.addEventListener("click", async () => {
  const text = inputText.value.trim();
  if (!text) return;

  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  const data = await response.json();
  renderResult(data);
});

function renderResult(data) {
  outputDiv.innerHTML = "";
  translatedDiv.textContent = data.full_translation || "";

  let lastRendered = null;

  data.tokens.forEach(token => {
    if (!token.is_alpha) {
      lastRendered = null;
      return;
    }

    const word = data.words[token.lemma];
    if (!word) return;

    const lower = token.text.toLowerCase();

    if (
      word.role === "functional" &&
      lastRendered === lower
    ) {
      return;
    }

    const span = document.createElement("span");
    span.textContent = token.text + " ";
    span.className = "word";
    span.style.cursor = "pointer";
    span.style.backgroundColor = getColor(token.pos);
    span.onclick = () => openModal(word);

    outputDiv.appendChild(span);
    lastRendered = lower;
  });
}

function openModal(word) {
  document.getElementById("modalWord").textContent = word.lemma;
  document.getElementById("modalPos").textContent = word.pos.pt;
  document.getElementById("modalTranslation").textContent = word.translation;

  document.getElementById("modalExampleEn").textContent =
    word.example?.text || "";

  document.getElementById("modalExamplePt").textContent =
    word.example?.translation || "";

  document.getElementById("modalExplanation").textContent =
    word.explanation || "";

  modal.classList.remove("hidden");
}

closeModal.onclick = () => {
  modal.classList.add("hidden");
};

modal.onclick = (e) => {
  if (e.target === modal) {
    modal.classList.add("hidden");
  }
};
function getColor(pos) {
  const colors = {
    NOUN: "#A5D6A7",
    VERB: "#90CAF9",
    PRON: "#FFCC80",
    ADJ: "#CE93D8",
    ADV: "#FFF59D",
    ADP: "#B0BEC5"
  };
  return colors[pos] || "#E0E0E0";
}
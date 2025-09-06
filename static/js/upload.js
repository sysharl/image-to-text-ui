const fileInput = document.getElementById("fileInput");
const dropZone = document.getElementById("dropZone");
const fileList = document.getElementById("fileList");
const uploadForm = document.getElementById("uploadForm");
const loadingScreen = document.getElementById("loadingScreen");

let selectedFiles = [];

function updateFileList(newFiles) {
  for (const file of newFiles) {
    if (
      !selectedFiles.some((f) => f.name === file.name && f.size === file.size)
    ) {
      selectedFiles.push(file);
    }
  }

  fileList.innerHTML = "";
  selectedFiles.forEach((file) => {
    const li = document.createElement("li");
    li.textContent = `${file.name} (${Math.round(file.size / 1024)} KB)`;
    fileList.appendChild(li);
  });
}

// Click on box opens hidden input
dropZone.addEventListener("click", () => fileInput.click());

// Handle file input
fileInput.addEventListener("change", () => updateFileList(fileInput.files));

// Drag & Drop Events
dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  updateFileList(e.dataTransfer.files);
});

uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault(); // prevent normal form submit
  loadingScreen.style.display = "flex"; 
  const formData = new FormData();
  selectedFiles.forEach((file) => {
    formData.append("files", file); // "files" matches Flask
  });

  fetch(uploadForm.action, {
    method: "POST",
    body: formData,
  }).then((data) => {
    console.log(data);
    if (data.redirected) {
      window.location.href = data.url; // force browser to navigate
    } else {
      console.log(data);
    }
  }).catch(e =>
    console.log(e)
  );
});


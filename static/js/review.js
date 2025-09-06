function createSegment(textarea_id) {
  const textArea = document.getElementById("texts_"+textarea_id);
  const selectedText = textArea.value.substring(
    textArea.selectionStart,
    textArea.selectionEnd
  );

  if (!selectedText.trim()) {
    alert("Please select some text to segment.");
    return;
  }
textarea_id="segments_"+textarea_id
console.log(textarea_id)
  const segmentsContainer = document.getElementById(textarea_id);
  const card = document.createElement("div");
  card.className = "form-group position-relative";
  uniqueId= textarea_id+'_'+segmentsContainer.childNodes.length
  card.id= uniqueId
  card.innerHTML = `
    <input type="text" name="${textarea_id}_title[]" id="${uniqueId}_title" placeholder="Title">
    <input type="text" name="${textarea_id}_author[]" id="${uniqueId}_author" placeholder="Author">
    <input type="text" name="${textarea_id}_actor[]" id="${uniqueId}_actor" placeholder="Actor">
    <input type="text" name="${textarea_id}_category[]" id="${uniqueId}_category" placeholder="Category">
    <textarea id="${uniqueId}_segment" name="${textarea_id}_quote[]">${selectedText}</textarea>
    <button type="button" class="btn btn-sm btn-danger position-absolute top-0 end-0 m-2" onclick="deleteSegment('${uniqueId}')">X</button>

  `;
  segmentsContainer.appendChild(card);
}

function deleteSegment(id) {
  const segment = document.getElementById(id);
  if (segment) {
    segment.remove();
  }
}
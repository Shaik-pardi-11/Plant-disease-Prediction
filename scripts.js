document.getElementById("imageUpload").addEventListener("change", function () {
  const file = this.files[0];
  const preview = document.getElementById("previewImage");

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      preview.src = e.target.result;
      preview.style.display = "block";
    };
    reader.readAsDataURL(file);
  }
});

document.getElementById("predictBtn").addEventListener("click", function () {
  const result = document.getElementById("predictionResult");
  const preview = document.getElementById("previewImage");

  if (!preview.src || preview.style.display === "none") {
    result.textContent = "Please upload an image first.";
    return;
  }

  // Simulate prediction result (can replace with ML model API later)
  const fakeResults = [
    "Prediction: Leaf Blight",
    "Prediction: Rust Disease",
    "Prediction: Powdery Mildew",
    "Prediction: Healthy Leaf"
  ];
  const randomIndex = Math.floor(Math.random() * fakeResults.length);
  result.textContent = fakeResults[randomIndex];
});


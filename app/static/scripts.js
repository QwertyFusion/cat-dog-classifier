function uploadImage() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  if (!file) {
    alert("Please select an image.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  fetch("/predict", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        document.getElementById("result").innerText = "Error: " + data.error;
      } else {
        let resultText = "<h3>Predictions:</h3>";
        resultText += `<p><strong>CNN:</strong> ${data.cnn}</p>`;
        resultText += `<p><strong>SVM:</strong> ${data.svm}</p>`;
        resultText += `<p><strong>Random Forest:</strong> ${data.random_forest}</p>`;
        resultText += `<p><strong>Logistic Regression:</strong> ${data.logistic_regression}</p>`;
        resultText += `<p><strong>K-Means:</strong> ${data.kmeans}</p>`;
        resultText += `<h2>Final Prediction: ${data.final_prediction}</h2>`;

        document.getElementById("result").innerHTML = resultText;

        const uploadedImage = document.getElementById("uploadedImage");
        uploadedImage.src = `/uploads/${file.name}`; // Use the original file name
        uploadedImage.style.display = "block";
      }
    })
    .catch((error) => console.error("Error:", error));
}

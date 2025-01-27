// Tab Switching Logic
function showTab(tabId) {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(tabId).classList.add('active');
}

// Insert Button Logic
function insertImage() {
    const inputFile = document.querySelector('input[type="file"]');
    if (inputFile.files.length > 0) {
        alert('Image inserted successfully!');
    } else {
        alert('Please select an image first.');
    }
}

// Display the Result After Classification
const form = document.getElementById('upload-form');
form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Simulate result display (replace this with your backend integration)
    const resultContent = document.getElementById('result-content');
    resultContent.innerHTML = "<p>Processing...</p>";
    setTimeout(() => {
        resultContent.innerHTML = "<p>The uploaded image is classified as a <strong>Cat</strong>!</p>";
        showTab('result-tab');
    }, 2000);
});

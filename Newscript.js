// script.js

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const imageUpload = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');
    const resultsDiv = document.getElementById('results');

    // Preview the selected image
    imageUpload.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.innerHTML = `<img src="${e.target.result}" alt="Image Preview" style="max-width: 100%; height: auto;">`;
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle form submission
    uploadForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData(uploadForm);

        try {
            const response = await fetch('/classify', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            console.log('Classification result:', result);

            // Display the classification result and matching items
            let itemsHtml = '';
            if (result.matching_items && result.matching_items.length > 0) {
                itemsHtml = '<h2>Matching Accessories</h2><ul>';
                result.matching_items.forEach(item => {
                    itemsHtml += `<li>${item.description} (${item.category})</li>`;
                });
                itemsHtml += '</ul>';
            } else {
                itemsHtml = '<h2>No matching accessories found.</h2>';
            }

            resultsDiv.innerHTML = `
                <h2>Classification Result</h2>
                <p><strong>Class:</strong> ${result.class_name}</p>
                ${itemsHtml}
            `;
        } catch (error) {
            console.error('Error:', error);
            resultsDiv.innerHTML = '<h2>An error occurred. Please try again.</h2>';
        }
    });
});

// script.js
document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);

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
        // Handle displaying result to the user if needed
    } catch (error) {
        console.error('Error:', error);
        // Handle error display or logging
    }
});



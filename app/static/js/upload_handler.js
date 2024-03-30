async function handleSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch(form.action, {
            method: form.method,
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Upload failed');
        }
        
        const data = await response.json();
        
        if ('error' in data) {
            document.getElementById('error-message').innerText = data.error;
            document.getElementById('predictions').innerText = '';
        } else {
            document.getElementById('error-message').innerText = '';
            const predictions = data.predictions;
            if (predictions.length === 0) {
                document.getElementById('predictions').innerText = 'No object detected.';
            } else {
                let result = '';
                predictions.forEach(prediction => {
                    result += `Label: ${prediction.label}\n`;
                    result += `Confidence: ${prediction.confidence.toFixed(2)}\n`;
                    result += `Bounding Box: ${prediction.bbox}\n\n`;
                });
                document.getElementById('predictions').innerText = result;
            }
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('error-message').innerText = 'An error occurred';
        document.getElementById('predictions').innerText = '';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', handleSubmit);

    const backButton = document.getElementById('back-home-btn');
    backButton.addEventListener('click', function() {
        window.location.href = '/';
    });
});

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
                    
                    // Simpan hasil prediksi
                    savePrediction(prediction);
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

async function savePrediction(prediction) {
    const user_id = getUserID();
    const data = { user_id: user_id, prediction: prediction };
    
    try {
        const response = await fetch('/save_prediction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error('Failed to save prediction');
        }
    } catch (error) {
        console.error('Error:', error);
        // Handle error jika gagal menyimpan prediksi
    }
}

function getUserID() {
    // jika ID pengguna disimpan dalam sessionStorage dengan kunci 'userID'
    return sessionStorage.getItem('id');
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', handleSubmit);

    const backButton = document.getElementById('back-home-btn');
    backButton.addEventListener('click', function() {
        window.location.href = '/';
    });
});

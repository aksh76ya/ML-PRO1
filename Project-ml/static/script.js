document.getElementById('emojiForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const text = document.getElementById('textInput').value;

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `text=${encodeURIComponent(text)}`,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('emojiResult').textContent = data.emoji;
    })
    .catch(error => console.error('Error:', error));
});
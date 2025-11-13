document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('image');
    const preview = document.getElementById('preview');
    const filenameSpan = document.getElementById('filename');
    const resetBtn = document.getElementById('reset-btn');
    const form = document.getElementById('upload-form');
    const spinner = document.getElementById('loading-spinner');

    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            filenameSpan.textContent = file.name;
            const reader = new FileReader();
            reader.onload = function(event) {
                preview.src = event.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            filenameSpan.textContent = '';
            preview.src = '';
        }
    });

    resetBtn.addEventListener('click', function() {
        form.reset();
        preview.src = '';
        filenameSpan.textContent = '';
        spinner.style.display = 'none';
    });

    form.addEventListener('submit', function() {
        spinner.style.display = 'flex';
    });
});

const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

sendBtn.onclick = async function() {
  const message = userInput.value.trim();
  if (!message) return;

  // Display user message
  chatBox.innerHTML += `<div class="user">👨‍🌾 You: ${message}</div>`;
  userInput.value = "";

  // Send to Django backend
  const response = await fetch("/chatbot/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message})
  });

  const data = await response.json();
  const reply = data.reply;

  chatBox.innerHTML += `<div class="bot">🤖 AgriChat: ${reply}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
};

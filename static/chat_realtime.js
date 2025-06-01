document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    const messageList = document.getElementById('message-list');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const loadingSpinner = document.getElementById('loading-spinner');

    // Append message to message list
    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender === 'You' ? 'user' : 'bot');

        const senderDiv = document.createElement('div');
        senderDiv.classList.add('sender');
        senderDiv.textContent = sender;

        const textDiv = document.createElement('div');
        textDiv.classList.add('text');
        textDiv.textContent = text;

        messageDiv.appendChild(senderDiv);
        messageDiv.appendChild(textDiv);

        messageList.appendChild(messageDiv);
        messageList.scrollTop = messageList.scrollHeight;
    }

    // Show spinner
    function showSpinner() {
        loadingSpinner.style.display = 'flex';
    }

    // Hide spinner
    function hideSpinner() {
        loadingSpinner.style.display = 'none';
    }

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const message = messageInput.value.trim();
        if (!message) return;

        addMessage('You', message);
        messageInput.value = '';

        showSpinner();

        // Emit message to server
        socket.emit('send_message', { message: message });
    });

    // Receive messages from server
    socket.on('receive_message', (data) => {
        hideSpinner();
        // Assuming data contains the reply from AI assistant
        addMessage('AI Assistant', data.message);
    });
});

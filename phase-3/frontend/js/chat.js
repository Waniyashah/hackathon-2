/**
 * Todo AI Chatbot - Frontend JavaScript
 * Handles chat UI interactions and API communication
 */

// Configuration
const API_BASE_URL = 'http://localhost:8080/api';
const USER_ID = 'user_' + Math.random().toString(36).substr(2, 9); // Generate random user ID

// State
let conversationId = null;
let isLoading = false;

// DOM Elements
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const sendButtonText = document.getElementById('sendButtonText');
const sendButtonLoader = document.getElementById('sendButtonLoader');
const messagesContainer = document.getElementById('messagesContainer');
const statusBar = document.getElementById('statusBar');
const statusText = document.getElementById('statusText');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    chatForm.addEventListener('submit', handleSubmit);
    messageInput.focus();
    updateStatus('Ready to chat!');
});

/**
 * Handle form submission
 */
async function handleSubmit(e) {
    e.preventDefault();

    const message = messageInput.value.trim();
    if (!message || isLoading) return;

    // Clear input
    messageInput.value = '';

    // Add user message to UI
    addMessage(message, 'user');

    // Set loading state
    setLoading(true);
    updateStatus('Thinking...');

    try {
        // Send message to API
        const response = await sendMessage(message);

        // Add assistant response to UI
        addMessage(response.response, 'assistant');

        // Update conversation ID
        if (response.conversation_id) {
            conversationId = response.conversation_id;
        }

        // Update status
        if (response.tool_executed) {
            updateStatus(`Executed: ${response.tool_name || 'action'}`);
        } else {
            updateStatus('Ready');
        }

    } catch (error) {
        console.error('Error sending message:', error);
        addErrorMessage('Failed to send message. Please try again.');
        updateStatus('Error - Ready to retry');
    } finally {
        setLoading(false);
        messageInput.focus();
    }
}

/**
 * Send message to API
 */
async function sendMessage(message) {
    const url = `${API_BASE_URL}/${USER_ID}/chat`;

    const requestBody = {
        message: message
    };

    if (conversationId) {
        requestBody.conversation_id = conversationId;
    }

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to send message');
    }

    return await response.json();
}

/**
 * Add message to UI
 */
function addMessage(content, role) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;

    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    scrollToBottom();
}

/**
 * Add error message to UI
 */
function addErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;

    messagesContainer.appendChild(errorDiv);
    scrollToBottom();
}

/**
 * Set loading state
 */
function setLoading(loading) {
    isLoading = loading;

    if (loading) {
        sendButton.disabled = true;
        messageInput.disabled = true;
        sendButtonText.classList.add('hidden');
        sendButtonLoader.classList.remove('hidden');
    } else {
        sendButton.disabled = false;
        messageInput.disabled = false;
        sendButtonText.classList.remove('hidden');
        sendButtonLoader.classList.add('hidden');
    }
}

/**
 * Update status bar
 */
function updateStatus(message) {
    statusText.textContent = message;
}

/**
 * Scroll messages container to bottom
 */
function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/**
 * Handle keyboard shortcuts
 */
document.addEventListener('keydown', (e) => {
    // Focus input on any key press (except special keys)
    if (!e.ctrlKey && !e.metaKey && !e.altKey && e.key.length === 1) {
        if (document.activeElement !== messageInput) {
            messageInput.focus();
        }
    }
});

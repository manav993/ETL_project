function connectWebSocket() {
    const socket = new WebSocket('ws://localhost:5678');

    socket.addEventListener('open', function (event) {
        console.log('WebSocket connection opened');
        startKeepAlive(socket);  // Start sending keep-alive messages
    });

    socket.addEventListener('message', function (event) {
        console.log('Message from server:', event.data);
        // Handle incoming messages
    });

    socket.addEventListener('close', function (event) {
        console.log('WebSocket connection closed:', event.code, event.reason);
        if (event.code !== 1000) {  // Reconnect only on abnormal closure
            console.log('Attempting to reconnect in 5 seconds...');
            setTimeout(connectWebSocket, 5000);
        } else {
            console.log('Connection closed normally.');
        }
    });

    socket.addEventListener('error', function (error) {
        console.error('WebSocket error observed:', error);
    });
}

function startKeepAlive(socket) {
    // Send a ping message every 15 seconds to keep the connection alive
    setInterval(() => {
        if (socket.readyState === WebSocket.OPEN) {
            console.log('Sending keep-alive ping to server');
            socket.send('ping');
        }
    }, 15000);  // 15 seconds interval
}

// Initialize WebSocket connection
connectWebSocket();

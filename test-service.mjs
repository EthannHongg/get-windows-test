import WebSocket from 'ws';

const ws = new WebSocket('ws://localhost:3002');

ws.on('open', () => {
    console.log('WebSocket connection opened');
});

ws.on('message', (data) => {
    const windows = JSON.parse(data);
    console.log('Received windows data: ', windows);
});

ws.on('close', () => {
    console.log('WebSocket connection closed');
});

ws.on('error', (error) => {
    console.error('WebSocket error: ', error);
});
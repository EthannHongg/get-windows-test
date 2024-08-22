const ffi = require('ffi-napi');
const ref = require('ref-napi');
const win32 = require('win32-api');
const { kernel32, user32 } = win32;

const user32Api = user32.api;

// Define data types
const intPtr = ref.refType('int');
const longPtr = ref.refType('long');

// Define structures
const rectStruct = new ffi.Struct({
    left: 'long',
    top: 'long',
    right: 'long',
    bottom: 'long',
});

// Helper function to get window title
function getWindowTitle(hwnd) {
    const titleBuffer = Buffer.alloc(255);
    user32Api.GetWindowTextW(hwnd, titleBuffer, 255);
    return titleBuffer.toString('ucs2').replace(/\0/g, '');
}

// Helper function to get window bounds
function getWindowBounds(hwnd) {
    const rect = new rectStruct();
    user32Api.GetWindowRect(hwnd, rect.ref());
    return {
        left: rect.left,
        top: rect.top,
        right: rect.right,
        bottom: rect.bottom,
    };
}

// Helper function to get window class name
function getClassName(hwnd) {
    const classNameBuffer = Buffer.alloc(255);
    user32Api.GetClassNameW(hwnd, classNameBuffer, 255);
    return classNameBuffer.toString('ucs2').replace(/\0/g, '');
}

// Function to capture windows metadata
function captureWindowsData() {
    user32Api.EnumWindows(ffi.Callback('bool', ['long', 'int32'], (hwnd, lParam) => {
        const title = getWindowTitle(hwnd);
        const className = getClassName(hwnd);
        const bounds = getWindowBounds(hwnd);

        if (title) {
            console.log('Window Handle:', hwnd);
            console.log('Window Title:', title);
            console.log('Class Name:', className);
            console.log('Bounds:', bounds);
            console.log('============================');
        }

        return true; // Continue enumeration
    }), 0);
}

// Start capturing
captureWindowsData();

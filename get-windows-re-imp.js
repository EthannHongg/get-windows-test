const ffi = require('ffi-napi');
const ref = require('ref-napi');
const Struct = require('ref-struct-napi');

// Define the necessary types
const HWND = ref.refType(ref.types.void);
const int = ref.types.int;
const long = ref.types.long;
const wchar_t = ref.types.uint16;
const TCHAR = wchar_t;
const LPTSTR = ref.refType(TCHAR);

const RECT = Struct({
  left: long,
  top: long,
  right: long,
  bottom: long,
});

const POINT = Struct({
  x: long,
  y: long,
});

const WINDOWINFO = Struct({
  cbSize: int,
  rcWindow: RECT,
  rcClient: RECT,
  dwStyle: long,
  dwExStyle: long,
  dwWindowStatus: long,
  cxWindowBorders: int,
  cyWindowBorders: int,
  atomWindowType: long,
  wCreatorVersion: int,
});

// Load the necessary Windows API functions
const user32 = ffi.Library('user32', {
  'EnumWindows': ['bool', [ffi.Function('bool', [HWND, ref.types.int32]), ref.types.int32]],
  'GetWindowTextW': ['int', [HWND, LPTSTR, int]],
  'GetWindowRect': ['bool', [HWND, ref.refType(RECT)]],
  'IsWindowVisible': ['bool', [HWND]],
});

// Helper function to convert wchar_t buffer to string
function wcharBufferToString(buffer) {
  return buffer.toString('ucs2').replace(/\0/g, '');
}

// Function to enumerate windows and retrieve their titles and positions
function getOpenWindows() {
  const windowList = [];

  // Define the callback function to be passed to EnumWindows
  const enumWindowsProc = ffi.Callback('bool', [HWND, ref.types.int32], (hwnd, lParam) => {
    const titleBuffer = Buffer.alloc(512 * 2); // Allocate buffer for the window title (512 wchar_t)
    const length = user32.GetWindowTextW(hwnd, titleBuffer, 512);

    if (length > 0 && user32.IsWindowVisible(hwnd)) {
      const title = wcharBufferToString(titleBuffer);
      const rect = new RECT();
      user32.GetWindowRect(hwnd, rect.ref());

      windowList.push({
        title,
        rect: {
          left: rect.left,
          top: rect.top,
          right: rect.right,
          bottom: rect.bottom,
        },
      });
    }

    return true; // Continue enumeration
  });

  // Call EnumWindows to start enumerating windows
  user32.EnumWindows(enumWindowsProc, 0);

  return windowList;
}

// Run the function and print the open windows
const windows = getOpenWindows();
console.log(windows);

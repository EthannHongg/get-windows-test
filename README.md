3P App Windows Metadata
===========

Experimentations, prototypes, and benchmarkings with different packages, OS APIs, OCR models, and techniques for retrieving windows metadata from third-party desktop apps.

Install
-------
**For python scripts**

`pip install -U pywinauto` (dependencies for pywinauto will be installed automatically)

`pip install pygetwindow screeninfo shapely mss pillow paddlepaddle paddleocr`

**For npm packages**

`npm install`

Files
-------
The following scripts all compile and have been manually tested unless it is exclusively mentioned that they haven't (provided as a implementation guideline).

**`ocr.py`**

Simple `PaddleOCR` implementation of taking screenshots, performs recognition, and visualizes the results for easy review of the model.

**`pygetwindow-test.py`**

Uses `pygetwindow` package for easy retrieval of Windows OS windows metadata. Also includes a sample implementation of `get_displayed_bounds` that calculates a list of regions which are actually visible to the user for the corresponding window. Includes performance benchmarking.

**`pywinauto-getwindowtest.py`**

Simple `pywinauto` implementation of retrieving window content level metadata. Does not include performance benchmarking because it's too slow.

**`pywinauto-test.py`**

`pywinauto` implementation of retrieving Windows OS windows metadata. Includes performance benchmarking.

**`start-service.py`**

Use `get-windows` package to get windows metadata across platforms. Includes benchmarking. However, on Windows OS, there is an error that the results will always be undefined without producing an error. Suspected to be caused by package versions. Recommended to start a Github issue for the package.

**`get-windows-re-imp.js`**

Sample implementation of `ffi-napi` and Windows OS APIs of getting windows metadata. DOES NOT guarantee to run and compile (had problems setting up ffi-napi and did not too much spend time fixing this)

Start the service: `terminal1 $ node start-service.js`

Start the test service script which establishes a WS connection with the service for constant monitoring in a separate terminal: `terminal2 $ node test-service.mjs`

Or you may send a GET request via `localhost:3001/windows`

**`windows-api.js`**

Sample implementation of `ffi-napi` and `win32-api` (FFI Definitions of Windows win32 api for node-ffi). DOES NOT guarantee to run and compile.

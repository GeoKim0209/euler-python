# Pyodide Timeout Implementation

This implementation adds timeout support to prevent infinite loops and browser hangs when running Python code in the browser using Pyodide.

## Features

- **5-second default timeout**: Code execution is automatically terminated after 5 seconds
- **Interrupt-based termination**: Uses Pyodide's interrupt system with SharedArrayBuffer
- **Web Worker isolation**: Python code runs in a separate worker thread
- **User-friendly error messages**: Clear timeout notifications with helpful context
- **Graceful fallback**: Handles browsers without SharedArrayBuffer support

## Implementation Details

### Files Modified/Created

1. **`pyodide-worker.js`** (new): Web worker that handles Pyodide execution with interrupt support
2. **`base.html`**: Updated to use web worker and timeout functionality
3. **`style.css`**: Added timeout-specific error styling
4. **`timeout-test.html`** (new): Test page for verifying timeout functionality

### Architecture

```
Main Thread                    Web Worker
     |                              |
     |-- SharedArrayBuffer ---------|
     |                              |
     |-- Start timeout timer        |
     |-- Send code to worker ------>|-- Execute Python code
     |                              |-- Check interrupt buffer
     |-- Timeout expires             |
     |-- Set interrupt signal ------>|-- Receive interrupt
     |-- Display timeout error       |-- Raise KeyboardInterrupt
```

### Key Components

#### 1. Interrupt Buffer
- Uses `SharedArrayBuffer` to communicate between main thread and worker
- Value `0`: Normal execution
- Value `2`: SIGINT (interrupt signal)

#### 2. Timeout Management
- Default 5-second timeout per execution
- Configurable via `DEFAULT_TIMEOUT` constant
- Automatic cleanup of pending requests

#### 3. Error Handling
- Distinguishes between timeout errors and regular Python errors
- Special styling for timeout messages
- Graceful degradation when SharedArrayBuffer is unavailable

## Browser Requirements

### Required for Full Functionality
- **SharedArrayBuffer support**: Required for timeout functionality
- **HTTPS or localhost**: SharedArrayBuffer requires secure context
- **Proper headers**: Server must set appropriate COOP/COEP headers

### Headers Required for SharedArrayBuffer
```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

### Fallback Behavior
If SharedArrayBuffer is not available:
- Buttons show "Python unavailable"
- Error message explains the requirement
- No code execution is attempted

## Usage

### Basic Usage
The timeout functionality is automatically enabled. No changes needed to existing code:

```html
<button class="run-code-btn" 
        data-code="your_python_code" 
        data-output="output-id" 
        onclick="runPythonCodeFromButton(this)">
    Run Code
</button>
<div id="output-id" class="code-output"></div>
```

### Customizing Timeout
To change the default timeout, modify the `DEFAULT_TIMEOUT` constant:

```javascript
// Set to 10 seconds instead of 5
const DEFAULT_TIMEOUT = 10000;
```

### Testing
Use `timeout-test.html` to verify functionality:
1. Open the test page in a browser
2. Run each test case
3. Verify timeout behavior for infinite loops
4. Confirm normal execution for quick code

## Error Messages

### Timeout Error
```
Timeout Error: Code execution timed out after 5 seconds
The code took too long to execute and was terminated to prevent browser hang.
```

### SharedArrayBuffer Not Supported
```
Python unavailable
SharedArrayBuffer not supported. Timeout functionality requires HTTPS and proper headers.
```

## Troubleshooting

### Common Issues

1. **"SharedArrayBuffer not supported"**
   - Ensure HTTPS is used (or localhost for development)
   - Check that proper COOP/COEP headers are set
   - Verify browser supports SharedArrayBuffer

2. **Timeouts not working**
   - Check browser console for worker errors
   - Verify `pyodide-worker.js` is accessible
   - Ensure interrupt buffer is properly initialized

3. **Worker fails to load**
   - Check file path to `pyodide-worker.js`
   - Verify CORS settings allow worker loading
   - Check browser console for detailed errors

### Development Server Setup
For local development, ensure your server sets the required headers. Example for Python's http.server:

```python
# Add headers for SharedArrayBuffer support
self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
```

## Performance Considerations

- **Worker overhead**: Initial setup takes ~1-2 seconds
- **Memory usage**: Each worker maintains its own Pyodide instance
- **Timeout precision**: Actual timeout may vary by ~100ms due to JavaScript timing
- **Cleanup**: Automatic cleanup prevents memory leaks from abandoned requests

## Future Enhancements

Potential improvements:
- Configurable timeout per code block
- Progress indicators for long-running code
- Memory usage monitoring
- CPU usage limits
- Multiple worker pool for parallel execution 

# Pyodide Timeout Implementation

This implementation adds timeout support to prevent infinite loops and browser hangs when running Python code in the browser using Pyodide.

## Features

- **5-second default timeout**: Code execution is automatically terminated after 5 seconds
- **Worker termination**: Uses worker termination to stop runaway code execution
- **Web Worker isolation**: Python code runs in a separate worker thread
- **User-friendly error messages**: Clear timeout notifications with helpful context
- **Universal compatibility**: Works on all modern browsers and hosting platforms

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
     |-- Start timeout timer        |
     |-- Send code to worker ------>|-- Execute Python code
     |                              |
     |-- Timeout expires             |
     |-- Terminate worker ---------->|-- Worker terminated
     |-- Display timeout error       |
     |-- Recreate worker for         |
     |   future use                  |
```

### Key Components

#### 1. Worker Termination
- Uses `Worker.terminate()` to forcefully stop code execution
- Immediate termination of runaway processes
- Worker recreation for subsequent executions

#### 2. Timeout Management
- Default 5-second timeout per execution
- Configurable via `DEFAULT_TIMEOUT` constant
- Automatic cleanup of pending requests

#### 3. Error Handling
- Distinguishes between timeout errors and regular Python errors
- Special styling for timeout messages
- Universal compatibility across all browsers and hosting platforms

## Browser Requirements

### Required for Full Functionality
- **Modern browser with Web Worker support**: All major browsers since 2012
- **JavaScript enabled**: Required for all functionality
- **No special headers needed**: Works on any hosting platform including GitHub Pages

### Compatibility
- ✅ **GitHub Pages**: Full compatibility
- ✅ **Netlify/Vercel**: Full compatibility  
- ✅ **Any static hosting**: Full compatibility
- ✅ **Local development**: Full compatibility

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

### Worker Initialization Error
```
Python unavailable
Failed to initialize Python environment. Please refresh the page and try again.
```

## Troubleshooting

### Common Issues

1. **Timeouts not working**
   - Check browser console for worker errors
   - Verify `pyodide-worker.js` is accessible
   - Ensure worker is being created successfully

2. **Worker fails to load**
   - Check file path to `pyodide-worker.js`
   - Verify CORS settings allow worker loading
   - Check browser console for detailed errors

3. **Slow performance after timeouts**
   - This is expected as workers are recreated after termination
   - Worker initialization takes 1-2 seconds
   - Consider increasing timeout for complex calculations

### Development Server Setup
No special server configuration needed. Any static file server will work:

```bash
# Python built-in server
python -m http.server 8000

# Node.js serve
npx serve .

# Any static hosting platform
```

## Performance Considerations

- **Worker overhead**: Initial setup takes ~1-2 seconds
- **Memory usage**: Each worker maintains its own Pyodide instance
- **Timeout precision**: Actual timeout may vary by ~100ms due to JavaScript timing
- **Worker recreation**: After timeout, new worker creation adds ~1-2 second delay
- **Cleanup**: Automatic cleanup prevents memory leaks from abandoned requests

## Future Enhancements

Potential improvements:
- Configurable timeout per code block
- Progress indicators for long-running code
- Memory usage monitoring
- CPU usage limits
- Multiple worker pool for parallel execution 

// Pyodide Web Worker for handling Python code execution with timeout support
let pyodide = null;
let pyodideReady = false;

// Initialize Pyodide in the worker
async function initPyodide() {
  if (pyodideReady) return pyodide;

  try {
    pyodide = await loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/",
    });

    // Install required packages
    await pyodide.loadPackage(["micropip"]);

    // Set up euler library functions in Pyodide
    pyodide.runPython(`
import math
from collections import Counter

def is_prime(k):
    """Utility Function that helps the user check if the inputted number is prime or composite."""
    for i in range(2, int(math.sqrt(k)) + 1):
        if k % i == 0:
            return False
    return True

def get_prime_factorization(n):
    r = []
    while n > 1:
        factor = n
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                # n is divisible by i
                factor = i
                break
        r.append(factor)
        n = n // factor
    return Counter(r)

def get_sum_of_divisors(n):
    # Sum of divisors = (p^0 + p^1 + … + p^m) × (q^0 + q^1 + … + q^n)
    pf = get_prime_factorization(n)
    product = 1
    for prime, exponent in pf.items():
        sum = 0
        for i in range(exponent + 1):
            sum += prime**i
        product *= sum
    return product - n

# Capture print output
import sys
from io import StringIO

class OutputCapture:
    def __init__(self):
        self.output = StringIO()
        self.original_stdout = sys.stdout
    
    def start_capture(self):
        sys.stdout = self.output
    
    def stop_capture(self):
        sys.stdout = self.original_stdout
        result = self.output.getvalue()
        self.output = StringIO()
        return result

output_capture = OutputCapture()
    `);

    pyodideReady = true;
    console.log("Pyodide initialized successfully in worker");
    
    // Notify main thread that Pyodide is ready
    self.postMessage({ type: 'pyodide-ready' });
    
  } catch (error) {
    console.error("Failed to initialize Pyodide in worker:", error);
    self.postMessage({ 
      type: 'pyodide-error', 
      error: error.message 
    });
  }

  return pyodide;
}

// Handle messages from main thread
self.addEventListener("message", async (event) => {
  const { type, data } = event.data;

  switch (type) {
    case 'init':
      await initPyodide();
      break;

    case 'run-code':
      if (!pyodideReady) {
        self.postMessage({
          type: 'execution-error',
          requestId: data.requestId,
          error: 'Pyodide not ready'
        });
        return;
      }

      try {
        // Clear any previous output and start capturing
        pyodide.runPython(`
output_capture.start_capture()
        `);

        // Run the user code
        pyodide.runPython(data.code);

        // Stop capturing and get output
        const result = pyodide.runPython(`
output_capture.stop_capture()
        `);

        self.postMessage({
          type: 'execution-success',
          requestId: data.requestId,
          result: result
        });

      } catch (error) {
        self.postMessage({
          type: 'execution-error',
          requestId: data.requestId,
          error: error.message,
          isTimeout: false
        });
      }
      break;

    default:
      console.warn('Unknown message type:', type);
  }
});

// Load Pyodide script
importScripts('https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js');

// Start initialization
initPyodide(); 

let term = new Terminal({ cursorBlink: true });
term.open(document.getElementById('terminal'));

async function main() {
  term.write('Loading Pyodide...\r\n');
  let pyodide = await loadPyodide();

  const inputBuffer = [];
  let inputResolve = null;

  function waitInput() {
    return new Promise((resolve) => {
      inputResolve = resolve;
    });
  }

  term.onKey(e => {
    const char = e.key;
    if (char === '\r') {
      term.write('\r\n');
      const input = inputBuffer.join('');
      inputBuffer.length = 0;
      inputResolve(input);
    } else if (char === '\u007f') {
      if (inputBuffer.length > 0) {
        inputBuffer.pop();
        term.write('\b \b');
      }
    } else {
      inputBuffer.push(char);
      term.write(char);
    }
  });

  await pyodide.runPythonAsync(`
import sys
from js import console

input_buffer = []

def input(prompt=''):
    if prompt:
        print(prompt, end='')
    return await_input()

def print(*args, **kwargs):
    console.log(' '.join(map(str, args)))

import js
async def await_input():
    return await js.waitInput()

globals().update(locals())
`);

  // Inject input function
  pyodide.globals.set("waitInput", waitInput);

  const code = await (await fetch("wordle.py")).text();
  await pyodide.runPythonAsync(code);
}

main();

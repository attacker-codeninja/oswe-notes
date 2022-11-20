## Dangerous Functions

```
# RCE
eval()                  //evaluate string as a javascript code
safe-eval()             //same as eval, but more secure.
setTimeout(string, 2)
setInterval(string)
Function(string)

# Command Execution
child_process.exec()

# LFI
require()
```

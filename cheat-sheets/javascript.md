## Notes
- JavaScript strings can be natively hex-encoded e.g. `"\\\\x2fbin\\\\x2fbash"` - useful for string/regex bypass

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

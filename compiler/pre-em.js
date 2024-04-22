// Make Emscripten believe it's running in a browser because Cloudflare Workers
// is closer to a brower than to Node.js.
globalThis.window = {};
globalThis.importScripts = () => {}

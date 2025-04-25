
const jsonrpc = require("jsonrpc-lite");

let AUTH_MODE = ""; 
let JWT_TOKEN = "";  //fetchJwtToken function handles this
const API_KEY = "another-key-456";        // api-key needs to be replaced

function getAuthHeaders() {
  if (AUTH_MODE === "jwt") {
    console.log("Using JWT authentication");
    return { Authorization: `Bearer ${JWT_TOKEN}` };
  } else if (AUTH_MODE === "api-key") {
    console.log("i-am-here")
    return { "x-api-key": API_KEY };
  }
  return {};
}

async function fetchJwtToken() {
    const res = await fetch("http://localhost:3000/token");
    const data = await res.json();
    JWT_TOKEN = data.token;
  }
  

async function sendRpcRequest(body, skipResponse = false, addAuthentication=true ) {
  const headers = {
    "Content-Type": "application/json",
    ...(addAuthentication ? getAuthHeaders() : {}),
  };

  const res = await fetch("http://localhost:3000/rpc", {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });
  if (skipResponse) {
    return res.status;
  }

  return await res.json();
}

async function test() {
  // Test JWT authentication
  console.log("\n======= JWT AUTHENTICATION TESTS =======");
  let originalAuthMode = AUTH_MODE;
  AUTH_MODE = "jwt";
  await fetchJwtToken();
  console.log("✅ JWT Auth - add([5, 3]):", 
    await sendRpcRequest(jsonrpc.request(1, "add", [5, 3]), false, true));
  console.log("✅ JWT Auth - greet({ name: 'Alice' }):", 
    await sendRpcRequest(jsonrpc.request(2, "greet", { name: "Alice" }), false, true));
  console.log("✅ JWT Auth - notification:", 
    await sendRpcRequest(jsonrpc.notification("log", { message: "Hello from JWT" }), true, true));

  // Test API Key authentication
  console.log("\n======= API KEY AUTHENTICATION TESTS =======");
  AUTH_MODE = "api-key";
  console.log("✅ API Key Auth - add([10, 20]):", 
    await sendRpcRequest(jsonrpc.request(3, "add", [10, 20]), false, true));
  console.log("✅ API Key Auth - greet({ name: 'Bob' }):", 
    await sendRpcRequest(jsonrpc.request(4, "greet", { name: "Bob" }), false, true));
  console.log("✅ API Key Auth - notification:", 
    await sendRpcRequest(jsonrpc.notification("log", { message: "Hello from API Key" }), true, true));

  // Test with no authentication (should fail)
  console.log("\n======= NO AUTHENTICATION TESTS (SHOULD FAIL) =======");
  console.log("🚫 No Auth - add([1, 2]):", 
    await sendRpcRequest(jsonrpc.request(5, "add", [1, 2]), false, false));
  console.log("🚫 No Auth - greet({ name: 'Charlie' }):", 
    await sendRpcRequest(jsonrpc.request(6, "greet", { name: "Charlie" }), false, false));
  console.log("🚫 No Auth - notification:", 
    await sendRpcRequest(jsonrpc.notification("log", { message: "This shouldn't work" }), true, false));

  // Reset authentication mode to original state
  AUTH_MODE = originalAuthMode;
}

test();

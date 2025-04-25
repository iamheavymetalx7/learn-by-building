const express = require("express");
const jsonrpc = require("jsonrpc-lite");
const bodyParser = require("body-parser");
const jwt = require("jsonwebtoken");
require("dotenv").config();


const app = express();
app.use(bodyParser.json());

const JWT_SECRET = process.env.JWT_SECRET || "super-secret";
const VALID_API_KEYS = new Set(["my-api-key-123", "another-key-456"]);


// Auth middleware - JWT or API Key
// here: authenticate middleware runs first.
// If authentication fails, it can stop the request and return an error.
function authenticate(req, res, next) {
    const authHeader = req.headers["authorization"];
    const apiKey = req.headers["x-api-key"];
  
    if (authHeader?.startsWith("Bearer ")) {
      const token = authHeader.split(" ")[1];
      try {
        const decoded = jwt.verify(token, JWT_SECRET);
        req.user = decoded;
        return next();
      } catch (err) {
        return res
          .status(401)
          .json(jsonrpc.error(null, jsonrpc.JsonRpcError.invalidRequest("Invalid JWT")));
      }
    } else if (apiKey && VALID_API_KEYS.has(apiKey)) {
      req.apiKey = apiKey;
      return next();
    } else {
      return res
        .status(401)
        .json(jsonrpc.error(null, jsonrpc.JsonRpcError.invalidRequest("Unauthorized")));
    }
  }


const methods = {
add: (params) => {
    if (!Array.isArray(params) || params.length !== 2)
    throw jsonrpc.JsonRpcError.invalidParams("Bad params, no sum!");
    return params[0] + params[1];
},
greet: (params) => {
    if (!params?.name)
    throw jsonrpc.JsonRpcError.invalidParams("No name, no fame!");
    return `Yo, ${params.name}, what’s good?`;
},
log: (params) => {
    if (!params?.message)
    throw jsonrpc.JsonRpcError.invalidParams("No message to log!");
    console.log(`Notification: ${params.message}`);
    return null;
},
};
  
app.post("/rpc", authenticate, (req, res) => {
    const parsed = jsonrpc.parseObject(req.body);
    console.log(parsed);
  
    if (parsed.type === "invalid") {
      return res
        .status(400)
        .json(jsonrpc.error(null, jsonrpc.JsonRpcError.invalidRequest()));
    }
  
    const { type, payload } = parsed;
  
    if (type === "notification") {
      try {
        if (!methods[payload.method]) throw jsonrpc.JsonRpcError.methodNotFound();
        methods[payload.method](payload.params);
        return res.status(204).send();
      } catch (error) {
        return res.status(204).send();
      }
    }
  
    if (type === "request") {
      try {
        if (!methods[payload.method]) throw jsonrpc.JsonRpcError.methodNotFound();
        const result = methods[payload.method](payload.params);
        res.json(jsonrpc.success(payload.id, result));
      } catch (error) {
        res.status(400).json(jsonrpc.error(payload.id, error));
      }
    }
  });


  app.get("/token", (req, res) => {
    const token = jwt.sign({ user: "testUser" }, JWT_SECRET, { expiresIn: "1h" });
    res.json({ token });
  });
  app.listen(3000, () =>
    console.log("🔗 JSON-RPC server at http://localhost:3000")
  );
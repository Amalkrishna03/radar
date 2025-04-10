import fs from "node:fs";
import openapiTS, { astToString } from "openapi-typescript";

const backend = process.env.BACKEND ?? "http://localhost:8000"

try {
    const ast = await openapiTS(new URL("/api/openapi.json", backend));
    const contents = astToString(ast);
    
    // (optional) write to file
    fs.writeFileSync("./openapi.d.ts", contents);
}
catch (e) {
    console.error(e);
}

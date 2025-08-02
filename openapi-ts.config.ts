import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "backend/schema.yml",
  output: {
    path: "frontend/src/api",
    format: "prettier",
  },
  client: "axios",
  useOptions: true,
});

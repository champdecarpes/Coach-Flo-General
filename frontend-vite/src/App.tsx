import * as Sentry from "@sentry/react";
import { parse } from "cookie";
import React from "react";

import { OpenAPI } from "./api";

OpenAPI.interceptors.request.use((request) => {
  const { csrftoken } = parse(document.cookie);
  if (request.headers && csrftoken) {
    request.headers["X-CSRFTOKEN"] = csrftoken;
  }
  return request;
});

export default function App() {
  return (
    <React.StrictMode>
      <p>TEST PLEASE</p>
      <Sentry.ErrorBoundary fallback={<p>An error has occurred</p>}>
        <p>Test route</p>
        <p>Test route</p>
      </Sentry.ErrorBoundary>
    </React.StrictMode>
  );
}

// export default App;

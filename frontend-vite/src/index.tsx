import {DevSupport} from "@react-buddy/ide-toolbox";
import * as Sentry from "@sentry/browser";
import {createRoot} from "react-dom/client";

import {ComponentPreviews, useInitial} from "../dev";

import App from "./App";

import "../sass/style.scss";
import React from "react";

Sentry.init({
  dsn: window.SENTRY_DSN,
  release: window.COMMIT_SHA,
});

const root = createRoot(document.getElementById("rootID") as HTMLElement)

if (!root) {
  console.log("Huina");
} else {
  console.log(root)
}

root.render(
  <React.StrictMode>
    <DevSupport ComponentPreviews={<ComponentPreviews/>} useInitialHook={useInitial}>
      <App/>
    </DevSupport>
  </React.StrictMode>
);

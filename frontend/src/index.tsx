import { DevSupport } from "@react-buddy/ide-toolbox";
import * as Sentry from "@sentry/browser";
import { createRoot } from "react-dom/client";

import { ComponentPreviews, useInitial } from "dev";

import App from "./App";

import "../sass/style.scss";

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
  // <DevSupport ComponentPreviews={ComponentPreviews} useInitialHook={useInitial}>
  <App />,
  // </DevSupport>
);

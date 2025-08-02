"use strict";

module.exports = {
  moduleNameMapper: {
    "^.+\\.(css|scss|png|svg|jpg|jpeg|gif|webp)$": "jest-transform-stub",
  },
  transformIgnorePatterns: ["node_modules/*"],
  modulePaths: ["frontend", "frontend/src", "frontend/src/app"],
  setupFilesAfterEnv: ["./jest.setup.src"],
  testEnvironment: "jsdom",
  collectCoverageFrom: ["frontend/src/**/*.{src,jsx,ts,tsx}"],
  coveragePathIgnorePatterns: [
    "frontend/src/store.src",
    "frontend/src/index.src",
    "frontend/src/constants/*",
    "frontend/src/pages/*",
    "frontend/src/tests/*",
  ],
  coverageThreshold: {
    global: {
      statements: 10,
    },
  },
  transform: {
    "^.+\\.(t|j)sx?$": "@swc/jest",
  },
};

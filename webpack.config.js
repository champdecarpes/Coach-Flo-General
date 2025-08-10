// Require Node.js and Webpack dependencies
const path = require("path");
const fs = require("fs");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const {WebpackManifestPlugin} = require("webpack-manifest-plugin");
const CaseSensitivePathsPlugin = require("case-sensitive-paths-webpack-plugin");
const ModuleNotFoundPlugin = require("react-dev-utils/ModuleNotFoundPlugin");
const InterpolateHtmlPlugin = require("react-dev-utils/InterpolateHtmlPlugin");
const ReactRefreshWebpackPlugin = require("@pmmmwh/react-refresh-webpack-plugin");
const ForkTsCheckerWebpackPlugin = require("react-dev-utils/ForkTsCheckerWebpackPlugin");
const ESLintPlugin = require("eslint-webpack-plugin");
const getClientEnvironment = require("react-dev-utils/getClientEnvironment");
const BundleTracker = require("webpack-bundle-tracker");

// Define paths for the project
const appPath = path.resolve(__dirname);
const appSrc = path.resolve(__dirname, "frontend/src");
const appPublic = path.resolve(__dirname, "frontend/public");
const appBuild = path.resolve(__dirname, "frontend/webpack_bundles");
const appHtml = path.join(appPublic, "index.html");
const appNodeModules = path.resolve(__dirname, "node_modules");
const appTsConfig = path.resolve(__dirname, "tsconfig.json");

// Environment variables for injecting into the app
const env = getClientEnvironment("/");

// Source maps configuration
const shouldUseSourceMap = process.env.GENERATE_SOURCEMAP !== "false";
const imageInlineSizeLimit = parseInt(process.env.IMAGE_INLINE_SIZE_LIMIT || "10000");

// Check if TypeScript is setup
const useTypeScript = fs.existsSync(appTsConfig);

// Style file regexes
const cssRegex = /\.css$/;
const cssModuleRegex = /\.module\.css$/;
const sassRegex = /\.(scss|sass)$/;
const sassModuleRegex = /\.module\.(scss|sass)$/;

// Check if JSX runtime is available
const hasJsxRuntime = (() => {
  if (process.env.DISABLE_NEW_JSX_TRANSFORM === "true") {
    return false;
  }
  try {
    require.resolve("react/jsx-runtime");
    return true;
  } catch (e) {
    return false;
  }
})();

// Common function to get style loaders
const getStyleLoaders = (cssOptions, preProcessor) => {
  const loaders = [
    isDev && require.resolve("style-loader"),
    !isDev && {
      loader: MiniCssExtractPlugin.loader,
      options: {publicPath: "../../"},
    },
    {
      loader: require.resolve("css-loader"),
      options: cssOptions,
    },
    {
      loader: require.resolve("postcss-loader"),
      options: {
        postcssOptions: {
          ident: "postcss",
          config: false,
          plugins: [
            "postcss-flexbugs-fixes",
            ["postcss-preset-env", {autoprefixer: {flexbox: "no-2009"}, stage: 3}],
            "postcss-normalize",
          ],
        },
        sourceMap: !isDev ? shouldUseSourceMap : isDev,
      },
    },
  ].filter(Boolean);
  if (preProcessor) {
    loaders.push(
      {
        loader: require.resolve("resolve-url-loader"),
        options: {
          sourceMap: !isDev ? shouldUseSourceMap : isDev,
          root: appSrc,
        },
      },
      {
        loader: require.resolve(preProcessor),
        options: {sourceMap: true},
      }
    );
  }
  return loaders;
};

module.exports = (env, argv) => {
  // Determine development or production mode
  const isDev = argv.mode === "development";
  const isProd = !isDev;

  return {
    // Set target to browserslist for compatibility
    target: ["browserslist"],
    // Show only errors and warnings in Webpack output
    stats: "errors-warnings",
    mode: isDev ? "development" : "production",
    // Stop compilation early in production
    bail: isProd,
    // Configure source maps
    devtool: isProd ? (shouldUseSourceMap ? "source-map" : false) : "cheap-module-source-map",
    // Define entry points
    entry: {
      main: "./frontend/src/index.tsx",
      previews: "./frontend/dev/previews.tsx",
    },
    // Output configuration
    output: {
      path: appBuild,
      pathinfo: isDev,
      filename: isProd ? "static/js/[name].[contenthash:8].js" : "static/js/[name].js",
      chunkFilename: isProd
        ? "static/js/[name].[contenthash:8].chunk.js"
        : "static/js/[name].chunk.js",
      assetModuleFilename: "static/media/[name].[hash][ext]",
      publicPath: isDev ? "/" : "auto",
      devtoolModuleFilenameTemplate: isProd
        ? (info) => path.relative(appSrc, info.absoluteResourcePath).replace(/\\/g, "/")
        : (info) => path.resolve(info.absoluteResourcePath).replace(/\\/g, "/"),
      clean: isProd,
    },
    // Cache configuration for faster rebuilds
    cache: {
      type: "filesystem",
      version: require("./package.json").version,
      cacheDirectory: path.resolve(appNodeModules, ".cache/webpack"),
      store: "pack",
      buildDependencies: {
        defaultWebpack: ["webpack/lib/"],
        config: [__filename],
        tsconfig: [appTsConfig].filter((f) => fs.existsSync(f)),
      },
    },
    // Development server configuration
    devServer: {
      allowedHosts: "all",
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
      },
      compress: true,
      static: {
        directory: appPublic,
        publicPath: ["/"],
      },
      client: {
        webSocketURL: {
          hostname: process.env.WDS_SOCKET_HOST || "0.0.0.0",
          pathname: process.env.WDS_SOCKET_PATH || "/ws",
          port: process.env.WDS_SOCKET_PORT || 3000,
        },
        overlay: {
          errors: true,
          warnings: false,
        },
      },
      devMiddleware: {
        publicPath: "/",
      },
      https: false,
      host: "0.0.0.0",
      port: 3000,
      historyApiFallback: {
        disableDotRule: true,
        index: "/",
      },
      hot: true,
    },
    // Module resolution configuration
    resolve: {
      modules: [appNodeModules, appSrc],
      extensions: [".js", ".jsx", ".ts", ".tsx"],
      alias: {
        src: path.resolve(__dirname, "frontend/src"),
        dev: path.resolve(__dirname, "frontend/dev"),
        react: path.join(appNodeModules, "react"),
        "react-dom": path.join(appNodeModules, "react-dom"),
      },
    },
    // Module rules for processing files
    module: {
      strictExportPresence: true,
      rules: [
        // Handle source maps in node_modules
        shouldUseSourceMap && {
          enforce: "pre",
          exclude: /@babel(?:\/|\\{1,2})runtime/,
          test: /\.(js|mjs|jsx|ts|tsx|css)$/,
          loader: require.resolve("source-map-loader"),
        },
        {
          oneOf: [
            // Handle images
            {
              test: [/\.bmp$/, /\.gif$/, /\.jpe?g$/, /\.png$/],
              type: "asset",
              parser: {
                dataUrlCondition: {maxSize: imageInlineSizeLimit},
              },
            },
            // Handle SVGs with @svgr/webpack
            {
              test: /\.svg$/,
              use: [
                {
                  loader: require.resolve("@svgr/webpack"),
                  options: {
                    prettier: false,
                    svgo: false,
                    svgoConfig: {plugins: [{removeViewBox: false}]},
                    titleProp: true,
                    ref: true,
                  },
                },
                {
                  loader: require.resolve("file-loader"),
                  options: {
                    name: "static/media/[name].[hash].[ext]",
                  },
                },
              ],
              issuer: {and: [/\.(ts|tsx|js|jsx)$/]},
            },
            // Process JS/TS files with swc-loader
            {
              test: /\.(js|mjs|jsx|ts|tsx)$/,
              include: appSrc,
              use: {
                loader: "swc-loader",
                options: {
                  jsc: {
                    parser: {syntax: "typescript", tsx: true},
                    transform: {
                      react: {
                        runtime: hasJsxRuntime ? "automatic" : "classic",
                        refresh: isDev,
                      },
                    },
                  },
                  cacheDirectory: true,
                  cacheCompression: false,
                  sourceMaps: shouldUseSourceMap,
                },
              },
            },
            // Process CSS
            {
              test: cssRegex,
              exclude: cssModuleRegex,
              use: getStyleLoaders({
                importLoaders: 1,
                sourceMap: isProd ? shouldUseSourceMap : isDev,
                modules: {mode: "icss"}
              }),
              sideEffects: true,
            },
            // Process CSS Modules
            {
              test: cssModuleRegex,
              use: getStyleLoaders({
                importLoaders: 1,
                sourceMap: isProd ? shouldUseSourceMap : isDev,
                modules: {mode: "local", getLocalIdent: require("react-dev-utils/getCSSModuleLocalIdent")},
              }),
            },
            // Process SASS
            {
              test: sassRegex,
              exclude: sassModuleRegex,
              use: getStyleLoaders(
                {importLoaders: 3, sourceMap: isProd ? shouldUseSourceMap : isDev, modules: {mode: "icss"}},
                "sass-loader"
              ),
              sideEffects: true,
            },
            // Process SASS Modules
            {
              test: sassModuleRegex,
              use: getStyleLoaders(
                {
                  importLoaders: 3,
                  sourceMap: isProd ? shouldUseSourceMap : isDev,
                  modules: {mode: "local", getLocalIdent: require("react-dev-utils/getCSSModuleLocalIdent")},
                },
                "sass-loader"
              ),
            },
            // Fallback for other assets
            {
              exclude: [/\.(js|mjs|jsx|ts|tsx)$/, /\.html$/, /\.json$/],
              type: "asset/resource",
            },
          ],
        },
      ].filter(Boolean),
    },
    // Webpack plugins
    plugins: [
      // Generate index.html with injected scripts
      new HtmlWebpackPlugin({
          inject: true,
          template: appHtml,
          ...(isProd && {
            minify: {
              removeComments: true,
              collapseWhitespace: true,
              removeRedundantAttributes: true,
              useShortDoctype: true,
              removeEmptyAttributes: true,
              removeStyleLinkTypeAttributes: true,
              keepClosingSlash: true,
              minifyJS: true,
              minifyCSS: true,
              minifyURLs: true,
            },
          }),
        }
      ),
      // Inject environment variables into index.html
      new InterpolateHtmlPlugin(HtmlWebpackPlugin, env.raw),
      // Provide context for module not found errors
      new ModuleNotFoundPlugin(appPath),
      // Define environment variables for JavaScript
      new webpack.DefinePlugin(env.stringified),
      // Enable hot reloading in development
      isDev && new ReactRefreshWebpackPlugin({overlay: false}),
      // Enforce case-sensitive paths
      isDev && new CaseSensitivePathsPlugin(),
      // Extract CSS in production
      isProd &&
      new MiniCssExtractPlugin({
        filename: "static/css/[name].[contenthash:8].css",
        chunkFilename: "static/css/[name].[contenthash:8].chunk.css",
      }),
      // Generate asset manifest
      new WebpackManifestPlugin({
        fileName: "asset-manifest.json",
        publicPath: "/",
      }),
      // TypeScript type checking
      useTypeScript &&
      new ForkTsCheckerWebpackPlugin({
        async: isDev,
        typescript: {
          typescriptPath: require.resolve("typescript"),
          configOverwrite: {
            compilerOptions: {
              sourceMap: isProd ? shouldUseSourceMap : isDev,
              skipLibCheck: true,
              inlineSourceMap: false,
              declarationMap: false,
              noEmit: true,
              incremental: true,
            },
          },
          context: appPath,
          diagnosticOptions: {syntactic: true},
          mode: "write-references",
        },
        issue: {
          include: [{file: "**/src/**/*.{ts,tsx}"}],
          exclude: [
            {file: "**/src/**/__tests__/**"},
            {file: "**/src/**/?(*.){spec|test}.*"},
          ],
        },
        logger: {infrastructure: "silent"},
      }),
      // ESLint integration
      new ESLintPlugin({
        extensions: ["js", "mjs", "jsx", "ts", "tsx"],
        formatter: require.resolve("react-dev-utils/eslintFormatter"),
        eslintPath: require.resolve("eslint"),
        failOnError: !isDev,
        context: appSrc,
        cache: true,
        cacheLocation: path.resolve(appNodeModules, ".cache/.eslintcache"),
        cwd: appPath,
        resolvePluginsRelativeTo: __dirname,
        baseConfig: {
          extends: [require.resolve("eslint-config-react-app/base")],
          rules: {...(!hasJsxRuntime && {"react/react-in-jsx-scope": "error"})},
        },
      }),
      // Bundle tracker for your specific use case
      new BundleTracker({
        path: __dirname,
        filename: "webpack-stats.json",
      }),
    ].filter(Boolean),
    // Optimization settings
    optimization: {
      minimize: isProd,
      minimizer: [
        new TerserPlugin({
          terserOptions: {
            parse: {ecma: 8},
            compress: {ecma: 5, warnings: false, comparisons: false, inline: 2},
            mangle: {safari10: true},
            output: {ecma: 5, comments: false, ascii_only: true},
          },
        }),
        new CssMinimizerPlugin(),
      ],
      splitChunks: {chunks: "all"},
    },
    // Disable performance hints
    performance: false,
  };
};

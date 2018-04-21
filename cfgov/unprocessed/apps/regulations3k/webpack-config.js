/* ==========================================================================
   Settings for webpack JavaScript bundling system.
   ========================================================================== */


const BROWSER_LIST = require( '../../../../config/browser-list-config' );
const path = require( 'path' );
const SWPrecacheWebpackPlugin = require( 'sw-precache-webpack-plugin' );
const UglifyWebpackPlugin = require( 'uglifyjs-webpack-plugin' );

/* Public path for service workers precache plugin to scrape for assets. */
const PUBLIC_PATH = 'http://build5.demo.cfpb.gov/eregulations3k/';

/* Webpack plugin that generates a service worker using sw-precache that will
   cache webpack's bundles' emitted assets.
   https://github.com/goldhand/sw-precache-webpack-plugin */
const SERVICE_WORKERS_PRECACHE_CONFIG = new SWPrecacheWebpackPlugin( {
  cacheId: 'my-project-name',
  dontCacheBustUrlsMatching: /\.\w{8}\./,
  filename: 'service-worker.js',
  minify: true,
  navigateFallback: PUBLIC_PATH + 'index.html',
  staticFileGlobsIgnorePatterns: [ /\.map$/, /asset-manifest\.json$/ ]
} );

/* Set warnings to true to show linter-style warnings.
   Set mangle to false and beautify to true to debug the output code. */
const COMMON_UGLIFY_CONFIG = new UglifyWebpackPlugin( {
  cache: true,
  parallel: true,
  uglifyOptions: {
    ie8: false,
    ecma: 5,
    warnings: false,
    mangle: true,
    output: {
      comments: false,
      beautify: false
    }
  }
} );

/* Commmon webpack 'module' option used in each configuration.
   Runs code through Babel and uses global supported browser list. */
const COMMON_MODULE_CONFIG = {
  rules: [ {
    test: /\.js$/,

    /* The below regex will capture all node modules that start with `cf`
      or atomic-component. Regex test: https://regex101.com/r/zizz3V/1/. */
    exclude: /node_modules\/(?:cf.+|atomic-component)/,
    use: {
      loader: 'babel-loader?cacheDirectory=true',
      options: {
        presets: [ [ 'babel-preset-env', {
          targets: {
            browsers: BROWSER_LIST.LAST_2_IE_9_UP
          },
          debug: true
        } ] ]
      }
    }
  } ]
};

const STATS_CONFIG = {
  stats: {
    entrypoints: false
  }
};

const conf = {
  cache: true,
  module: COMMON_MODULE_CONFIG,
  mode: 'production',
  output: {
    filename: '[name]',
    jsonpFunction: 'eregs',
    path: path.resolve( __dirname, 'src/bundles/' ),
    publicPath: PUBLIC_PATH
  },
  plugins: [
    SERVICE_WORKERS_PRECACHE_CONFIG,
    COMMON_UGLIFY_CONFIG
  ],
  stats: STATS_CONFIG.stats
};

module.exports = { conf };

var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')
var config = require('./webpack.base.config.js')

config.devtool = "#eval-source-map"

config.output.path = require('path').resolve('./djreact/static/bundles/local/')
config.output.publicPath = 'http://127.0.0.1:3000/static/bundles/local/'

console.log(config.output.path)
config.ip = '127.0.0.1',

config.entry = {
  // Add as many entry points as you have container-react-components here
  SampleApp:[
    'webpack-dev-server/client?http://' + config.ip + ':8000',
    './reactjs/SampleApp'
  ],
  SampleApp2: [
    'webpack-dev-server/client?http://' + config.ip + ':8000',
    './reactjs/SampleApp2',
  ],
  PDF:[
    'webpack-dev-server/client?http://' + config.ip + ':8000',
    './reactjs/PDF'
  ],
  vendors: ['react'],
},

config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoErrorsPlugin(),
  new BundleTracker({filename: './webpack-stats-stage.json'}),
  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('staging'),
      'BASE_API_URL': JSON.stringify('http://127.0.0.1:8000/static/bundles/local/'),
  }}),

  // keeps hashes consistent between compilations
  new webpack.optimize.OccurenceOrderPlugin(),

  // minifies your code
  new webpack.optimize.UglifyJsPlugin({
    compressor: {
      warnings: false
    }
  })
])

// Add a loader for JSX files
config.module.loaders.push(
  { test: /\.jsx?$/, exclude: /node_modules/, loaders: ['react-hot', 'babel']}
)

module.exports = config

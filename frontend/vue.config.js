const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    },
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false)
      })
    ]
  },
  devServer: {
    host: 'localhost',
    port: 8080,
    hot: false, // Disable hot reload to stop WebSocket errors
    liveReload: false, // Disable live reload
    client: {
      logging: 'none', // Hide client logs
      overlay: {
        errors: true,
        warnings: false,
        runtimeErrors: false
      }
    },
    proxy: {
      '/app': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        ws: true
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
// webpack.config.js
module.exports = {
    // ...
    module: {
      rules: [
        {
          test: /\.[tj]sx?$/,
          include: /(src)/,
          use: [{
            loader: 'babel-loader',
            options: {
              presets: [
                ['@babel/preset-env', { useBuiltIns: "usage", corejs: 3 }],
                ['@babel/preset-typescript', { allowNamespaces: true }]
              ],
              plugins: ['@babel/plugin-syntax-dynamic-import']
            }
          }]
        },
        // ...
      ]
    }
   };
   
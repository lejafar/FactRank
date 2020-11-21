module.exports = {
  publicPath: '',
  chainWebpack: config => {
    config.module.rules.delete("svg");
    config.module.rules.delete("md");
  },
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.svg$/,
          loader: 'vue-svg-loader',
        },
        {
          test: /\.md$/,
            use: [
                {
                    loader: 'vue-loader'
                },
                {
                    loader: 'vmark-loader'
                }
            ]
        }
      ]
    },
  }
};

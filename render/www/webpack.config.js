const path = require("path");
const webpack = require('webpack');

const CSS_DIR = path.resolve(__dirname, './static/render/css');
const JS_DIR = path.resolve(__dirname, './static/render/js');
const BUILD_DIR = path.resolve(__dirname, './static/render/dist');

module.exports = {
    entry: {
        index: [`${JS_DIR}/index.jsx`],
        login: [`${JS_DIR}/login.jsx`],
        register: [`${JS_DIR}/register.jsx`],
        list_view: [`${JS_DIR}/list_view.jsx`]
    },
    output: {
        path: BUILD_DIR,
        filename: '[name].js'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: ["babel-loader"]
            },
            {
                test: /\.jsx$/,
                exclude: /node_modules/,
                use: ["babel-loader"]
            },
            {
                test: /\.css$/,
                use: ["style-loader", "css-loader"]
            }
        ]
    },

    plugins: []
};
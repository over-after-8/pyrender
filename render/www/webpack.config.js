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

        list_view: [`${JS_DIR}/list_view.jsx`],
        add_view: [`${JS_DIR}/add_view.jsx`],
        detail_view: [`${JS_DIR}/detail_view.jsx`],
        edit_view: [`${JS_DIR}/edit_view.jsx`],

        user_add_view: [`${JS_DIR}/admin/admin_user_add_view.jsx`],
        user_change_password_view: [`${JS_DIR}/admin/admin_user_change_password_view.jsx`]

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
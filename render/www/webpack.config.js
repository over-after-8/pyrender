const path = require("path");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

const JS_DIR = path.resolve(__dirname, './static/js');
const BUILD_DIR = path.resolve(__dirname, './static/dist');

const AUTH_JS_DIR = path.resolve(__dirname, './applications/authentication/static/js');
const AUTH_BUILD_DIR = path.resolve(__dirname, './applications/authentication/static/dist');

const ADMIN_JS_DIR = path.resolve(__dirname, './applications/administration/static/js');
const ADMIN_BUILD_DIR = path.resolve(__dirname, './applications/administration/static/dist');

const configMain = {
    mode: "development",
    resolve: {
        extensions: ['.js', '.jsx']
    },
    entry: {
        index: [`${JS_DIR}/index.jsx`],
        utils: [`${JS_DIR}/components/utils.jsx`],

        list_view: [`${JS_DIR}/list_view.jsx`],
        add_view: [`${JS_DIR}/add_view.jsx`],
        detail_view: [`${JS_DIR}/detail_view.jsx`],
        edit_view: [`${JS_DIR}/edit_view.jsx`],
        delete_view: [`${JS_DIR}/delete_view.jsx`],
    },
    output: {
        path: BUILD_DIR,
        filename: '[name].js',
        publicPath: '/static/dist/'
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ["babel-loader"]
            },
            {
                test: /\.css$/,
                use: ["style-loader", "css-loader"]
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin()
    ],
    devtool: false
}

const configAuth = {
    mode: "development",
    resolve: {
        extensions: ['.js', '.jsx']
    },
    entry: {
        login: [`${AUTH_JS_DIR}/login.jsx`],
        register: [`${AUTH_JS_DIR}/register.jsx`],
        index: [`${AUTH_JS_DIR}/index.jsx`],
    },
    output: {
        path: AUTH_BUILD_DIR,
        filename: '[name].js',
        publicPath: '/auth/dist/'
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ["babel-loader"]
            },
            {
                test: /\.css$/,
                use: ["style-loader", "css-loader"]
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin()
    ],
    devtool: false
}

const configAdmin = {
    mode: "development",
    resolve: {
        extensions: ['.js', '.jsx']
    },
    entry: {
        admin_user_add_view: [`${ADMIN_JS_DIR}/admin_user_add_view.jsx`],
        admin_user_change_password_view: [`${ADMIN_JS_DIR}/admin_user_change_password_view.jsx`]
    },
    output: {
        path: ADMIN_BUILD_DIR,
        filename: '[name].js',
        publicPath: '/administration/dist/'
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ["babel-loader"]
            },
            {
                test: /\.css$/,
                use: ["style-loader", "css-loader"]
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin()
    ],
    devtool: false
}

module.exports = [configMain, configAuth, configAdmin];

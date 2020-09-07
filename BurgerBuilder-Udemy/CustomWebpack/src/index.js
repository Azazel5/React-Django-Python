import './index.css'
import React from 'react'
import ReactDOM from 'react-dom'
import {BrowserRouter} from 'react-router-dom'
import App from './App'

/**
 * Install webpack-cli and add the scripts items. Example - setup start with the webpack-dev-server
 * that you installed with --save-dev configuration. You have to also create a webpack.config.js 
 * as webpack doesn't understand how to handle JSX. After setting the entry point, development mode, 
 * output, ... configurations, you'll need to install babel to handle ES6 javascript/JSX. 
 * For babel, you will install a bunch of packages like @babel/preset-react etc.
 * CSS files/modules need to be supported as well. You gotta do the same for images with url-loader.
 * Finally all your js/css/images needs to be injected into the index.html, so you need html-webpack-plugin
 */

const app = (
    <BrowserRouter>
        <App />
    </BrowserRouter>
)

ReactDOM.render(app, document.getElementById('root'))

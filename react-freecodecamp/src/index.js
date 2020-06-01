import React from 'react'
import ReactDom from 'react-dom'
import './index.css';
import {App} from './components/App'
import * as serviceWorker from './serviceWorker';

// ReactDom.render() takes your component and attaches it to the index.html's root div.  
ReactDom.render(
  <App />,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

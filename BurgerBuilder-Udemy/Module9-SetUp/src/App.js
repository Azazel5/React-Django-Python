import React, { Component } from 'react';
import {BrowserRouter} from 'react-router-dom'
import Blog from './containers/Blog/Blog';

/**
 * You can use XMLHttp/fetch api to make requests; however, you can also use axios, which is a 
 * pretty popular choice. 
 */
class App extends Component {
  render() {
    return (
      <BrowserRouter>
      <div className="App">
        <Blog />
      </div>
      </BrowserRouter>
    );
  }
}

export default App;

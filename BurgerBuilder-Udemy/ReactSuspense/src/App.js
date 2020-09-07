import React, { Component, Suspense } from 'react';
import { BrowserRouter, Route, NavLink } from 'react-router-dom';
import User from './containers/User';
import Welcome from './containers/Welcome';

// This is similar to how you lazily loaded in the module9 files.
const Posts = React.lazy(() => import('./containers/Posts'))

// This is a great example to show that suspense can be used to lazily load other things too, not
// just navigation pages. 
class App extends Component {
  state = {
    show: false 
  }

  modeHandler = () => {
    this.setState(prevState => {
      return {show: !prevState.show}
    })
  }

  render() {
    return (
      <React.Fragment>
      <button onClick={this.modeHandler}>Toggle Mode</button>
      {this.state.show ?
        <Suspense fallback={<div>Loading...</div>}>
          <Posts />
        </Suspense>: <User />
      }
      </React.Fragment>

      // You can setup a basename prop in the BrowserRouter to configure any root name for the requests.
      // <BrowserRouter>
      //   <React.Fragment>
      //     <nav>
      //       <NavLink to="/user">User Page</NavLink> |&nbsp;
      //       <NavLink to="/posts">Posts Page</NavLink>
      //     </nav>
      //     <Route path="/" component={Welcome} exact />
      //     <Route path="/user" component={User} />
      //     <Route path="/posts" render={() =>
      //       <Suspense fallback={<div>Loading...</div>}>
      //         <Posts />
      //       </Suspense>} />
      //   </React.Fragment>
      // </BrowserRouter>
    );
  }
}

export default App;

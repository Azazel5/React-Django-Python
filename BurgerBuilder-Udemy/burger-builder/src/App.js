import React, { Component } from 'react';
import Layout from './hoc/Layout/Layout'
import BurgerBuilder from './containers/BurgerBuilder/BurgerBuilder'
import { Route, Switch, withRouter, Redirect } from 'react-router-dom'
import Logout from './containers/Auth/Logout/Logout'

import * as actionCreators from './store/actions/index'
import { connect } from 'react-redux'
import asyncComponent from './hoc/AsyncComponent/AsyncComponent'

/**
 *  Using CSS modules: name your css files as {file_name}.module.css, import {keyword} from 
 *  './{file_name}.module.css', and use like <button class={keyword.css_class_name}
 */

// Using the asyncComponent we defined in module 9 to lazily load checkout, orders, and auth components
const asyncCheckout = asyncComponent(() => {
  return import('./containers/Checkout/Checkout')
})

const asyncOrders = asyncComponent(() => {
  return import('./containers/Orders/Orders')
})

const asyncAuth = asyncComponent(() => {
  return import('./containers/Auth/Auth')
})

class App extends Component {
  componentDidMount() {
    this.props.onTryAutoSignUp()
  }

  render() {
    let routes = (
      <Switch>
        <Route path="/auth" component={asyncAuth} />
        <Route path="/" component={BurgerBuilder} exact />
        <Redirect to="/" />
      </Switch>

    )

    if (this.props.isAuthenticated) {
      routes = (
        <Switch>
          <Route path="/checkout" component={asyncCheckout} />
          <Route path="/orders" component={asyncOrders} />
          <Route path="/logout" component={Logout} />
          <Route path="/" component={BurgerBuilder} exact />
          <Redirect to="/" />
        </Switch>
      )
    }
    return (
      <div>
        <Layout>
          {routes}
        </Layout>
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    isAuthenticated: state.auth.token !== null
  }
}

const mapDispatchToProps = dispatch => {
  return {
    onTryAutoSignUp: () => dispatch(actionCreators.authCheckState())
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(App))

/**
 * Hookified App.js *
  const Checkout = React.lazy(() => {
  return import('./containers/Checkout/Checkout')
})

  const Orders = React.lazy(() => {
  return import('./containers/Orders/Orders')
})

const Auth = React.lazy(() => {
  return import('./containers/Auth/Auth')
})
 * const app = props => {
 *   useEffect(() => {
 *      props.onTryAutoSignUp()
 *  }, [])
 *
 *   let routes = (
      <Switch>
        <Route path="/auth" render={() => Auth)} />
        <Route path="/" component={BurgerBuilder} exact />
        <Redirect to="/" />
      </Switch>

    )

    if (props.isAuthenticated) {
      routes = (
        <Switch>
          <Route path="/checkout" render={() => <Checkout />} />
          <Route path="/orders" render={() => <Orders />} />
          <Route path="/logout" component={Logout} />
          <Route path="/" component={BurgerBuilder} exact />
          <Redirect to="/" />
        </Switch>
      )
    }
    return (
      <div>
        <Layout>
        <Suspense fallback={<p>Loading...</p>}>
          {routes}
        </Suspense>
        </Layout>
      </div>
    );
  }
 *
 */
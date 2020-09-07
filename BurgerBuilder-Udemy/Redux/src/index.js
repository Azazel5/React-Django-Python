import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import {createStore, combineReducers, applyMiddleware, compose} from 'redux'
import {Provider} from 'react-redux'

import counterReducer from './store/reducers/counter'
import resultReducer from './store/reducers/result'
import App from './App';
import registerServiceWorker from './registerServiceWorker';

import thunk from 'redux-thunk'

const rootReducer = combineReducers({
    counter: counterReducer, 
    results: resultReducer
})

// Creating a middleware: triple nested function middleware
const logger = store => {
    return next => {
        return action => {
            console.log('[Middleware] dispatching', action)
            const result = next(action)
            console.log('[Middleware] next state', store.getState())
            return result
        }
    }
}

// The second argument of createStore is called an enhancer or a middleware.  
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose
const store = createStore(rootReducer, composeEnhancers(applyMiddleware(logger, thunk)))
ReactDOM.render(<Provider store={store}><App /></Provider>, document.getElementById('root'));
registerServiceWorker();

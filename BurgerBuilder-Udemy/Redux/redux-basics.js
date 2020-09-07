const redux = require('redux')
/**
 * Redux is independent of react and is run by Node js. 
 * The redux workflow is: store, reducer, action, dispatch, subscription. A store needs to 
 * be initialized to the reducer (we can have multiple reducers; they will be merged).
 * Here we're using node js to run this file using node {file_name}. A default state value is 
 * provided to the rootReducer function. The rootReducer must return the new state.
 * Dispatch takes a JS object which needs a type property, which is a unique identifier. 
 * You can pass a payload with a dispatch call.
 * Subscription informs you of the new state, so you know when to call getState in a sense.
 * Subscription informs you of any future dispatches. 
 */

const initialState = {
    counter: 0
}

const createStore = redux.createStore
const rootReducer = (state = initialState, action) => {
    if(action.type === 'INC_COUNTER') {
        return {
            ...state, 
            counter: state.counter + 1
        }
    }

    if(action.type === 'ADD_COUNTER') {
        return {
            ...state, 
            counter: state.counter + action.value 
        }
    }
    return state 
}

const store = createStore(rootReducer)

store.subscribe(() => {
    console.log('[Subscription]', store.getState())
    
})

// All uppercase is a convention for a type value 
store.dispatch({type: 'INC_COUNTER'})
store.dispatch({type: 'ADD_COUNTER', value: 10})


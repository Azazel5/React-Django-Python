import * as actionTypes from '../actions/actionTypes'
import updateObject from '../utility'

const initialState = {
    counter: 0, 
}

/**
 * Unlike this.setState, the returned/edited state is not merged with the previous state here. So
 * you gotta copy the other state values and change what you want in the one you want. Concat creates 
 * a new array, which is crucial to keep things immutable instead of push.
 * Remember, if you have an array of objects, calling the spread operator does copy the array, but the 
 * objects themselves still point to what they did before. If you have to touch the object, remember to 
 * spread that too.
 * You can split up the reducers by feature, as the app grows in size.
 * -----------------------------------------------------------------------------------------------------
 * You could create utility functions to cleanup this time further. 
 */
const reducer = (state = initialState, action) => {
    switch(action.type) {
        case actionTypes.INCREMENT:
            return updateObject(state, {counter: state.counter + 1})

        case actionTypes.DECREMENT: 
            return updateObject(state, {counter: state.counter - 1})

        case actionTypes.ADD:
            return updateObject(state, {counter: state.counter + action.value})

        case actionTypes.SUBTRACT:
            return updateObject(state, {counter: state.counter - action.value})
            
        default:
            return state
        }
}

export default reducer
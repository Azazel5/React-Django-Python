import * as actionTypes from '../actions/actionTypes'

export const saveResult = result => {
    return {
        type: actionTypes.STORE_RESULT,
        result: result
    }
}

/**
 * Here we're trying to execute an asynchronous codeblock in an action creater. We save the earlier 
 * block of code we had in storeResult to another function 'saveResult', and return a function which 
 * dispatches the 'saveResult' function. Make sure to pass on the payload to the saveResult because
 * that is the part which will be dispatched in the mapDispatchToProps as well.  
 * Action creators are the place to run asynchronous code versus reducer is the place where you 
 * update the state. Thus, the reducer should be the place where you place the transforming/performing
 * logic.
 * ---------------------------------------------------------------------------------------------------
 * If you do want to perform logic here, you would be well off knowing about the getState argument you 
 * can pass to the dispatch function (next to it). Try not to use it. Instead, if you truly need data 
 * here, just pass it on from where you have used mapDispatchToProps, and you'll get it here. 
 */
export const storeResult = result => {
    return (dispatch, getState) => {
        console.log(getState())
        setTimeout(() => {
            dispatch(saveResult(result))
        }, 2000)
    }
}
export const deleteResult = id => {
    return {
        type: actionTypes.DELETE_RESULT,
        resultId: id
    }
}
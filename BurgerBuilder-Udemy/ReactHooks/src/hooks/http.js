import { useReducer, useCallback } from 'react'

const initialState = {
    loading: false,
    error: null,
    data: null,
    extra: null,
    identifier: null
}
// The reducer which will judge whether it is a loading state or an error state, since they're
// closely tied up. 
const httpReducer = (httpState, action) => {
    switch (action.type) {
        case 'SEND':
            return { loading: true, error: null, data: null, extra: null, identifier: action.identifier }
        case 'RESPONSE':
            return { ...httpState, loading: false, data: action.responseData, extra: action.extra }
        case 'ERROR':
            return { loading: false, error: action.errorData }
        case 'CLEAR':
            return initialState
        default:
            throw new Error("Shouldn't be reached")
    }
}

/**
 * Here we are building a custom http request hook, and a problem we quickly face is:
 * custom hooks should be reusable in multiple components. How will you pass the HttpResponse
 * data back into the desired component?
 * We can add data to the reducer as state and pass it through the dispatch as a payload. Still, 
 * the state still lives here in the hook file. 
 * Answer -> Just like other hooks, our custom hooks can return stuff as well. 
 */

const useHttp = () => {
    const [httpState, dispatchHttp] = useReducer(httpReducer, initialState);
    const clear = useCallback(() => dispatchHttp({ type: 'CLEAR' }), []);
    const sendRequest = useCallback(
        (url, method, body, reqExtra, reqIdentifer) => {
            dispatchHttp({ type: 'SEND', identifier: reqIdentifer });
            fetch(url, {
                method: method,
                body: body,
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    return response.json();
                })
                .then(responseData => {
                    dispatchHttp({
                        type: 'RESPONSE',
                        responseData: responseData,
                        extra: reqExtra
                    });
                })
                .catch(error => {
                    dispatchHttp({
                        type: 'ERROR',
                        errorMessage: 'Something went wrong!'
                    });
                });
        },
        []
    );

    return {
        ...httpState,
        sendRequest: sendRequest,
        reqExtra: httpState.extra,
        identifier: httpState.identifier,
        clear: clear
    }
}

export default useHttp
import * as actionTypes from './actionTypes'

export const authStart = () => {
    return {
        type: actionTypes.AUTH_START
    }
}

export const authSuccess = (token, userId) => {
    return {
        type: actionTypes.AUTH_SUCCESS, 
        idToken: token, 
        userId: userId
    }
}

export const authFail = (error) => {
    return {
        type: actionTypes.AUTH_FAIL, 
        error: error
    }
}

/**  
 * LocalStorage is something you can use to save these authentication tokens, user preferences, etc to 
 * persist them even if the application reloads. 
 */
export const auth = (email, password, isSignUp) => {
    return {
        type: actionTypes.AUTH_USER, 
        email: email, 
        password: password, 
        isSignUp: isSignUp 
    }
}

export const checkAuthTimeout = (expirationTime) => {
    return {
        type: actionTypes.AUTH_CHECK_TIMEOUT, 
        expirationTime: expirationTime
    }
}

export const logout = () => {
    return {
        type: actionTypes.AUTH_INITIATE_LOGOUT
    }
}

export const logoutSucceed = () => {
    return {
        type: actionTypes.AUTH_LOGOUT
    }
}

export const setAuthRedirectPath = (path) => {
    return {
        type: actionTypes.SET_AUTH_REDIRECT, 
        path: path 
    }
}

/**
 * While dispatching the authSuccess creator here, you need userId as well as token. You can, of course, 
 * save the user ID in localStorage as well. However, you can also send a request to the firebase 
 * auth API to fetch it from the server and use it here. 
 */
export const authCheckState = () => {
    return {
        type: actionTypes.AUTH_CHECK_STATE
    }
}

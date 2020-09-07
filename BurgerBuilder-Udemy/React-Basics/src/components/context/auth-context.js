import React from 'react'

/**
 * Context is useful when you don't want to chain a certain prop across multiple levels of 
 * components just to get it to a certain place. For example, the authenticated prop passed in
 * the App.js file. You can decide where the context is available (it can also be available globally).
 * You can pass in whatever data type you want in the context, doesn't just have to be an object.
 * Just import this file and wrap whatever component needs this context in this authContext.
 * You should still provide whatever context you need from a top-level state by 
 * --------------------------------------------------------------------------------------------------
 * <ContextComp.Provider value={{key: val, funcHandler: handler}} />
 * To consume the context, import the ContextComp, and wrap whichever element that needs it with 
 * <ContextComp.Consumer {(context) => some JSX}/>, where the consumer returns an anonymous function
 * with the context obj, which can access the dictionary defined here. The handler can point to 
 * the handler created in the top-level file, as it is passed in the 'value' prop as well.
 * --------------------------------------------------------------------------------------------------
 * Alterative way of using context is useful as this way only gives you access where you use JSX. 
 * React 16.6 gives us a static contextType, and you can set that equal to your ContextComp, after 
 * which you can simply access the context by this.context.
 * In functional components, you can use the useContext hook.
 */

const authContext = React.createContext({
    authenticated: false, 
    login: () => {}
})

export default authContext


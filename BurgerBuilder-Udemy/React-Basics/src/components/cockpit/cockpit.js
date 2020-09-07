import React, { useEffect, useRef, useContext } from 'react'
import AuthContext from '../context/auth-context'

/**
 * The useEffect hook: combines the functionality of class-based lifecycle hooks in one react hook. 
 * The useEffect runs for every render cycle. It takes a function and a dependency. What if you 
 * want to control the useEffect and when it renders? Use the dependency array (the second argument)
 * to do that. It points to what is actually used in your effect. If you want the effect to take place
 * only the first time, make it point to an empty array.
 * How to prevent unnecessary renders in functional components? Ans -> react memos 
*/

const Cockpit = (props) => {
    const toggleButtonRef = useRef(null)    // You could pass initial value here too 
    const authContext = useContext(AuthContext)
    console.log(authContext.authenticated)
    useEffect(() => {
        toggleButtonRef.current.click()

        console.log("Cockpit.js useEffect")
        // OK to do http requests here 
        
        return () => {
            console.log("Cockpit unmounted")
        }
    }, [])

    const style = {
        backgroundColor: 'green',
        color: 'white', 
        font: 'inherit', 
        border: '1px solid blue', 
        padding: '8px',
        cursor: 'pointer', 
    }
  
    const classes = []
    if(props.personsLength <= 2) {
      classes.push('red')
    } 
    if(props.personsLength <=1) {
      classes.push('bold')
    }

    if(props.showPeople) {
        style.backgroundColor = 'red'
    }

    /**
    * Can refs be created in functional components? Yes, if you use the useRef hook. You should call 
    * refs in a useEffect, since the latter hook only runs after render cycles. 
    */
    return (
        <div>
            <p className={classes.join(" ")}>This is really working!</p>
            <button ref={toggleButtonRef} className="button" onClick={props.onToggle}>Switch Names</button>
            <button onClick={authContext.login}>Log In</button>
        </div>
    )
}

export default React.memo(Cockpit)
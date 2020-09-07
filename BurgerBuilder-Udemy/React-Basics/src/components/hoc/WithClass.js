import React from 'react'

/** 
 * An H.O.C with class element, which expects a props called classes. Remember, there is nothing wrong 
 * with using divs to wrap around content. But this kind of a structure becomes useful when you 
 * want custom components wrapping around the logic where you perform HTTP requests or something else
 * so you can do error handling etc. You could also have a function that returns a functional component.
 * You can also pass dynamic, unknown props if you want. You can do {...props}, which spreads the props.
 */

const WithClass = (props) => {
    return (
        <div className={props.classes}>{props.children}</div>
    )
}

export default WithClass
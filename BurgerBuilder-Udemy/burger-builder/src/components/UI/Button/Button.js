import React from 'react'
import classes from './Button.module.css'

/**
 * Creating a custom button component with styles. It is especially a clever trick to do because of 
 * how the classnames attribute has been set up i.e. it always takes the Button class, but it conditionally
 * takes in the other classes (success or danger), which we can specify through a prop, thus making it 
 * extremely flexible. 
 */

const button = (props) => {
    return (
        <button 
            className={[classes.Button, classes[props.buttonType]].join(' ')}
            onClick={props.clicked}
            disabled={props.disable}>
            {props.children}
        </button>
    )
}

export default button 
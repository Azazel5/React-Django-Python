import React from 'react'
import classes from './BuildControls.module.css'
import BuildControl from './BuildControl/BuildControl'

const controls = [
    {label: 'Salad', type: 'salad'},
    {label: 'Bacon', type: 'bacon'},
    {label: 'Cheese', type: 'cheese'},
    {label: 'Meat', type: 'meat'}
]

/**
 * The reason why we don't pass the onAdd prop onward further to the BuildControl component is because it 
 * isn't needed. You can simply call it from here and pass the control.type. 
 * Index into the props.disabled array right here, so the individual build control only receives a 
 * boolean t/f value, making it easy to check for that and disable the button in BuildControl. This is a 
 * clever way of doing things: only pass whatever is needed to components. No need to pass the entirety 
 * of props of all components following a prop chain.
 */

const buildControls = (props) => {
    return <div className={classes.BuildControls}>
        <p>Current price: <strong>{props.price.toFixed(2)}</strong></p>
        {controls.map(control => {
            return <BuildControl 
                onAdd={() => props.onAdd(control.type)}
                onRemove={() => props.onRemove(control.type)}
                key={control.label} 
                label={control.label} 
                disabled={props.disabled[control.type]}/>
        })}
        <button 
            onClick={props.purchaseHandler}
            disabled={!props.purchasable}
            className={classes.OrderButton}>{props.isAuthenticated ? 'ORDER NOW': 'Sign Up to order'}</button>
    </div>
}

export default buildControls
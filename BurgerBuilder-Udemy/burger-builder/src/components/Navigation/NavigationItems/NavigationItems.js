import React from 'react'
import classes from './NavigationItems.module.css'
import NavigationItem from './NavigationItem/NavigationItem'

// Boolean props can simply be set by calling the prop, no need for the {prop_name}={true/false}
const navigationItems = (props) => {
    return (
        <ul className={classes.NavigationItems}>
            <NavigationItem link="/" >Burger Builder</NavigationItem>
            {props.isAuthenticated ? <NavigationItem link="/orders">Orders</NavigationItem>: null}
            {props.isAuthenticated ? 
                <NavigationItem link="/logout">Logout</NavigationItem> :
                <NavigationItem link="/auth">Authenticate</NavigationItem> 
            }
        </ul>
    )
}

export default navigationItems
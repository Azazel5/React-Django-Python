import React from 'react'
import burgerLogo from '../../assets/images/burger.png'
import classes from './Logo.module.css'

/**
 * Webpack compiles your project structure and creates its own directories during production, so 
 * it isn't a good idea to set the image src by directly passing it. Instead, import the image 
 * using the path like you did with the CSS files and set it directly in the img tag.
 * This example also uses setting the height of this component through a prop, which makes it 
 * reusable. Thus, this is sometimes more useful than custom media queries in the Logo.module.css file.
 */

const logo = (props) => {
    return (
        <div className={classes.Logo} style={{height: props.height}}>
            <img src={burgerLogo} alt="My Burger"/>
        </div>
    )
}

export default logo
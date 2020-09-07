import React from 'react'
import classes from './PizzaImage.module.css'
import PizzaImage from '../../assets/pizza.png'

const pizzaImage = (props) => {
    return <div className={classes.PizzaImage}>
        <img className={classes.PizzaImg} src={PizzaImage}/>
    </div>
}

export default pizzaImage 
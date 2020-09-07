import React from 'react'
import classes from './Burger.module.css'
import BurgerIngredients from './BurgerIngredients/BurgerIngredients'

/**
 * The object prop is a dictionary, so we get the keys as an array, and start mapping over each
 * value. We return another array with the value and map over it to return the BurgerIngredients. 
 * The reduce function tales a callback (with the previous and current array) and an intial value.
 * -----------------------------------------------------------------------------------------------
 * Remember, wrapping this component with the withRouter H.O.C can give you access to the match
 * objects in this file.
 */
const burger = (props) => {
    let transformedIngredients = Object.keys(props.ingredients)
        .map(ingredient => {
            return [...Array(props.ingredients[ingredient])].map((_, i) => {
                return <BurgerIngredients key={ingredient + i} type={ingredient} />
            })
        })
        .reduce((arr, el) => {
            return arr.concat(el)
        }, [])

    if (transformedIngredients.length === 0) {
        transformedIngredients = <p>Please start adding ingredients</p>
    }

    return (
        <div className={classes.Burger}>
            <BurgerIngredients type="bread-top" />
            {transformedIngredients}
            <BurgerIngredients type="bread-bottom" />
        </div>
    )
}

export default burger
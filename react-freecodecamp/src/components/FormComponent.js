import React from 'react'

/**
 * Several things to note:
 * 1. Form components always have names. Make sure your name matches the state object's attributes.
 * 2. Radio buttons don't check for boolean-ness. Its checked property relates to its value. 
 * 3. While using select, give it a dummy option with an empty name and a --select-- sorta text.
 */
export function FormComponent(props) {
    return (
        <div>
            <form>
                <input type="text" name="firstName" placeholder="First Name"
                onChange={props.onChange} value={props.firstName}></input><br />
                <input type="text" name="lastName" placeholder="Last Name"
                onChange={props.onChange} value={props.lastName}></input><br />
                <input type="number" name="age" placeholder="Eg. 18"
                onChange={props.onChange} value={props.age}></input><br />

                <label>Select your gender</label><br />
                <label><input type="radio" name="gender" value="male"
                checked={props.gender === "male"} onChange={props.onChange}></input>Male</label><br />
                <label><input type="radio" name="gender" value="female"
                checked={props.gender === "female"} onChange={props.onChange}></input>Female</label><br />

                <label>Select where you're flying</label><br />
                <select name="fly" value={props.fly} onChange={props.onChange}>
                    <option value="">--Select an option--</option>
                    <option value="michigan">Michigan</option>
                    <option value="san diego">San Diego</option>
                    <option value="glasgow">Glasgow</option>
                </select><br />

                <label>Dietary Restrictions?</label><br />
                <label><input name="option1" type="checkbox" checked={props.option1} onChange={props.onChange}></input>Meat</label>
                <label><input name="option2" type="checkbox" checked={props.option2} onChange={props.onChange}></input>Veggies</label>
                <label><input name="option3" type="checkbox" checked={props.option3} onChange={props.onChange}></input>Vegan</label>
                
            </form>
            <hr />

            <h1>Entered information:</h1>
            {props.firstName && <p>Your first name is {props.firstName}</p>}
            {props.lastName && <p>Your last name is {props.lastName}</p>}
            {props.age && <p>Your age is {props.age}</p>}
            {props.gender && <p>Your gender is {props.gender}</p>}
            {props.fly && <p>You are flying to {props.fly}</p>}
            {(props.option1 || props.option2 || props.option3) && <p>You cannot eat
            {props.option1 && " meat"} {props.option2 && " veggies"} 
            {props.option3 && " vegan"}</p>}
        </div>
    )
}
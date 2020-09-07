import React from 'react'
import './Person.css'
import PropTypes from 'prop-types'
import WithClass from '../../hoc/WithClass'
import AuthContext from '../../context/auth-context'
// import styled from 'styled-components'

/**
 * If you need media queries, wrap your application in StyleRoot. You don't need it for
 * pseudo-selectors. Another popular library is the StyledComponents library, through which
 * you can create your own components, which are styled.
 */


// const StyleDiv = styled.div`
//     width: 60%;
//     margin: 16px auto;
//     border: 1px solid #eee;
//     box-shadow: 0 2px 3px #ccc;
//     padding: 16px;
//     text-align: center;

//     @media (min-width: 500px){
//         width: 450px;
//     }
// `

/**
 * Return an array with keys can be a workaround for adjacent JSX elements. Otherwise, a wrapper 
 * component like Aux can be created to do that. As of React 16.2, fragments do the same thing. 
 * If you want to make sure your props are of a certain type, you can use proptypes. 
 */

/**
 * Refs are useful if you want a reference to any HTML or JSX element that you want. Create a constructor
 * and set a reference using the React.createRef function. Call it using this.{ref_name}.current.{func}
 */


class Person extends React.Component {
    constructor(props) {
        super(props)
        this.inputRef = React.createRef()
    }

    static contextType = AuthContext

    componentDidMount() {
    }

    /**
     * Sometimes it may be the case that something happens in one component, and you want to 
     * use the ref in another component. Eg. Calling the focusInput function in Persons.js
     * You can create a ref to hold a person element in the Persons.js file and call the 
     * focusInput function using this.{ref}.current.focusInput()
     * You can also use React.forwardRef(props, reference => {return H.O.C(...props, forwardedRef)})
     * Why is only the last element highlighted? It can only hold one ref at a time. 
     */

    focusInput() {
        this.inputRef.current.focus()
    }


    render() {
    console.log("persoN renders()")
    return (
       <WithClass classes="Person"> {/* Same as wrapping it in <React.Fragment> </React.Fragment> */}
            {this.context.authenticated ? <p>Authenticated</p>: <p>Please Log In</p>}
            <p key="i1" onClick={this.props.onClick}>{this.props.text} and I am {this.props.age} years old</p>
            <p key="i2">{this.props.children}</p>
            <input ref={this.inputRef} key="i3" type="text" value={this.props.text} onChange={this.props.onChange}  />
        </WithClass>
    )
    }
}

// Keys are prop names and the values are what type of values. You can get pretty advanced here. 
Person.propTypes = {
    onClick: PropTypes.func, 
    onChange: PropTypes.func, 
    name: PropTypes.string, 
    age: PropTypes.number
}

export default Person


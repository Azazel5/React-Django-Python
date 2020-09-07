import React from 'react'
import Person from './Person/Person'

class persons extends React.Component {
    constructor(props) {
        super(props)
        this.lastPersonRef = React.createRef()
    }
    // static getDerivedStateFromProps(props, state) {
    //     console.log("Persons js get derived state from props")
    //     return state 
    // }

    /** 
     * This is where you compare this.props with nextProps and return a boolean indicating 
     * if the component should be updated and the DOM re-rendered. Right now, the Persons 
     * component will still re-render even if only the cockpit is changed. That's when 
     * shouldComponentUpdate is used. Remember: there's a difference between how react re-renderrs
     * the virtual DOM versus the real DOM.
     * If you want to check if all props have changed while calling shouldComponentUpdate, you 
     * have another option: extending from PureComponent, which is a component which already 
     * implements all props checks. 
    */ 
    
    componentDidMount() {
        this.lastPersonRef.current.focusInput()
    }

    shouldComponentUpdate(nextProps, nextState) {
        return true 
    }

    getSnapshotBeforeUpdate(prevProps, prevState) {
        console.log("Persons getSnapshot")
    }

    render() {
    console.log("persons renders")
    return this.props.persons.map((person, index) => {
    return <Person ref={this.lastPersonRef} key={person.id}
        onChange={(event) => this.props.changed(event, person.id)}
        onClick={() => this.props.clicked(index)} 
        text={person.name} age={person.age}
        />
    })
    }

    componentDidUpdate() {
        console.log("persons componentDidUpdate")
    }

    componentWillUnmount() {
        console.log("persons.js unmounted")
    }
}

export default persons  

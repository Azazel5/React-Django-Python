import React, {useState} from 'react';
import './App.css';
import Person from '../components/Persons/Person/Person'
import styled from 'styled-components'
import Persons from '../components/Persons/Persons'
import Cockpit from '../components/cockpit/cockpit'
import WithClass from '../components/hoc/WithClass'
import AuthContext from '../components/context/auth-context'

/**
 * It is a good idea to have more containers than state-ful components. Passing method handlers from 
 * parent down to children as props is a common pattern as you've seen so far. This is useful if you 
 * want a container/component change the state of another component. If you want to pass an argument 
 * to the passed prop, you could do the arrow function (Beware that using it that way may be inefficient).
 * You cannot write if statements in the {} dynamic syntax. 
 * As your render returns get complicated, consider saving certain parts (especially pertailing to
 * conditionals) in variables and simply rendering them out in the returns. It makes the code cleaner.
 * The slice/splice operators are important as you will often times need to change the array of state.
 * Make sure to not mutate the state (as arrays are reference types) and do a copy of the state object.
 */

/**
 * RECAP for the list handling part 
 * -----------------------------------------------------------------------------------------
 * 1. Create a map function which creates multiple Persons for the persons state.
 * 2. Pass an onChange prop to Person.js, which will be called on the onChange for the input.
 * 3. Create the onChange handler which takes an event (because we want to get the event.value)
 *    and the id because we want to know which Person element was clicked.
 * 4. Calling that onChange on the Person will have to be done via an anonymous function since it 
 *    takes arguments (the event object is acquired via the anonymous function).
 * 5. Get the person index by traversing the array and checking if the passed id is equal to the 
 *    arr element id, if it is, return the id. 
 * 6. Make a copy of the person obj with that id, alter the person obj to the event value, make a 
 *    copy of the persons array, set the person obj to the person index of the persons array, and 
 *    set the state. Whew!
 */

/**
 * How to conditionally style elements when using styled components? You can pass in props to the 
 * component in question. Then check the props in the template literal using the $ syntax. Easy.
 */

const StyledButton = styled.button`
  background-color: ${props => props.altt ? 'red': 'green'};
  color: white; 
  font: inherit; 
  border: 1px solid blue; 
  padding: 8px;
  cursor: pointer; 
  &:hover {
    background-color: ${props => props.altt ? 'salmon': 'lightgreen'};
    color: black;
  }
`

class App extends React.Component {
  state = {
    persons: [
      {id: 1, name: 'Subhanga', age: 20}, 
      {id: 2, name: 'Tom', age: 40}, 
      {id: 3, name: 'Jenn', age: 11}, 
      {id: 4, name: 'Mark', age: 5}
    ], 
    showPeople: false, 
    showCockpit: true, 
    authenticated: false
  }

  static getDerivedStateFromProps(props, state) {
    console.log('Get derived state', props, state)
    return state
  }

  componentDidUpdate() {
    console.log("App.js updated")
  }

  shouldComponentUpdate(nextProp, nextState) {
    console.log("App.js shouldComponentUpdate")
    return true 
  }

  // This will be removed at some point 
  // componentWillMount() {
  //   console.log("Will mount")
  // }

  handleDeletePerson = (index) => {
    const people = [...this.state.persons] // this.state.persons.slice()
    people.splice(index, 1)
    this.setState({persons: people})
  }

  // Find/FindIndex is a javascript function for finding a predicate which returns true for a specific test
  handleNameChange = (event, id) => {
    const personIndex = this.state.persons.findIndex(p => {
      return p.id === id 
    })

    // Make a copy 
    const person = {
      ...this.state.persons[personIndex]
    }
    person.name = event.target.value 
    const persons = [...this.state.persons]
    persons[personIndex] = person
    this.setState({persons: persons})
  }

  handleTogglePerson = () => {
    this.setState(prevState => {
      return {showPeople: !prevState.showPeople}
    })
  }

  loginHandler = () => {
    this.setState({authenticated: true})
  }

  /**
   * What about dynamically changing styles? Eg. you cannot put a :hover selector on inline styles. You 
   * can set the attribute of the the style variable in javascript. Everything is javascript. You can 
   * put conditionals in classNames, create list of classes, etc (as done below). Yes, you could put it in 
   * a global css file with classes/ids to uniquely put styling on them, but knowing a workaround 
   * for inline pseudo-selectors would be pretty cool. Here's where radium comes in. You can do media
   * queries as well. 
   * Sometimes you may want your CSS classes to be scoped to a certain component, which can be achieved 
   * by CSS modules.
   */

  render() {
    console.log("render")
    let people = null 

    if(this.state.showPeople) {
      people = (
          this.state.showCockpit && <Persons persons={this.state.persons} changed={this.handleNameChange}
            clicked={this.handleDeletePerson} isauthenticated={this.state.authenticated}
          />
      )
    }

    return (
      <WithClass classes="App">
        <button onClick={() => this.setState({showCockpit: false})}>Remove cockpit</button>

        <AuthContext.Provider value={
          {authenticated: this.state.authenticated,
          login: this.loginHandler}}>

          {this.state.showCockpit && <Cockpit personsLength={this.state.persons.length}
            showPeople={this.state.showPeople}
            onToggle={this.handleTogglePerson}
            />
          }
          {people}
        </AuthContext.Provider>
      </WithClass>
    )
  }
}

export default App


/**
 * As of react 16.8, you can also use functional components which handle states using hooks. 
 * There are many hooks available (which all begin with the use prefix), but useState is an 
 * important one. It returns an array with two elements (the current state and a setState).
 * In JavaScript, you can have functions inside functions, so just create an event handler, 
 * as usual, and use setCurrState inside it. 
 * HOWEVER, when you use react hooks to manage state, it doesn't automatically merge the new 
 * state with other elements of the old state like the class-based example below does. 
 */
export const FuncApp = () => {
  const [currState, setCurrState] = useState({
    persons: [
      {name: 'Subhanga', age: 20}, 
      {name: 'Tom', age: 40}, 
      {name: 'Jenn', age: 11}, 
      {name: 'Mark', age: 5}
    ], 
  })
  const [,, ] = useState('Haha')
  const handleSwitchNames = () => {
    // to get the 'another' val, you coulld use currState.otherprop, or useState multiple times. 
    setCurrState({persons: [{name: 'Shubmeister', age: 20}]})
  }

  return (
    <div className="App">
      <button onClick={handleSwitchNames}>Switch Names</button>
      <Person text={currState.persons[0].name} age={currState.persons[0].age}>My Hobbies: Racing</Person>
      {currState.persons[1] && <Person text={currState.persons[1].name} age={currState.persons[1].age}/>}
    </div>
  )
}

/**
 * The component lifecycle 
 * -----------------------
 * | Creation |
 * constructor -> getDerivedStateFromProps -> render -> render child components -> 
 * componentDidMount (can cause side-effects here; don't call setState here) -> 
 * | Updating |
 * getDerivedStateFromProps -> shouldComponentUpdate (for performance optimizations) -> 
 * render() -> render child components -> getSnapshotBeforeUpdate -> componentDidUpdate (http requests ok!)
 * Again, don't update state here 
 * Cleanup work needs to be done as well i.e. when the component disappears, remove any dangling event 
 * listeners etc. 
*/

/**
  * How does react update the DOM? Not render(), it just shows a map of what the HTML should look like.
  * React compares virtual DOMs (previous against re-rendered), then it checks if there were any differences.
  * The real DOM is only touched if there are differences (it only renders the parts which were changed).
*/

/**
 * What about rendering adjancent JSX elements ? React does not usually allow it, and you should
 * generally enclose adjacent JSX elements in on parent element. BUT, there are exceptions. In the 
 * Persons.js file, you rendered a list of elements (although a list is one object) because you had 
 * a key item. You can also have other workarounds (check out Person.js)
*/

// this.setState((prevState, props)) => {}



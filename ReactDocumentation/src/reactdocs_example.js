import React, { Suspense } from 'react'
import { render } from 'react-dom'
import { Profiler } from 'react'

/**
 * JSX is powerful, and any valid JavaScript is allowed inside it. It can 
 * be saved as variables in ifs, fors, accepted as arguments, and returned from 
 * functions. 
 */

const details = {
    firstName: "Subhanga",
    lastName: "Upadhyay"
}

export function JSXExample() {
    const anElem = <h3>It is {new Date().toLocaleTimeString()}.</h3>
    return (
        <div>
            <h1>{`Hey ${details.firstName}  ${details.lastName}!`}</h1>
            {anElem}
        </div>
    )
}

/**
 * Props are the way to go to pass down elements from parent to child elements. React elements can 
 * also encapsulate user defined components, just like normal tags.
 * Always simplify long components into a series of other components. Look at the component from its 
 * own point of view. Reuse should always be in the back of your mind. Eg. If there's a comment 
 * component showing an avatar, author name, text, and date, you could create an avatar child 
 * component. 
 */

export function ComponentsExample(props) {
    const comp = <MyComp />
    return (
        <div>
            <h1>Hello {props.name}</h1>
            {comp}
        </div>
    )
}

function MyComp() {
    return <div>Sup?</div>
}

export function StateExample() {
    return (
        <Clock />
    )
}

/**
 * This is a good example which shows how react works and the flow of things. StateExample calls 
 * Clock, which runs the constructor. The current date-time is rendered to the screen and 
 * componentDidMount sets a time, which is connected to the tick function, which updates the 
 * state every second. Every time react detects state being changed, it re-renders the DOM, so the
 * clock runs every second.
 */
class Clock extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            date: new Date()
        }
    }

    tick() {
        this.setState({
            date: new Date()
        })
    }

    componentDidMount() {
        this.timer = setInterval(() => this.tick(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.timer)
    }

    render() {
        return (
            <div>
                <h1>Hello World!</h1>
                <h2>It is {this.state.date.toLocaleTimeString()}.</h2>
            </div>
        )
    }
}

/**
 * State and Props are calculated asynchronously. Beware of using them to calculate the next state.
 * Instead you could do, this.setState((state, props) => {}), where that is the prevState and prop.
 * setState merges the current object into the current state. 
 * this.state = {message: "Hi"}, and then you do this.setState({message: "Hello", name: "Shubs"}), it 
 * replaces the previous message and adds a new name object. 
 * Components may choose to pass down its state as props to child components.
 */

/**
  * If you don't like binding, event handling can be done like - 
  * handleClick = () => {//Whatever}; <button onClick={this.handleClick}> (without parenthesis), which
  * is the method that the documentation recommends. 
  */


function Greeting(props) {
    return (
        <div>
            Welcome!
        </div>
    )
}

function Register(props) {
    return (
        <div>
            Register!
        </div>
    )
}

export class ConditionalExample extends React.Component {
    render() {
        return this.props.isLoggedIn ? <Greeting /> : <Register />
    }
}

/**
 * If you want the element to not render, just return null from the render() function. 
 * You can also render a list of elements using JSX and the map function. Most of the 
 * time you can use the data id as the keys. If you don't have that you can use the 
 * map((element, index) => ...), which isn't recommended. Use some unique indentifier instead. 
 * Keys don't get passed to the comoponent, so if you need em pass them into props.
 */

export class ListExample extends React.Component {
    render() {
        // This code could be embedded within the ul element, as the {} braces allows any 
        // embedded JavaScript. If it results in clearer code, go for it. 
        const mapped = this.props.numbers.map(element => {
            return <li key={element.toString()}>{element}</li>
        })
        return <ul>{mapped}</ul>
    }
}
/**
 * Controlled forms: set values from the form component's state/setState using the element's name and 
 * event handler. If you are handling multiple inputs, give a name to all of them and handle them using 
 * one handler. Check the name and set the state, eg:
 * const target = event.target; const value = target.name === {} ? {}: {}; const name = 
 * target.name; this.setState({[name]: value})
 */

export class FormExample extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            value: ''
        }
    }

    inpChange = (event) => {
        this.setState({
            value: event.target.value
        })
    }

    submit = (event) => {
        event.preventDefault()
    }

    render() {
        return (
            <form onSubmit={this.submit}>
                <label>
                    Name:
                    <input type="text" onChange={this.inpChange}></input>
                </label>
                <button type="submit">Submit</button>
            </form>
        )
    }
}

function BoilingVerdict(props) {
    return (
        <p>
            {props.celcius >= 100 ? 'The water should boil' : 'The water should not boil'}
        </p>
    )
}

const scaleNames = {
    c: 'celcius',
    f: 'fahrenheit'
}

function toCelsius(fahrenheit) {
    return (fahrenheit - 32) * 5 / 9;
}

function toFahrenheit(celsius) {
    return (celsius * 9 / 5) + 32;
}

export class TemperatureInput extends React.Component {
    constructor(props) {
        super(props)
        this.state = { temperature: '' }
    }

    tempChange = (event) => {
        this.props.onTemperatureChange(event.target.value)
    }

    render() {
        const temperature = this.props.temperature
        const scale = this.props.scale;
        return (
            <fieldset>
                <legend>Enter temperature in {scaleNames[scale]}: </legend>
                <input value={temperature} onChange={this.tempChange} />
            </fieldset>
        )
    }
}

/**
 * This is the waterfall example. Here, we want this component (which is the most top-level)
 * component handling the state. C and F are kept in sync as a result. When you do this, you 
 * can pass the event handlers as props so information can flow in between components to make 
 * things work. Follow this pattern: use state when a component needs it. If you find other 
 * components requiring it, lift the state up to their nearest common ancestor and pass it down 
 * as props. 
 * If something can be derived from the props or state, it shouldn't live in the props or state.
 */
export class SharedStateExample extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            temperature: '',
            scale: 'c'
        }
    }

    handleCelciusChange = (temperature) => {
        this.setState({ temperature: temperature, scale: 'c' })
    }

    handleFahrenheitChange = (temperature) => {
        this.setState({ temperature: temperature, scale: 'f' })
    }

    render() {
        const scale = this.state.scale
        const temp = this.state.temperature
        const celcius = temp !== '' && scale === 'f' ? toCelsius(temp) : temp
        const fahrenheit = temp !== '' && scale === 'c' ? toFahrenheit(temp) : temp

        return (
            <div>
                <TemperatureInput temperature={celcius} onTemperatureChange={this.handleCelciusChange} scale="c" />
                <TemperatureInput temperature={fahrenheit} onTemperatureChange={this.handleFahrenheitChange} scale="f" />
                {temp !== '' && <BoilingVerdict celcius={parseFloat(temp)} />}
            </div>
        )
    }
}

/**
 * The docs reccommend using composition instead of inheritance for code reuse. Here's why.
 * Sometimes, some components don't know if they have children components. In that scenario, 
 * props.children can be used (ParentProp). Similarly, you can create your own tags similar to 
 * that too (TagProp).
 */

function ParentProp(props) {
    return (
        <div>
            {props.children}
        </div>
    )
}

function TagProp(props) {
    return (
        <div>
            <div>
                {props.left}
            </div>
            <div>
                {props.right}
            </div>
        </div>
    )
}

export function ChildrenExample() {
    return (
        <div>
            <ParentProp>
                <h1>One child</h1>
                <p>Another child</p>
                <p>Stack em up</p>
            </ParentProp>
            <TagProp
                left={<h1>JSX makes life easy</h1>}
                right={<span>Here's some more for ya</span>}
            />
        </div>
    )
}

// Advanced Guides 

/**
 * You can programatically ensure focus by using the ref operator in React. You can pass the parent's
 * refs to the children using props. This will be looked at in detail later.
 * It's your duty as the developer to think about the edge cases, eg: click option pops out a 
 * window which blocks the other content on the page OR disable the opened popup by clicking in 
 * the background. Make sure functionality used with pointers 
 * can be used through keyboards as well. 
 */

export class CustomTextExample extends React.Component {
    constructor(props) {
        super(props)
        this.textInput = React.createRef() // Initialize a ref
    }

    componentDidMount() {
        this.textInput.current.focus()
    }

    render() {
        return (
            <input type="text" ref={this.textInput} /> // Storing the ref to the input 
        )
    }
}

/**
 * This example utlizes a click outside the element to close element, using refs and window handlers.
 * This example is okay if you're fine with being exclusively based on mouse clicks. If you want 
 * keyboard functionality, use the onBlur and onFocus functionalities. 
 */
export class OuterClickExample extends React.Component {
    constructor(props) {
        super(props)
        this.state = { isOpen: false }
        this.toggleContainer = React.createRef()
    }

    openHandler = () => {
        this.setState(prevState => {
            return { isOpen: !prevState.isOpen }
        })
    }

    // Checking if state is open and if the event click is inside the div or not 
    onClickOutsideHandler = (event) => {
        if (this.state.isOpen && !this.toggleContainer.current.contains(event.target)) {
            this.setState({ isOpen: false })
        }
    }

    componentDidMount() {
        window.addEventListener('click', this.onClickOutsideHandler)
    }

    render() {
        const isOpen = this.state.isOpen
        const buttonStyles = {
            width: '10%',
            margin: '10px',
        }

        return (
            <div ref={this.toggleContainer}>
                <button style={buttonStyles} onClick={this.openHandler}>Click Me</button><br />
                {isOpen && (
                    <ul>
                        <li>Option 1</li>
                        <li>Option 2</li>
                        <li>Option 3</li>
                    </ul>
                )}

                <button style={buttonStyles}>Other Options</button><br />
                <button style={buttonStyles}>More Options</button>
            </div>
        )
    }
}

// Code Splitting 

/**
 * Consider using code splitting as your javascript bundle grows in size. You have, so far, 
 * encountered tools like suspense or React.lazy to do this, but have only scratched the surface.
 * Remember: this is not yet available for server-side rendering, for which the docs recommend
 * some other library. 
 * Code splitting is often done route-based, for which you just wrap the component which 
 * renders the routes with the suspense tag. 
 */

const LazilyLoaded = React.lazy(() => import('./someModule'))
const SomeComponent = () => {
    return (
        <div>
            <Suspense fallback={<div>Loading...</div>}>
                <LazilyLoaded />
            </Suspense>
        </div>
    )
}

// Context API 

/**
 * Only consider saving things which pertain to the overall application in context, such as, 
 * authenticated state, user preferences, themes, etc. You can pass a default value to it 
 * as well. Anything that falls within the provider gets access to the value. You can 
 * define the contextType prop in any consumer to get access to the context.
 * MyClass.contextType = MyContextComponent, after which you can use this.context.
 * In a functional component, you can use the Consumer tag to pass a value inside the 
 * inclosing {} brackets. 
 * To update context values from children, you can pass event handler functions from the 
 * context.
 */

const myContext = {
    authenticated: false,
    authenticateHandler: () => { }
}

// Error boundaries 

/**
 * Use the lifecycle methods getDerivedStateFromError and componentDidCatch with error boundaries. 
 * Return this.props.children in error boundaries, as it returns children. They don't catch 
 * errors in event handlers.
 */

// Ref forwarding 

/**
 * We usually only use this for highly usabale components like FancyButton, which behaves similar 
 * to the DOM buttons. You can forward refs passed to the FancyButton itself like
 * React.forwardRef((props, ref) => {return JSX]})
 * Take care while using HOCs and forward refs, as you might set a reference to the HOC instead
 * of your component. 
 */


const FancyButton = React.forwardRef((props, ref) => {
    return <button ref={ref} className="fancy-button">
        {props.children}
    </button>
})

// Fragments 

/**
 * Solves the problem of having to enclose items in a div. If you have no key to pass to the 
 * fragment, you can define it like <> </>.
 */

// Higher Order Components 

/** 
 * An HOC is a function that takes a component and returns an enhanced component. Take for example
 * you have two different components that have a similar work flow i.e.
 * 1) onMount add an event listener 2) setState whenever data source changes 3) Remove listener
 * We can create an HOC withSubscription that gets the data. Always remember to pass through 
 * additional props using the spread operator!
 * Filter any unnecessary props in the render of the HOC and inject the desired prop.
 * You can simply return the anonymous class i.e. return class extends Component {} or 
 * do as below for easier debugging. 
 * HOCs are wrapped while exporting the component, NOT returned in the render method. 
 * Static methods in the wrapped component doesn't pass through (just like refs).
 */

const commentListWithSubscription = withSubscription(CommentList,
    (Datasource) => Datasource.getComments())

function withSubscription(WrapperComponent, selectData) {
    class WithSubscription extends React.Component {
        state = {
            data: selectData(Datasource, props)
        }

        // Do whatever you did with your OG component

        render() {
            const { extraProps, ...passthruProps } = this.props
            return <WrapperComponent data={this.state.data} {...this.passthruProps} />
        }
    }

    WithSubscription.displayName = `WithSubscription(${getDisplayName(WrappedComponent)})`;
    return WithSubscription
}

function getDisplayName(WrappedComponent) {
    return WrappedComponent.displayName || WrappedComponent.name || 'Component';
}

/**
 * Under the hood, JSX simple calls the React.createElement function and passes a bunch of 
 * arguments to it. Although boolean props can just be called without specifying true or 
 * false, the docs recommend doing so anyways so it isn't confused with the ES6 shorthand 
 * of {foo} (which is {foo:foo}). 
 */

// Optimizing performance 

/**
 * Use the production build, using npm build, which does a number of optimizations such as minimizing 
 * the files etc. 
 * If your application uses thousands of lists, the docs recommend a technique called windowing. 
 * Rendering a small subset of those lists at any given time. You can also implement 
 * shouldComponentUpdate or extends from React.PureComponent.
 */

// Never mutate state directly. This spreads the entire contents of the words array and adds
// 'marklar' to the result. 

export const handleClick = () => {
    this.setState(state => ({
        words: [...state.words, 'marklar'],
    }));
};

// Rewriting mutating object (eg. colormap.right = 'blue') without actual mutation

export const mutateColorMap = (colormap) => {
    return Object.assign({}, colormap, { right: 'blue' }) ||
        { ...colormap, right: 'blue' }
}

// Portals 

/**
 * Typically the render method of react returns the JSX element to the nearest DOM element.
 * If you need the item to render anywhere in screen, you need to use portals. 
 * A typical usecase: when parent has overflow: hidden or a Z-index, and you need the children
 * to visually break out. Use ReactDOM.createPortal(children, element) to do this. 
 */


// Profiler

/**
 * Measures how often some component renders and what the cost of it is. Wrap the profiler 
 * in whatever element you want to profile. 
 */

export class MyComponent extends React.Component {
    render() {
        <Profiler id="my-profiler" onRender={}>
        </Profiler>
    }
}

/**
 * The render() function creates a tree of elements, which updates on the next props/state update. 
 * It re-renders elements differently based on different elements. When the root element have 
 * different types, it tears it down and creates a new element entirely. 
 * Otherwise, react is smart enough to only update the inline things that have changed such as 
 * className(s) and style(s). 
 * React uses the key prop for list items to detect which is a new item versus which is not. 
 */

// Refs and the DOM 

/**
 * Ref receives the mounted instance of the component as current, so you can do things like 
 * focus on them. It assigns the current property only after the component has mounted on the 
 * screen. 
 */

// Another way of creating refs: callback refs 

export class SubhangaClass extends React.Component {
    constructor(props) {
        super(props)
        this.textRef = null
        this.setTextRef = element => {
            this.textRef = element
        }
        this.focusText = () => {
            if(this.textRef) {
                this.textRef.focus()
            }
        }
    }

    componentDidMount() {
        this.focusText()
    }

    render() {
        return (
            <div>
                <input type="text" ref={this.setTextRef}/>
            </div>
        )
    }
}

// Render props: how to share code between components 

/**
 * Just pass in a render prop which takes a function which returns a JSX component. 
 * For example - if you have a component which tracks the mouse position on an app, how
 * would you reuse this?  
 * If you segregate the component such that Mouse is a component which only tracks mouse 
 * position, how would you reuse it? If you want another component's mouse positions, would
 * you simply render it inside mouse? The answer is nien.
 * Instead of hard-coding a specific component, we provide the Mouse component a render 
 * function prop that dynamically determines what to render.
 */

export class Mouse extends Component {
    constructor(props) {
        super(props)
        this.state = {x: 0, y: 0}
    }

    handleMouseMove = (event) => {
        this.setState({
            x: event.clientX, 
            y: event.clientY
        })
    }

    // Instead of passing another component inside the div, we render the props and pass in the 
    // state.
    render() {
        return (
        <div onMouseMove={this.handleMouseMove}>
            {this.props.render(this.state)}
        </div>
        )
    }
}

// Simple component which receives mouse props 
export class Cat extends React.Component {
    render() {
        const mouse = this.props.mouse;
        return (
            <img src="/cat.jpg" style={{ position: 'absolute', left: mouse.x, top: mouse.y }} />
        )
    }
}

export class MouseTracker extends Component {
    constructor(props) {
        super(props)
        this.state = {}
    }

    render() {
        return (
        <div>
            <Mouse render={mouse => {
                <Cat mouse={mouse} />
            }}/>
        </div>
        )
    }
}

// Be careful with render props and PureComponent. 

/**
 * {class_name/func_name}.propTypes = {
 *      name: Proptypes.string
 * }
 * 
 * This makes sure that the class/function receives a name prop which is of type string. 
 * There are all kinds of validations available. You can also specify default props.
 */

/**
 * The only place where an uncontrolled component makes sense is <input type="file" />, as it 
 * can only be controlled by the user. You can get access to it through a ref.
 */
import React, { Component } from 'react';
import {connect} from 'react-redux'
import * as actionTypes from '../../store/actions/index'
import CounterControl from '../../components/CounterControl/CounterControl';
import CounterOutput from '../../components/CounterOutput/CounterOutput';

/**
 * Set up a subscription to the store. Remember, it is still your components which manage the state, 
 * but now, they just don't do it on their own. Connect is a function which returns an HOC, and it 
 * takes two pieces of information: 
 * 1. Which part of the state is interesting to us
 * 2. Which actions do I want to dispatch
 * Create two functions for that, one which accesses the state you have in the reducer, and one 
 * which returns an anonymous function which dispatches the type of action.
 * Then, in the reducer, you check the type, and modify the state (immutably), and call the 
 * anonymous function via this.props.{func_name} or props.{func_name}. You can pass a payload 
 * to the dispatch as well to pass the data to the reducer.
 * Outsource your action types 
 */
class Counter extends Component {
    state = {
        counter: 0
    }

    counterChangedHandler = ( action, value ) => {
        switch ( action ) {
            case 'inc':
                this.setState( ( prevState ) => { return { counter: prevState.counter + 1 } } )
                break;
            case 'dec':
                this.setState( ( prevState ) => { return { counter: prevState.counter - 1 } } )
                break;
            case 'add':
                this.setState( ( prevState ) => { return { counter: prevState.counter + value } } )
                break;
            case 'sub':
                this.setState( ( prevState ) => { return { counter: prevState.counter - value } } )
                break;
            default:
                console.log("Broken")
                break 
        }
    }

    render () {
        return (
            <div>
                <CounterOutput value={this.props.ctr} />
                <CounterControl label="Increment" clicked={this.props.onIncrementCounter} />
                <CounterControl label="Decrement" clicked={this.props.onDecrementCounter}  />
                <CounterControl label="Add 5" clicked={this.props.onAddCounter}  />
                <CounterControl label="Subtract 5" clicked={this.props.onSubtractCounter}  />
                <hr />
                <button onClick={() => this.props.onStoreResult(this.props.ctr)}>Store Result</button>
                <ul>
                    {this.props.storedResults.map(res => {
                        return <li key={res.id} onClick={() => this.props.onDeleteResult(res.id)}>{res.val}</li>
                    })}
                </ul>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        ctr: state.counter.counter,
        storedResults: state.results.results
    }
}

/**
 * Use action creators while dispatching actions to the reducer, which are defined in the actions.js
 * file alongside the actionTypes. They do the mapping of the type/payloads of the actions instead of 
 * doing it inside the dispatch function by creating an object there. It is useful for implementing 
 * asynchronous code. For redux to be able to handle asynchronous code (such as an API call), you need
 * to use a library called redux-thunk.
 */
const mapDispatchToProps = dispatch => {
    return {
        onIncrementCounter: () => dispatch(actionTypes.increment()), 
        onDecrementCounter: () => dispatch(actionTypes.decrement()), 
        onAddCounter: () => dispatch(actionTypes.add(5)), 
        onSubtractCounter: () => dispatch(actionTypes.subtract(5)),

        onStoreResult: (result) => dispatch(actionTypes.storeResult(result)),
        onDeleteResult: (id) => dispatch(actionTypes.deleteResult(id))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Counter);
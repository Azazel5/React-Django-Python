import React from 'react'
import {todos} from '../todos'

/**
 * Inline styles are pretty useful if you want style to conditionally change. Two different kinds 
 * of conditionals used regularly in React: the ternary and the && boolean. 
 * {bool} ? cond1: cond2 follows an if else structure and the {bool1} && {bool2} is typically used 
 * when you have no use for the else, and want something to be displayed when it is true and not 
 * undefined/null etc.
 */
function TodoItem(props) {
    const completeStyle = {'textDecoration': 'line-through'}
    return (
        <div className="todo-item">
            <input type="checkbox" checked={props.elem.completed} onChange={() => props.handleChange(props.elem.id)}/>
            <p style={props.elem.completed ? completeStyle: null}>{props.elem.text}</p>
        </div>
    )
}

export class AppTodoItem extends React.Component {
    constructor() {
        super()
        this.state = {
            todos: todos 
        }
    
        this.handleChange = this.handleChange.bind(this)
    }


    handleChange(id) {
        /**
         * The map function returns a object which is altered via every operation performed
         * on the original object.
         */
        this.setState(prevState => {
            const updatedTodos = prevState.todos.map(obj => {
                if(obj.id === id) {
                    obj.completed = !obj.completed 
                }

                return obj
            })

            return {
                todos: updatedTodos
            }
        })
    }

    render() {
        const Elems = this.state.todos.map(Elem => {
            // Remember to pass in the key prop if working with/rendering multiple elements.
            return <TodoItem elem={Elem} key={Elem.id} handleChange={this.handleChange} />
        })

        return (
            <div className="todo-list">
                {Elems}       
            </div>
        )
    }
}


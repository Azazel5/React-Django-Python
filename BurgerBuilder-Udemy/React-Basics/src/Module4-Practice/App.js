import React, {Component} from 'react'
import {ValidationComponent, CharComponent} from './components'

export class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            text: ''
        }
    }
    onTextLengthChangeHandler = (event) => {
        this.setState(
            {
                text: event.target.value 
            }
        )
    }

    onCharClickHandle = (index) => {
        const text = [...this.state.text]
        text.splice(index, 1)
        const str = text.join("")
        this.setState({text: str})
    }

    render() {
        const text = this.state.text
        const charArr = text.split('').map((char, index) => {
            return <CharComponent onClick={() => this.onCharClickHandle(index)} key={index} letter={char}/>
        })

        return (
            <div>
                <input type="text" onChange={this.onTextLengthChangeHandler} value={this.state.text}/>
                <p>{text}</p>
                <ValidationComponent textLength={text.length} />
                {charArr}
            </div>
        )
    }
}
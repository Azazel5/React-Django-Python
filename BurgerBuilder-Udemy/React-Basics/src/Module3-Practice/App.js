import React, {Component} from 'react'
import {UserInput, UserOutput} from './Components'

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            username: 'boyWhoLived999'
        }
    }

    handleState = (event) => {
        this.setState({
            username: event.target.value
        })
    }

    render() {
        return (
            <div>
                <UserInput currentName={this.state.username} onUsernameChange={this.handleState}/>
                <UserOutput username={this.state.username}/>
            </div>
        )
    }
}

export default App 
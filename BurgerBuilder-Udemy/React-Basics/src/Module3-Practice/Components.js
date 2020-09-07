import React, {Component} from 'react'

export class UserInput extends Component {
    render() {
        const inputStyle = {
            border: '2px solid red'
        }
        return (
            <div>
                <input style={inputStyle} value={this.props.currentName}
                    onChange={this.props.onUsernameChange} type="text"/>
            </div>
        )
    }
}

export class UserOutput extends Component {
    render() {
        return (
            <div>
                <p>{this.props.username}</p>
                <p>Another one</p>
            </div>
        )
    }
}
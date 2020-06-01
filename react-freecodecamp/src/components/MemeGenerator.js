import React from 'react'

/**
 * The meme generator component, which makes the API call and sets the data.
 * -------------------------------------------------------------------------
 * componentDidMount - lifecycle method. It is a good place to make API calls 
 * and set the state. React hooks have eliminated the need for class based 
 * components and make setState easier. 
 * Using arrow functions (eg. onChange = (event) => {}) is good. No more 
 * binding to the constructor. 
 */
export class MemeGenerator extends React.Component {
    constructor() {
        super()
        this.state = {
            topText: "", 
            bottomText: "", 
            allImages: [], 
            randomImageUrl: ""
        }

        this.onChange = this.onChange.bind(this)
        this.handleFormSubmit = this.handleFormSubmit.bind(this)
    }

    componentDidMount() {
        /**
         * Never manipulate state directly. Always use the setState method. You have two ways of 
         * going about things. If you don't care about previous state (like in this example), 
         * simply pass in a new dictionary of state values that you want. If you do care, then 
         * pass in the prevState argument.
         */
        fetch("https://api.imgflip.com/get_memes")
        .then(response => response.json())
        .then(data => {
            this.setState({
                allImages: data.data.memes, 
                randomImageUrl: data.data.memes[Math.floor(Math.random() * data.data.memes.length)].url
            })
        })
    }

    onChange(event) {
        // A good way of using on onChange method to handle multiple form elements. 
        const {name, value} = event.target
        this.setState({
            [name]: value
        })
    }

    handleFormSubmit(event) {
        event.preventDefault()
        this.setState({
            randomImageUrl: 
            this.state.allImages[Math.floor(Math.random() * this.state.allImages.length)].url
        })

    }

    render() {
        // Controlled forms: set value through state, so every alteration to the form is tracked.
        return (
            <div className="memes">
                <form onSubmit={this.handleFormSubmit}>
                    <input name="topText" type="text" value={this.state.topText}
                    onChange={this.onChange} placeholder="Top Text"></input>
                    <input name="bottomText" type="text" value={this.state.bottomText}
                    onChange={this.onChange} placeholder="Bottom Text"></input>
                    <button>Gen</button>
                </form>

                <div className="col">
                    <img src={this.state.randomImageUrl} alt="meme"/>
                    <h2>{this.state.topText}</h2>
                    <h2>{this.state.bottomText}</h2>
                </div>
            </div>
        )
    }
}
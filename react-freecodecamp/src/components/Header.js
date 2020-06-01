import React from 'react'

export class Header extends React.Component {
    render() {
        return (
            <header>
                <div className="row">
                    <div className="col">
                        <img src="http://www.pngall.com/wp-content/uploads/2016/05/Trollface.png" 
                        alt="Problem?"/>
                    </div>
                    
                    <div className="col">
                    <p>Meme Generator</p>
                    </div>
                </div>
            </header>
        )
    }
}
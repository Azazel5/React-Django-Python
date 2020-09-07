import React, { Component } from "react";
import { CSSTransition } from 'react-transition-group';
import "./App.css";
import Modal from "./components/Modal/Modal";
import Backdrop from "./components/Backdrop/Backdrop";
import List from "./components/List/List";

// You can set different animation timings for enter and exit.
const ANIMATION_TIMING = {
  enter: 400, 
  exit: 1000
}

class App extends Component {
  state = {
    modalIsOpen: false,
    showBlock: false
  }

  showModal = () => {
    this.setState({ modalIsOpen: true })
  }

  closeModal = () => {
    this.setState({ modalIsOpen: false })
  }

  /**
   * React transition group is extremely powerful as it has props such as mountOnEnter to 
   * get the animation rolling only when the element appears. The transition component gets
   * 4 props (exited, etc) to control how the animation plays out. 
   */
  render() {
    return (
      <div className="App">
        <h1>React Animations</h1>
        <button className="Button" onClick={() => this.setState(prevState => ({ showBlock: !prevState.showBlock }))}>Toggle</button><br />
        {/* <Transition in={this.state.showBlock} timeout={300}>
          {state => (
            <div style={{
              backgroundColor: 'red', width: '100px', height: '100px',
              margin: 'auto', opacity: state === 'exited' ? 0: 1
            }}>
            </div>
          )}

        </Transition> */}

        {/* The CSSTransition tag automatically adds some extra things to the classNames prop at the 
        end i.e. -enter-active, -exit, -exit-active. You can use your own CSS classes as well instead of 
        following this pattern. 
        */}
        <CSSTransition 
          mountOnEnter unmountOnExit 
          in={this.state.modalIsOpen} timeout={ANIMATION_TIMING}
          onEnter={() => console.log("OnEnter()")}
          onEntering={() => console.log("OnEntering()")}
          onEntered={() => console.log("OnEntered()")}
          onExit={() => console.log("OnExit()")}
          onExiting={() => console.log("OnExiting()")}
          onExited={() => console.log("OnExited()")}
          classNames="fate-slide">
            <Modal closed={this.closeModal} /> 
        </CSSTransition>

        {this.state.modalIsOpen && <Backdrop show={this.state.modalIsOpen} />}
        <button className="Button" onClick={this.showModal}>Open Modal</button>
        <h3>Animating Lists</h3>
        <List />
      </div>
    );
  }
}

export default App;

import React from 'react';


function Square(props) {
    return (
      <button onClick={() => props.onClick()}
      className="square">
        {props.value}
      </button>
    );
  }


class Board extends React.Component {
  renderSquare(i) {
    return (
      <Square onClick={() => this.props.onClick(i)} value={this.props.squares[i]}/>
    )
  }

  render() {
    let matrix = []
    for(let i = 0; i < 3; ++i) {
      let row = []
      for(let j = 0; j < 3; ++j) {
        row.push(this.renderSquare(i*3 + j))
      }
      matrix.push(<div key={i} className="board-row">{row}</div>)
    }
    return (
      <div>
          {matrix}
      </div>
    );
  }
}

export class Game extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      history: [{
        squares: Array(9).fill(null)
      }], 
      stepNumber: 0,
      xIsNext: true, 
    }
  }

  handleClick(i) {
    /**
     * Immutability is an important concept in React. It has several benefits, so 
     * never specifically change state directly. Make copies, or use prevState.
     */
    const history = this.state.history.slice(0, this.state.stepNumber + 1)
    const current = history[history.length - 1]
    const squares = current.squares.slice()
    if (calculateWinner(squares) || squares[i]) {
      return 
    }
    squares[i] = this.state.xIsNext ? "X": "O"
    this.setState(prevState => {
      return {
        history: history.concat([{
          squares: squares, 
          latestMove: i 
        }]),

        stepNumber: history.length, 
        xIsNext: !prevState.xIsNext
      }
    })
  }

  jumpTo(step) {
    this.setState({
      stepNumber: step, 
      xIsNext: (step % 2) === 0
    })
  }

  render() {
    const history = this.state.history
    const current = history[this.state.stepNumber]
    const winner = calculateWinner(current.squares)

    const moves = history.map((step, move) => {
      const row = Math.floor(step.latestMove / 3) + 1
      const col = (step.latestMove % 3) + 1
      const desc = move ? `Go to move #${move} and pos (row, col): (${row}, ${col})`: 'Go to game start' 

      return (
        <li key={move}>
          <button className={move === this.state.stepNumber ? 'bold-item': null}
          onClick={() => this.jumpTo(move)}>{desc}</button>
        </li>
      )
    })

    let status 
    if(winner) {
      status = 'Winner: ' + winner
    } else {
      status = 'Next player: ' + (this.state.xIsNext ? "X": "O")
    }

    return (
      <div className="game">
        <div className="game-board">
          <Board squares={current.squares} onClick={(i) => this.handleClick(i)} />
        </div>
        <div className="game-info">
          <div>{status}</div>
          <ol>{moves}</ol>
        </div>
      </div>
    );
  }
}

// ========================================

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2], 
    [3, 4, 5], 
    [6, 7, 8], 
    [0, 3, 6], 
    [1, 4, 7], 
    [2, 5, 8], 
    [0, 4, 8], 
    [2, 4, 6]
  ]

  for(let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i]
    if(squares[a] && squares[a] === squares[b] && squares[b] === squares[c]) {
      return squares[a]
    }
  }
  return null 
}

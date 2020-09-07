import React, {useState} from 'react';
import LoadingIndicator from '../UI/LoadingIndicator'

import Card from '../UI/Card';
import './IngredientForm.css';

/**
 * The useState hook works differently from this.state, as it doesn't merge but replaces whatever 
 * state you have. Pass an anonymous function into the set function and get access to the 
 * prevState, just like in this.setState. While using two nested closures, be careful of the 
 * scope of variables - it might create some unknown errors, especially in events. 
 * You should split your state into multiple states. Only use objects or arrays as state if 
 * you have data which changes together. React hooks can only be used in other hooks or JSX 
 * functions. You cannot do it inside if statements either. Use them at the root level of functions.
 */
const IngredientForm = React.memo(props => {
  const [title, setTitle] = useState('')
  const [amount, setAmount] = useState('')

  const submitHandler = event => {
    event.preventDefault();
    props.onAddIngredient({title: title, amount: amount})
  };

  return (
    <section className="ingredient-form">
      <Card>
        <form onSubmit={submitHandler}>
          <div className="form-control">
            <label htmlFor="title">Name</label>
            <input type="text" id="title" value={title} onChange={event => {
                setTitle(event.target.value )
            }}/>
          </div>
          <div className="form-control">
            <label htmlFor="amount">Amount</label>
            <input type="number" id="amount" value={amount.amount} onChange={event => {
              setAmount(event.target.value)
            }}/>
          </div>
          <div className="ingredient-form__actions">
            <button type="submit">Add Ingredient</button>
            {props.isLoading && <LoadingIndicator />}
          </div>
        </form>
      </Card>
    </section>
  );
});

export default IngredientForm;

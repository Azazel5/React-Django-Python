import React from 'react';

import './IngredientList.css';

/**
 * Using React.memo and callbacks is a great way to reduce the number of renders in your 
 * components. useCallback is used if the function doesn't need to change after re-renders.
 * An alternative to React.memo would be to use the useMemo hook.
 * Typically, React.memo is used to wrap around components, but the useMemo hook can be 
 * used to wrap around any data that doesn't change from time to time. 
 */
const IngredientList = React.memo(props => {
  return (
    <section className="ingredient-list">
      <h2>Loaded Ingredients</h2>
      <ul>
        {props.ingredients.map(ig => (
          <li key={ig.id} onClick={() => props.onRemoveItem(ig.id)}>
            <span>{ig.title}</span>
            <span>{ig.amount}x</span>
          </li>
        ))}
      </ul>
    </section>
  );
})

export default IngredientList;

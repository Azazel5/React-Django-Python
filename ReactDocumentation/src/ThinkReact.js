import React from 'react'

/**
 * Lesson 12 of the react documentation step-by-step tutorial. Shows why analyzing/designing
 * components. Think of the website you want to make as a series of components, which is the 
 * "React" way of designing things. Also follows a waterfall architectural style where props 
 * flows down from the parent component to the children, as needed. (Example in ProductCategoryRow, 
 * only the category is passed, whereas in ProductRow, the product object is passed).
 * 
 * Here are some questions to help you determine if you should use an item as props of state:
    1. Is it passed in from a parent via props? If so, it probably isn’t state.
    2. Does it remain unchanged over time? If so, it probably isn’t state.
    3. Can you compute it based on any other state or props in your component? If so, it isn’t state.
 */

 /**
  * For this, we can see that the only state we want is the input textbox and the checkboxes.
  * On deciding where to hold the state for the application, we can see that ProductTable and 
  * Searchbar components need to be updated. So the state goes to the nearest common ancestor, which 
  * is the FilterableProductTable.
  * Props flows from the top-level to the bottom-level, but sometimes, state will need to follow
  * an inverse flow. Deeply nested form elements will have to update the state of a component somehow.
  * As the state of a component should only be handled by itself, event handlers are passed as props
  * to the children components, and the setState is called in the OG component.
  */

class Searchbar extends React.Component {
    render() {
        const searchText = this.props.searchText
        const isStockOnly = this.props.isStockOnly
        return (
            <form>
                <input type="text" placeholder="Search..." value={searchText} 
                onChange={(event) => this.props.onTextChange(event.target.value)}/>
                <p>
                    <input type="checkbox" checked={isStockOnly}
                    onChange={(event) => this.props.onInStockChange(event.target.checked)} /> Only show products in stock
                </p>
            </form>
        )
    }
}

class ProductCategoryRow extends React.Component {
    render() {
        const category = this.props.category 
        return (
            <tr>
                <th colSpan="2">{category}</th>
            </tr>
        )
    }
}

class ProductRow extends React.Component {
    render() {
        const product = this.props.product 
        const stockOrNot = product.stocked ? null: {'color': 'red'}
        return (
            <tr>
                <td style={stockOrNot}>{product.name}</td>
                <td>{product.price}</td>
            </tr>
        )
    }
}

class ProductTable extends React.Component {
    render() {
        let lastCategory = null 
        const rows = []
        const searchText = this.props.searchText
        const isStockOnly = this.props.isStockOnly
        this.props.products.forEach(element => {
            if(element.name.indexOf(searchText) === -1) {
                return 
            }

            if(isStockOnly && !element.stocked) {
                return 
            }

            if(element.category !== lastCategory) {
                rows.push(
                    <ProductCategoryRow key={element.category} category={element.category}/>
                )
            }

            rows.push(
                <ProductRow product={element} key={element.name}/>
            )
            lastCategory = element.category;
        })

        return (
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Price</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        )
    }
}

export class FilterableProductTable extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            searchText: '', 
            isStockOnly: false 
        }
    }

    handleTextChange = (searchText) => {
        this.setState({searchText: searchText})
    }

    handleInStockChange = (isStockOnly) => {
        this.setState({isStockOnly: isStockOnly})
    }

    render() {
        return (
            <div>
                <Searchbar isStockOnly={this.state.isStockOnly} searchText={this.state.searchText}
                onTextChange={this.handleTextChange} onInStockChange={this.handleInStockChange}/>

                <ProductTable searchText={this.state.searchText} isStockOnly={this.state.isStockOnly}
                products={this.props.products}/>
            </div>
        )
    }
}

export const PRODUCTS = [
    {category: 'Sporting Goods', price: '$49.99', stocked: true, name: 'Football'},
    {category: 'Sporting Goods', price: '$9.99', stocked: true, name: 'Baseball'},
    {category: 'Sporting Goods', price: '$29.99', stocked: false, name: 'Basketball'},
    {category: 'Electronics', price: '$99.99', stocked: true, name: 'iPod Touch'},
    {category: 'Electronics', price: '$399.99', stocked: false, name: 'iPhone 5'},
    {category: 'Electronics', price: '$199.99', stocked: true, name: 'Nexus 7'}
  ];


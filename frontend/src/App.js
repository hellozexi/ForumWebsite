import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import Blog from './containers/Blog/Blog';

class App extends Component {
  render () {
    return (
      // <BrowserRouter basename="/my-app">
      <BrowserRouter>
        <div className="App">
          <Blog isAuthenticated={this.props.isAuthenticated} />
        </div>
      </BrowserRouter>
    );
  }
}
const mapStateToProps = state => {
  return {
      isAuthenticated : state.token !== null
  }
}

export default connect(mapStateToProps)(App);

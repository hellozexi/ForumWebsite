import React, { Component } from 'react';
// import axios from 'axios';
import { Route, NavLink, Switch, Redirect } from 'react-router-dom';

import classes from './Blog.css';
import Posts from './Posts/Posts';
import Sections from './Sections/Sections'
import asyncComponent from '../../hoc/asyncComponent';
import Auth from '../../containers/Auth/Auth'
import Logout from '../../containers/Auth/Logout/Logout'
// import NewPost from './NewPost/NewPost';
import { connect } from 'react-redux';
import FullPost from './FullPost/FullPost';
const AsyncNewPost = asyncComponent(() => {
    return import('./NewPost/NewPost');
});

class Blog extends Component {
    render () {
        return (
            <div className={classes.Blog}>
                <header>
                    <nav>
                        <ul>
                            <li><NavLink
                                to="/"
                                exact
                                activeClassName="my-active"
                                activeStyle={{
                                    color: '#fa923f',
                                    textDecoration: 'underline'
                                }}>Home</NavLink></li>
                            <li><NavLink to={{
                                pathname: '/new-post',
                                hash: '#submit',
                                search: '?quick-submit=true'
                            }}>New Post</NavLink></li>
                            <li> 
                                {
                                    this.props.isAuthenticated ? <NavLink to="/logout">Log out</NavLink> : <NavLink to="/auth">Sign up/Sign in</NavLink>
                                }
                            </li>
                        </ul>
                    </nav>
                </header>
                {/* <Route path="/" exact render={() => <h1>Home</h1>} />
                <Route path="/" render={() => <h1>Home 2</h1>} /> */}
                <Switch>
                    <Route path="/new-post" component={AsyncNewPost} /> 
                    <Route path="/auth" component={Auth} />
                    <Route path="/logout" component={Logout} />
                    <Route path="/posts/:id" exact component={FullPost} />
                    <Route path={'/:id'} exact component={Posts} />
                    <Route path="/" component={Sections} />
                    <Route render={() => <h1>Not found</h1>}/>
                    
                    {/* <Redirect from="/" to="/posts" /> */}
                    {/* <Route path="/" component={Posts} /> */}
                </Switch>
            </div>
        );
    }
}
export default Blog;
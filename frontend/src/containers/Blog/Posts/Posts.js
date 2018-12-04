import React, { Component } from 'react';
import axios from '../../../axios';
import { Route } from 'react-router-dom';

import Post from '../../../components/Post/Post';
import classes from './Posts.css';
import FullPost from '../FullPost/FullPost';

class Posts extends Component {
    state = {
        posts: []
    }
    componentDidMount () {

        this.loadData();
    }
    loadData () {
        console.log(this.props);
        if ( this.props.match.params.id ) {
            axios.get( '/api/posts?section_name=' + this.props.match.params.id )
            .then( response => {
                 console.log(response);
                 this.setState({posts : response.data})
            } );
        }
    }
    postSelectedHandler = ( id ) => {
        // this.props.history.push({pathname: '/posts/' + id});
        console.log("path:::" + '/' + this.props.match.params.id + '/' + id)
        this.props.history.push( '/posts/'  + id );
    }

    render () {
        let posts = <p style={{ textAlign: 'center' }}>Something went wrong!</p>;
        if ( !this.state.error ) {
            posts = this.state.posts.map( post => {
                return (
                    // <Link to={'/posts/' + post.id} key={post.id}>
                    <Post
                        key={post.post_id}
                        title={post.post_name}
                        author={post.poster_email}
                        clicked={() => this.postSelectedHandler( post.post_id )} />
                    // </Link>
                );
            } );
        }

        return (
            <div>
                <section className={classes.Posts}>
                    {posts}
                </section>
                <Route path="/posts/:id" exact component={FullPost} />
            </div>
            
        );
    }
}

export default Posts;
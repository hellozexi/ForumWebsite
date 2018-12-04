import React, { Component } from 'react';
import axios from 'axios';

import classes from'./FullPost.css';

class FullPost extends Component {
    state = {
        loadedPost: null
    }

    componentDidMount () {
        this.loadData();
    }

    loadData () {
        console.log(this.props)
        if ( this.props.match.params.id ) {
            axios.get( '/api/post/' + this.props.match.params.id )
                .then( response => {
                    console.log(response);
                    this.setState( { loadedPost: response.data } );
                } );
        }
    }

    render () {
        let post = <p style={{ textAlign: 'center' }}>Please select a Post!</p>;
        if ( this.props.match.params.id ) {
            post = <p style={{ textAlign: 'center' }}>Loading...!</p>;
        }
        if ( this.state.loadedPost ) {
            post = (
                <div className={classes.FullPost}>
                    <h1>{this.state.loadedPost.post_name}</h1>
                    <p>{this.state.loadedPost.context}</p>
                    <div className={classes.Edit}>
                        <button onClick={this.deletePostHandler} className={classes.delete}>Comment</button>
                    </div>
                    <div>
                        <p>{this.state.loadedPost.post_time}</p>
                        <p>{this.state.loadedPost.poster_email}</p>
                    </div>
                </div>
            );
        }
        return post;
    }
}

export default FullPost;
import React, { Component } from 'react';
import axios from '../../../axios';
import { Route } from 'react-router-dom';
import Post from '../../../components/Post/Post';
import Comment from '../../../components/Comment/Comment'
import classes from './OtherProfile.css';
import FullPost from '../FullPost/FullPost';

class OtherProfile extends Component {
    state = {
        posts: [],
        comments: []
    }
    componentDidMount () {

        this.loadData();
    }
    loadData () {
        console.log(this.props)
        if ( this.props.match.params.id ) {
            
            //response = client.get(f'/api/posts?{urlencode(   }')
            axios.get( '/api/posts?' + encodeURI("user_email="+encodeURI(this.props.match.params.id)) )
            .then( response => {
                 console.log(response);
                 this.setState({posts : response.data})
            } )
            .catch(err => {
                alert(err.response.data.message)
            })
        }
        if ( this.props.match.params.id ) {
            //response = client.get(f'/api/comments?{urlencode({"user_email": "xua@wustl.edu"})}')
            axios.get( '/api/comments?' + encodeURI("user_email="+encodeURI(this.props.match.params.id)))
                .then( response => {
                    console.log(response);
                    this.setState( { comments: response.data } );
                } )
                .catch(err => {
                    alert(err.response.data.message)
                })
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
        let comments = <p style={{ textAlign: 'center' }}>Something went wrong!</p>;
        if ( !this.state.error ) {
            comments = this.state.comments.map( comment => {
                return (
                    // <Link to={'/posts/' + post.id} key={post.id}>
                    <Comment 
                        key={comment.comment_id}
                        title={comment.context}
                        author={comment.author_email}
                        time={comment.comment_time}
                        clicked={() => this.commentSelectedHandler( comment.comment_id )}/> 
                    // </Link>
                );
            } );
        }
        return (
            <div className={classes.OtherProfile}>
                <h1>Welcome to {this.props.match.params.id}'s home</h1>
                <section className={classes.Posts}>
                    {posts}
                </section>
                <h1>Comments:</h1>
                {comments}
                
                <Route path="/posts/:id" exact component={FullPost} />
            </div>
            
        );
    }
}

  
export default OtherProfile;
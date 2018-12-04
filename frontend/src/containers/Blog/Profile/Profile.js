import React, { Component } from 'react';
import axios from '../../../axios';
import { Route } from 'react-router-dom';
import { connect} from 'react-redux';
import Post from '../../../components/Post/Post';
import Comment from '../../../components/Comment/Comment'
import classes from './Profile.css';
import FullPost from '../FullPost/FullPost';

class Profile extends Component {
    state = {
        posts: [],
        comments: []
    }
    componentDidMount () {

        this.loadData();
    }
    loadData () {
        console.log(this.props.email);
        console.log(this.props)
        if ( this.props.email ) {
            
            //response = client.get(f'/api/posts?{urlencode(   }')
            axios.get( '/api/posts?' + encodeURI("user_email="+encodeURI(this.props.email)) )
            .then( response => {
                 console.log(response);
                 this.setState({posts : response.data})
            } );
        }
        if ( this.props.email ) {
            //response = client.get(f'/api/comments?{urlencode({"user_email": "xua@wustl.edu"})}')
            axios.get( '/api/comments?' + encodeURI("user_email="+encodeURI(this.props.email)))
                .then( response => {
                    console.log(response);
                    this.setState( { comments: response.data } );
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
            <div>
                <section className={classes.Profile}>
                    {posts}
                    <hr />
                    <p>Comments:</p>
                    {comments}
                </section>
                <Route path="/posts/:id" exact component={FullPost} />
            </div>
            
        );
    }
}

const mapStateToProps = state => {
    return {
        email : state.email
    }
  }
  
export default connect(mapStateToProps)(Profile);
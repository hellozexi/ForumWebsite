import React, { Component } from 'react';
import axios from '../../../axios';
import { Route } from 'react-router-dom';
import { connect} from 'react-redux';
import Post from '../../../components/Post/Post';
import Comment from '../../../components/Comment/Comment'
import classes from './Profile.css';
import EditComment from '../../Blog/EditComment/EditComment'
import FullPost from '../FullPost/FullPost';
import EditPost from '../EditPost/EditPost'
class Profile extends Component {
    state = {
        posts: [],
        comments: []
    }
    componentDidMount () {
        this.loadData();
    }
    loadData () {
        if ( this.props.email ) {
            console.log("posts:::::")
            axios.get( '/api/posts?' + encodeURI("user_email="+encodeURI(this.props.email)) )
            .then( response => {
                 console.log(response);
                 this.setState({posts : response.data})
            } )
            .catch(err => {
                alert(err.response.data.message)
            })
        }
        if ( this.props.email ) {
            //response = client.get(f'/api/comments?{urlencode({"user_email": "xua@wustl.edu"})}')
            axios.get( '/api/comments?' + encodeURI("user_email="+encodeURI(this.props.email)))
                .then( response => {
                   
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
    postDeleteHandler = (id) => {
        if(id) {
            //response = client.delete(f'/api/post/{self.post_id}')
            let config = {
                headers: {
                    'Authorization': "Token " + this.props.token
                }
            }
            axios.delete('/api/post/' + id, config)
                .then(response => {
                    this.loadData();
                })
                .catch(err => {
                    alert(err.response.data.message)
                })
        }
        
    }
    postEditHandler = (id) => {
        if(id) {
            this.props.history.push('/posts/edit/' + id)
            this.loadData();
        }
    }
    commentDeleteHandler = (id) => {
        if(id) {
            //response = client.delete(f'/api/comment/{self.comment_id}')
            let config = {
                headers: {
                    'Authorization': "Token " + this.props.token
                }
            }
            axios.delete('/api/comment/' + id, config)
                .then(response => {
                    console.log("comment deleted:::")
                    console.log(response);
                    this.loadData();
                })
                .catch(err => {
                    alert(err.response.data.message)
                })
        }
    }
    commentEditHandler = (id) => {
        if(id) {
            this.props.history.push('/comments/edit/' + id)
        }
    }
    render () {
        let posts = <p style={{ textAlign: 'center' }}>Something went wrong!</p>;
        if ( !this.state.error ) {
            posts = this.state.posts.map( post => {
                return (
                    <div>
                        <Post
                            key={post.post_id}
                            title={post.post_name}
                            author={post.poster_email}
                            //content = {post.post_content}
                            clicked={() => this.postSelectedHandler( post.post_id )} />
                            <div className={classes.Edit}>
                                <button onClick={()=> this.postDeleteHandler(post.post_id)}>Delete</button> 
                                <button onClick={()=> this.postEditHandler(post.post_id)}>Edit</button>
                            </div>
                       
                    </div>
                );
            } );
        }
        let comments = <p style={{ textAlign: 'center' }}>Something went wrong!</p>;
        if ( !this.state.error ) {
            comments = this.state.comments.map( comment => {
                return (
                    <div className={classes.Comments}>
                        <Comment 
                            key={comment.comment_id}
                            title={comment.context}
                            author={comment.author_email}
                            time={comment.comment_time}
                            clicked={() => this.commentSelectedHandler( comment.comment_id )}/>
                            <div className={classes.Edit}>
                                <button onClick={()=> this.commentDeleteHandler(comment.comment_id)}>Delete</button> 
                                <button onClick={()=> this.commentEditHandler(comment.comment_id)}>Edit</button> 
                            </div>
                            
                    </div>
                );
            } );
        }
        return (
            <div className={classes.Profile}>
                <section className={classes.Posts}>
                    {posts}
                </section>
                <h1>Comments:</h1>
                {comments}
               
                
            </div>
            
        );
    }
}

const mapStateToProps = state => {
    return {
        email : state.email,
        token : state.token
    }
  }
  
export default connect(mapStateToProps)(Profile);
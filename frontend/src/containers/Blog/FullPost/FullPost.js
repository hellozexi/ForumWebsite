import React, { Component } from 'react';
import axios from 'axios';
import {connect} from 'react-redux'
import { Redirect } from 'react-router-dom';
import classes from'./FullPost.css';
import Comment from '../../../components/Comment/Comment'
class FullPost extends Component {
    state = {
        loadedPost: null,
        comments:[],
        create : false,
        content : '',
        submitted : 'false'
    }

    componentDidMount () {
        this.loadData();
    }
    loadData () {
        console.log(this.props)
        if ( this.props.match.params.id ) {
            axios.get( '/api/post/' + this.props.match.params.id )
                .then( response => {
                    console.log("FullPost:::::::")
                    console.log(response);
                    this.setState( { loadedPost: response.data } );
                } )
                .catch(err => {
                    alert(err.response.data.message)
                })
        }
        if ( this.props.match.params.id ) {
            axios.get( '/api/comments?post_id=' + this.props.match.params.id )
                .then( response => {
                    console.log(response);
                    this.setState( { comments: response.data } );
                } )
                .catch(err => {
                    alert(err.response.data.message)
                })
        }
       
    }
    createHandler = () => {
        this.setState({
            create : !this.state.create
        })
    }
    submitHandler = () => {
        //console.log("token" + this.props.token)
        if(this.props.token && this.state.loadedPost.post_id 
            && this.state.content.length < 50 && this.state.content.length > 0) {
            let config = {
                headers: {
                    'Authorization': "Token " + this.props.token
                }
            }
            axios.post( '/api/comments', {
                'post_id': this.state.loadedPost.post_id,
                'comment_time': new Date(),
                'context': this.state.content,
            }, config)
                .then( response => {
                    console.log( response );
                    this.loadData()
                    //this.props.history.replace('/posts/' + this.props.match.params.id);
                    //this.setState( { submitted: true } );
                } )
                .catch(err => {
                    alert(err.response.data.message)
                })
        }
    }
    checkAuthorHandler = (email) => {
        console.log('EMail:' + email);
        this.props.history.push('/users/' + encodeURI(email));
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
    rollBack = () => {
        this.props.history.goBack();
    }
    render () {
        let redirect = null;
        if (this.state.submitted) {
            let url = '/posts/' + this.props.match.params.id
            console.log("redirect to:" + url)
            redirect = <Redirect to={url}  />;
        }
        let post = <p style={{ textAlign: 'center' }}>Please select a Post!</p>;
        if ( this.props.match.params.id ) {
            post = <p style={{ textAlign: 'center' }}>Loading...!</p>;
        }
        if ( this.state.loadedPost ) {
            post = (
                <div className={classes.FullPost}>
                    <h1>{this.state.loadedPost.post_name}</h1>
                    <p>{this.state.loadedPost.context}</p>
                    <p>{this.state.loadedPost.post_time}</p>
                    <div className={classes.Edit}>
                        {
                        this.props.token 
                        ?<button className={classes.delete} onClick={()=>this.checkAuthorHandler(this.state.loadedPost.poster_email)}>{this.state.loadedPost.poster_email}</button>
                        :<p>{this.state.loadedPost.poster_email}</p>
                        }
                    </div>
                    <div className={classes.Edit}>
                        
                        {this.state.create ? <textarea rows="4" value={this.state.content} onChange={( event ) => this.setState( { content: event.target.value } )} /> : null}
                        {this.state.create ? <button onClick={this.submitHandler}>submit</button> : null}
                        <button onClick={this.createHandler} className={classes.delete}>{this.state.create ? 'cancel' : 'comment'}</button>
                        <button onClick={this.rollBack} >Back</button>
                    </div>
                    <h3>Comments</h3>
                    <div className={classes.Comments}>
                        {
                            this.state.comments.map(comment => {
                                return (
                                    <div>
                                        
                                        <Comment
                                        key={comment.comment_id}
                                        title={comment.context}
                                        author={comment.author_email}
                                        time={comment.comment_time}
                                        clicked={() => this.commentSelectedHandler( comment.comment_id )}/>
                                        {
                                            this.props.email === comment.author_email ? <button onClick={()=> this.commentDeleteHandler(comment.comment_id)}>Delete</button> : null
                                            
                                        }
                                        {
                                            this.props.email === comment.author_email ? <button onClick={()=> this.commentEditHandler(comment.comment_id)}>Edit</button> : null
                                        }
                                        
                                          
                                    </div>
                                )
                        })}
                    </div>
                </div>

            );
        }

        return post;
    }
}

const mapStateToProps = state => {
    return {
        token : state.token,
        email : state.email
    }
  }
  
export default connect(mapStateToProps)(FullPost);
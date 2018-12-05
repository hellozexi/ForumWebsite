import React, { Component } from 'react';
import axios from '../../../axios';
import { Route } from 'react-router-dom';

import Post from '../../../components/Post/Post';
import classes from './Posts.css';
import FullPost from '../FullPost/FullPost';
import {connect} from 'react-redux'
class Posts extends Component {
    state = {
        posts: [],
        blockedUsers: []
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
    postEditHandler = (id) => {
        if(id) {
            this.props.history.push('/posts/edit/' + id)
        }
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
                    console.log("profile:::")
                    console.log(response);
                    this.loadData();
                })
                .catch(err => {
                    alert(err.response.data.message)
                })
        }
    }
    mute =(user, section) => {
        /*response = client.post('/api/blocks', json={
            'section_name': 'sport',
            'user_email': 'xua'
        }, headers={'Authorization': "Token " + token})*/
        let config = {
            headers: {
                'Authorization': "Token " + this.props.token
            }
        }
        axios.post('/api/blocks',{
            'section_name' : section,
            'user_email' : user
        }, config)
            .then(response => {
                console.log(response);
            })
            .catch(err => {
                alert(err.response.data.message)
            })
    }
    unMute = (user, section) => {
        let config = {
            headers: {
                'Authorization': "Token " + this.props.token
            }
        }
        /*response = client.delete(f'/api/block/sport?{urlencode({"user_email": "xua"})}',
        headers={'Authorization': "Token " + self.token})*/
        axios.delete('/api/block/' + section + "?" +  encodeURI("user_email=" + encodeURI(user)), config)
            .then(response => {
                console.log(response);
            })
            .catch(err => {
                alert(err.response.data.message)
            })
    }
    render () {
        let posts = <p style={{ textAlign: 'center' }}>Something went wrong!</p>;
        if ( !this.state.error ) {
            posts = this.state.posts.map( post => {
                return (
                    // <Link to={'/posts/' + post.id} key={post.id}>
                    <div>
                        <Post
                            key={post.post_id}
                            title={post.post_name}
                            author={post.poster_email}
                            clicked={() => this.postSelectedHandler( post.post_id )}/>
                            {this.props.email === post.poster_email ? <button onClick={()=>this.postEditHandler(post.post_id)}>Edit</button> : null}
                            {this.props.email === post.poster_email ? <button onClick={()=>this.postDeleteHandler(post.post_id)}>Delete</button> : null}
                            {
                                this.props.email==='admin'
                                ? <button onClick={()=>this.mute(post.poster_email, post.section_name)}>Mute</button>
                                : null
                            }
                             {
                                this.props.email==='admin'
                                ? <button onClick={()=>this.unMute(post.poster_email, post.section_name)}>unMute</button>
                                : null
                            }
                    </div>
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
const mapStateToProps = state => {
    return {
        token : state.token,
        email : state.email
    }
  }
  
export default connect(mapStateToProps)(Posts);
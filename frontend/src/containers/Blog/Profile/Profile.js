import React, { Component } from 'react';
import axios from '../../../axios';
import { Route } from 'react-router-dom';
import { connect} from 'react-redux';
import Post from '../../../components/Post/Post';
import classes from './Profile.css';
import FullPost from '../FullPost/FullPost';

class Profile extends Component {
    state = {
        posts: []
    }
    componentDidMount () {

        this.loadData();
    }
    loadData () {
        console.log(this.props.email);
        if ( this.props.email ) {
            axios.get( '/api/posts?user_id=' + this.props.email )
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

const mapStateToProps = state => {
    return {
        email : state.email
    }
  }
  
export default connect(mapStateToProps)(Profile);
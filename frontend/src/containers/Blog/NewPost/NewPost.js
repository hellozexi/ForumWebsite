import React, { Component } from 'react';
import axios from 'axios';
import { Redirect } from 'react-router-dom';
import {connect} from 'react-redux';
import classes from'./NewPost.css';

class NewPost extends Component {
    state = {
        title: '',
        content: '',
        section: 'default',
        submitted: false
    }

    componentDidMount () {
        // If unauth => this.props.history.replace('/posts');
        console.log( this.props );
    }

    postDataHandler = () => {
        /*json={
            'post_name': "today's sports",
            'post_time': time,
            'section_name': 'sport',
            'context': "sport is great!",
        }*/
        console.log(this.props.token)
        let config = {
            headers: {
                'Authorization': "Token " + this.props.token
            }
        }
        axios.post( '/api/posts', {
            'post_name': this.state.title,
            'post_time': new Date(),
            'section_name': this.state.section,
            'context': this.state.content,
        }, config)
            .then( response => {
                console.log( response );
                this.props.history.replace('/posts');
                this.setState( { submitted: true } );
            } );
    }

    render () {
        let redirect = null;
        if (this.state.submitted) {
            redirect = <Redirect to="/posts" />;
        }
        return (
            <div className={classes.NewPost}>
                {redirect}
                <h1>Add a Post</h1>
                <label>Title</label>
                <input type="text" value={this.state.title} onChange={( event ) => this.setState( { title: event.target.value } )} />
                <label>Content</label>
                <textarea rows="4" value={this.state.content} onChange={( event ) => this.setState( { content: event.target.value } )} />
                <label>Section</label>
                <select value={this.state.section} onChange={( event ) => this.setState( { section: event.target.value } )}>
                    <option value="default">default</option>
                    <option value="others">others</option>
                </select>
                <button onClick={this.postDataHandler}>Add Post</button>
            </div>
        );
    }
}
const mapStateToProps = state => {
    return {
        token : state.token
    }
  }
  
export default connect(mapStateToProps)(NewPost);
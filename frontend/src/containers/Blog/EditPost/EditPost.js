import React, { Component } from 'react';
import axios from 'axios';
import {connect} from 'react-redux'
import { Redirect } from 'react-router-dom';
import classes from'./EditPost.css';
class EditPost extends Component {
    state = {
        loadedPost: null,
        create : false,
        content : '',
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
                } )
                .catch(err => {
                    alert(err.response.data.message)
                })
        }
       
    }
    submitHandler = (id) => {
        console.log("id==" + id);
        /*response = client.put(f'/api/post/{self.post_id}', json={
            'context': "sport is worse!",
        }, headers={'Authorization': "Token " + self.token})*/
        if(this.props.token) {
            let config = {
                headers: {
                    'Authorization': "Token " + this.props.token
                }
            }
            console.log("content:::" + this.state.content)
            axios.put('/api/post/' + id, {
                'context' : this.state.content
            }, config)
                .then(response => {
                    console.log("result:::")
                    console.log(response);
                })
                .catch(err => {
                    alert(err.response.data.message)
                })
        }
       
        this.props.history.push("/posts/" + id);
    }
    rollBack = () => {
        this.props.history.goBack();
    }
    render () {
        let post = <p style={{ textAlign: 'center' }}>Please select a Post!</p>;
        if ( this.props.match.params.id ) {
            post = <p style={{ textAlign: 'center' }}>Loading...!</p>;
        }
        if ( this.state.loadedPost ) {
            post = (
                <div className={classes.EditPost}>
                    <h1>{this.state.loadedPost.post_name}</h1>
                    <div className={classes.Edit}>
                        <textarea rows="4" placeholder={this.state.loadedPost.context} value={this.state.content} onChange={( event ) => this.setState( { content: event.target.value } )} />
                        <button onClick={() => this.submitHandler(this.state.loadedPost.post_id)}>submit</button>
                        <button onClick={() => this.rollBack()}>Back</button>
                    </div>
                </div>

            );
        }
        return post;
    }
}

const mapStateToProps = state => {
    return {
        token : state.token
    }
  }
  
export default connect(mapStateToProps)(EditPost);
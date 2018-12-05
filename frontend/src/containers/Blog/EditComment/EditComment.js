import React, { Component } from 'react';
import axios from 'axios';
import {connect} from 'react-redux'
import { Redirect } from 'react-router-dom';
import classes from'./EditComment.css';
class EditComment extends Component {
    state = {
        loadedComment: null,
        create : false,
        content : '',
    }

    componentDidMount () {
        this.loadData();
    }
    
    loadData () {
        console.log(this.props)
        if ( this.props.match.params.id ) {
            axios.get( '/api/comment/' + this.props.match.params.id )
                .then( response => {
                    console.log(response);
                    this.setState( { loadedComment: response.data } );
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
            axios.put('/api/comment/' + id, {
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
       
        this.props.history.push("/");
    }
    rollBack = () => {
        this.props.history.goBack();
    }
    render () {
        let comment = <p style={{ textAlign: 'center' }}>Please select a comment!</p>;
        if ( this.props.match.params.id ) {
            comment = <p style={{ textAlign: 'center' }}>Loading...!</p>;
        }
        if ( this.state.loadedComment ) {
            comment = (
                <div className={classes.EditComment}>
                    <div className={classes.Edit}>
                        <textarea rows="4" placeholder={this.state.loadedComment.context} value={this.state.content} onChange={( event ) => this.setState( { content: event.target.value } )} />
                        <button onClick={() => this.submitHandler(this.state.loadedComment.comment_id)}>submit</button>
                        <button onClick={() => this.rollBack()}>Back</button>
                    </div>
                </div>

            );
        }
        return comment;
    }
}

const mapStateToProps = state => {
    return {
        token : state.token
    }
  }
  
export default connect(mapStateToProps)(EditComment);
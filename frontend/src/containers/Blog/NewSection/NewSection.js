import React, { Component } from 'react';
import axios from 'axios';
import { Redirect } from 'react-router-dom';
import {connect} from 'react-redux';
import classes from'./NewSection.css';

class NewSection extends Component {
    state = {
        title: '',
        submitted: false
    }

    componentDidMount () {
        // If unauth => this.props.history.replace('/posts');
        console.log( this.props );
        axios.get('api/sections')
            .then(response => {
                console.log(response);
                this.setState({sections : response.data});
                console.log(this.state.sections);
            })
    }

    postDataHandler = () => {
        console.log(this.props.token)
        /*response = client.post('/api/sections', json={
            'section_name': 'sport',
        }, headers={'Authorization': "Token " + self.token})*/
        let config = {
            headers: {
                'Authorization': "Token " + this.props.token
            }
        }
        axios.post( '/api/sections', {
            'section_name' : this.state.title
        }, config)
            .then( response => {
                console.log( response );
                //this.props.history.replace('/posts');
                this.setState( { submitted: true } );
            } )
            .catch(err => {
                alert(err.response.data.message)
            })
    }

    render () {
        let redirect = null;
        if (this.state.submitted) {
            redirect = <Redirect to="/" />;
        }
        return (
            <div className={classes.NewPost}>
                {redirect}
                <h1>Add a Section</h1>
                <label>Title</label>
                <input type="text" value={this.state.title} onChange={( event ) => this.setState( { title: event.target.value } )} />
                <button onClick={this.postDataHandler}>Add Section</button>
            </div>
        );
    }
}
const mapStateToProps = state => {
    return {
        token : state.token
    }
  }
  
export default connect(mapStateToProps)(NewSection);
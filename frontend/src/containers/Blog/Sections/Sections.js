import React, { Component } from 'react';
import axios from '../../../axios';
import { Route } from 'react-router-dom';

import Section from '../../../components/Section/Section';
import classes from './Sections.css';
import Posts from '../Posts/Posts'
import {connect} from 'react-redux'
class Sections extends Component {
    state = {
        sections : []
    }
    componentDidMount () {
       this.loadData()
    }
    loadData() {
        axios.get( '/api/sections' )
            .then( response => {
                const sections = response.data;
                this.setState({sections : sections})
            } )
            .catch( error => {
                // this.setState({error: true});
            } );
    }
    sectionSelectedHandler = (id) => {
        this.props.history.push( '/' + id );
    }
    sectionDelete =(id) => {
        let config = {
            headers: {
                'Authorization': "Token " + this.props.token
            }
        }
        axios.delete('/api/section/' + id, config)
            .then(response => {
                console.log(response);
                this.loadData();
            })
            .catch(err => {
                alert(err.response.data.message)
            })
        
    }
    render() {
        let sections = this.state.sections.map(section => {
            return (
                <div>
                <Section 
                    key= {section}
                    name = {section}
                    admin = 'admin'
                    clicked={() => this.sectionSelectedHandler(section)}
                /> 
                {this.props.isAdmin ? <button onClick={()=> this.sectionDelete(section)}>Delete</button> : null}
                </div>
            )
        })
        return (
            <div>
                <section className={classes.Sections}>
                    {sections}
                </section>
               
            </div>
           
        )
    }
}
const mapStateToProps = state => {
    return {
        isAdmin : state.email === 'admin',
        token : state.token
    }
  }
  
  export default connect(mapStateToProps)(Sections);
  
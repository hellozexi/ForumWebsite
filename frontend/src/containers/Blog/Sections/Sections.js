import React, { Component } from 'react';
import axios from '../../../axios';
import { Route } from 'react-router-dom';

import Section from '../../../components/Section/Section';
import classes from './Sections.css';
import Posts from '../Posts/Posts'
class Sections extends Component {
    state = {
        sections : []
    }
    componentDidMount () {
        axios.get( '/api/sections' )
            .then( response => {
                const sections = response.data;
                console.log(sections);
                // console.log( response );
                this.setState({sections : sections})
            } )
            .catch( error => {
                console.log( error );
                // this.setState({error: true});
            } );
    }
    sectionSelectedHandler = (id) => {
        console.log(this.props);
        this.props.history.push( '/' + id );
    }
    render() {
        let sections = this.state.sections.map(section => {
            return (
                <Section 
                    key= {section}
                    name = {section}
                    admin = 'admin'
                    clicked={() => this.sectionSelectedHandler(section)}
                /> 
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
export default Sections;
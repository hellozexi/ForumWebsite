import React, { Component } from 'react';
import axios from '../../../axios';
import { Route } from 'react-router-dom';

import Section from '../../../components/Section/Section';
import classes from './Sections.css';
import FullPost from '../FullPost/FullPost';
import Posts from '../Posts/Posts'
class Sections extends Component {
    state = {
        sections : ['default', 'others']
    }
    sectionSelectedHandler = (id) => {
        this.props.history.push( '/' + id );
    }
    render() {
        let sections = this.state.sections.map(section => {
            return (
                <Section 
                    key= {section}
                    name = {section}
                    admin = 'default'
                    clicked={() => this.sectionSelectedHandler(section)}
                /> 
            )
        })
        return (
            <div>
                <section className={classes.Sections}>
                    {sections}
                </section>
                <Route path={this.props.match.url + '/:id'} component={Posts} />
            </div>
           
        )
    }
}
export default Sections;
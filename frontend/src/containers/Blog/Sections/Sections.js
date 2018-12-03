import React, { Component } from 'react';
import axios from '../../../axios';
import { Route } from 'react-router-dom';

import Section from '../../../components/Section/Section';
import classes from './Sections.css';
import FullPost from '../FullPost/FullPost';

class Sections extends Component {
    state = {
        sections : ['default', 'others']
    }
    render() {
        let sections = this.state.sections.map(section => {
            return (
                <Section 
                    key= {section}
                    name = {section}
                    admin = 'default'
                /> 
            )
        })
        return (
            <section className={classes.Posts}>
                {sections}
            </section>
        )
    }
}
export default Sections;
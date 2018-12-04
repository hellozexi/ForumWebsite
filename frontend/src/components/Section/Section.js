import React from 'react';

import classes from './Section.css';

const section = (props) => (
    <article className={classes.Section} onClick={props.clicked}>
        <h1>{props.name}</h1>
        <div className={classes.Info}>
            <div className={classes.Admin}>{props.admin}</div>
        </div>
    </article>
);

export default section;
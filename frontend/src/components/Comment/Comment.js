import React from 'react';

import classes from './Comment.css';

const comment = (props) => (
    <article className={classes.Comment} onClick={props.clicked}>
        <h1>{props.title}</h1>
        <div className={classes.Info}>
            <div className={classes.Author}>{props.author}</div>
        </div>
    </article>
);

export default comment;
import React from 'react';

import classes from './Comment.css';

const comment = (props) => (
    <article className={classes.Comment} onClick={props.clicked}>
        <p>{props.title}</p>
        <div className={classes.Info}>
            <div className={classes.Author}>{props.author}</div>
        </div>
    </article>
);

export default comment;
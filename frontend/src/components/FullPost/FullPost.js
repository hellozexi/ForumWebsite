import React, { Component } from 'react';
import axios from 'axios';

import './FullPost.css';

class FullPost extends Component {
  

    render () {
        let post = (
            <div className="FullPost">
                <h1></h1>
                <p></p>
                <div className="Edit">
                    <button onClick={this.deletePostHandler} className="Delete">Delete</button>
                </div>
            </div>

        );
        return post;
    }
}

export default FullPost;

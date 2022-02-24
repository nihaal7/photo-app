
const story2Html = story => {
    return `
        <div id = 'story_box'>
            <img id = 'story_pic' src='${ story.user.thumb_url }' alt="profile pic for ${ story.user.username }" />
            <p id ='story_name'>${ story.user.username }</p>
        </div>
    `;
};

const displayStories = () => {
    fetch('api/stories')
        .then(response => response.json())
        .then(stories => {
            const html = stories.slice(0,6).map(story2Html).join('\n');
            document.querySelector('#stories').innerHTML = html;
        })
};

const suggestions2Html = suggestion => {
    return `
    <div id = suggestion_box>
        <img id = 'suggestion_pic' src = '${ suggestion.thumb_url}' alt = 'profile pic for ${ suggestion.username}' />
        <div id ='suggested_name_box'>
            <p id = suggested_name>${ suggestion.username}</p>
            <p id = 'suggested_for_you'>suggested for you</p>
        </div>
            <div id = 'follow_box'>
            <p><a href="#" id = 'follow_${suggestion.id}' aria-label = 'Following' aria-checked = 'False' onclick="follow_button_handler('${suggestion.id}')">follow</a></p>
            </div>
    </div>
    `;
};
    
const displaySuggestions = () => {
    fetch('api/suggestions')
        .then(response => response.json())
        .then(suggestions => {
            const html = suggestions.map(suggestions2Html).join('\n');
            document.querySelector('#actual_recommendations').innerHTML = html;
        })
};

const displayProfile = () => {
    fetch('api/profile')
        .then(response => response.json())
        .then(profile => {
            html = `
            <div id='picdiv'>              
                    <img id = 'ppic' src = '${ profile.image_url }' alt='profile pic for ${ profile.username }'/>
            </div>      
             <div id='namediv'>
                    <h2>${ profile.username }</h2>
            </div>
            `;
            document.querySelector('#profile_pic_name').innerHTML = html;
        })
};

const updatePost = (post_box,id) => {
    fetch('api/posts/'+id)
    .then(response => response.json())
    .then(posts => {
        const html = postUpdateHTML(posts)
        post_box.innerHTML = html;
    })
};

const likeUnlike = ev => {
    id = ev.currentTarget.dataset.postId;
    currently_liked = ev.currentTarget.dataset.currLiked;
    likeid = ev.currentTarget.dataset.likeId;
    post_box = ev.currentTarget.parentNode.parentNode.parentNode;
    data = {};
    if (currently_liked ==='no'){
        fetch('/api/posts/'+id+'/likes', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            updatePost(post_box,id)
        })
        .catch(err => {
            console.error(err);
            alert('Error!');
        });
    }
    else{
        fetch('/api/posts/'+id+'/likes/'+likeid, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            updatePost(post_box,id)
        })
        .catch(err => {
            console.error(err);
            alert('Error!');
        });
    }
};

const bookmarkUnbookmark = ev => {
    id = ev.currentTarget.dataset.postId;
    currently_bookmarked = ev.currentTarget.dataset.currBookmarked;
    bookmarkid = ev.currentTarget.dataset.bookmarkId;
    post_box = ev.currentTarget.parentNode.parentNode;
    data = {
        "post_id": id,
    };
    if (currently_bookmarked ==='no'){
        fetch('/api/bookmarks', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            updatePost(post_box,id)
        })
        .catch(err => {
            console.error(err);
            alert('Error!');
        });
    }
    else{
        fetch('/api/bookmarks/'+bookmarkid, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            updatePost(post_box,id)
        })
        .catch(err => {
            console.error(err);
            alert('Error!');
        });
    }
};

const destoryModal = (ev,postId) => {
    document.querySelector('#modal-container').innerHTML = '';
    document.querySelector('#'+'view_more_'+postId).focus();
};

const comments2Html = comment => {
    return `
    <div class='modal_individual_comment_box'>
        <div class = 'modal_comment_pic_box'>
            <img class='modal_comment_pic' src='${comment.user.thumb_url}'/>
        </div>    
        <div class = 'modal_comment_text_box'>
            <p><b>${comment.user.username}</b> ${comment.text}</p>
            <p><b>${comment.display_time}</p></b>
        </div>
        <div class = 'modal_comment_heart_box'>
            <i class="far fa-heart"></i>
        </div>    
    </div>
    `;
};

const showPostDetail = ev => {
    const postId = ev.currentTarget.dataset.postId;
    view_post_id = postId;
    fetch(`/api/posts/${postId}`)
        .then(response => response.json())
        .then(post=> {
            const html = `
            <div class ="modal-bg">
                <button id='close_button' onClick="destoryModal(event,${postId})">
                    <i class="fas fa-times"></i>
                </button>
                <div class ="modal">
                    <img class="modal_image" src='${post.image_url}'/>
                    <div class="modal_right">
                        <div class="modal_profile">
                        <img class="modal_profile_pic" src='${post.user.image_url}'/>
                        ${post.user.username}
                        </div>
                        <div class="modal_comments">
                            ${post.comments.map(comments2Html).join('\n')}
                        <div>
                    </div
                </div>
            </div> 
        `;
        document.querySelector('#modal-container').innerHTML = html;
        document.querySelector('#close_button').focus();
        // alert(document.querySelector('.fa-times').className)
        })
};

const postComment = ev => {
    comment_box = ev.currentTarget.parentNode.children[1];
    text = comment_box.value;
    post_id = ev.currentTarget.dataset.postId;
    post_box = ev.currentTarget.parentNode.parentNode;
    data = {
        "post_id": post_id,
        "text": text
    };
    fetch('/api/comments', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        updatePost(post_box,post_id)
    })
    .catch(err => {
        console.error(err);
        alert('Error!');
    });
};

const displayComments = (comments,postId) => {
    let html ='';
    if (comments.length > 1){
        html+=`<button class='link' id='view_more_${postId}' data-post-id = '${postId}'onclick="showPostDetail(event);"> View all ${comments.length} comments</button>`;
    }
    if (comments && comments.length > 0){
        const lastComment = comments[comments.length - 1];
        html += `<p>
                    <b>${lastComment.user.username}</b>
                    ${lastComment.text}
                    <div>${lastComment.display_time}</div>
                </p>`;
    }
    return html;
};

const postUpdateHTML = post => {
    return `
        <div id='post_header_box'>
        <div id='post_user_name_box'>
            <b>${post.user.username}</b>
        </div>
        <div id='post_3dots_box'>
            <i class="fas fa-ellipsis-h"></i>
        </div>
    </div>
    <div id='post_image_box'>
        <img id='post_image' src = '${post.image_url}' alt ='posted photo by ${post.user.username}'/>
    </div>
    <div id='post_reactions_box'>
        <div id='post_reactions_box_left'>
            <button data-like-id='${post.current_user_like_id}' data-post-id = '${post.id}' onclick='likeUnlike(event)' data-curr-liked='${post.current_user_like_id ? 'yes':'no'}' aria-label = 'user_liked' aria-checked = ${post.current_user_like_id ? 'True':'False'}>
            <i class="fa${post.current_user_like_id ? 's':'r'} fa-heart"></i>
            </button>
            <i class="far fa-comment"></i>
            <i class="far fa-paper-plane"></i>                       
        </div>
            <button data-bookmark-id='${post.current_user_bookmark_id}' data-post-id = '${post.id}' onclick='bookmarkUnbookmark(event)' data-curr-bookmarked='${post.current_user_bookmark_id ? 'yes':'no'}' aria-label = 'user_bookmarked' aria-checked = ${post.current_user_bookmark_id ? 'True':'False'}>
            <i class="fa${post.current_user_bookmark_id ? 's':'r'} fa-bookmark"></i>
            </button>
    </div>
    <div id='post_likes_box'>
        <p> ${post.likes.length} likes</p>
    </div>
    <div id='post_titles_box'>
        <p><b>${post.user.username}</b> ${post.caption}</p>
    </div>
    <div id='post_time_box'>
    <p>${post.display_time}</p>
    </div>
    <div id='post_comments_box'>
    ${displayComments(post.comments,post.id)}
    </div>
    <div id='post_your_comment_box'>
        <i class="far fa-smile"></i>
        <input type='text' placeholder='Add a comment...' id='comment_form' aria-label="comment box">
        <button onclick='postComment(event)' data-post-id = '${post.id}'> 
            <b>Post</b>
        </button>
    </div>
    `;
};

const posts2Html = post => {
    return `
    <div id='post_box'>
        <div id='post_header_box'>
            <div id='post_user_name_box'>
                <b>${post.user.username}</b>
            </div>
            <div id='post_3dots_box'>
                <i class="fas fa-ellipsis-h"></i>
            </div>
        </div>
        <div id='post_image_box'>
            <img id='post_image' src = '${post.image_url}' alt ='posted photo by ${post.user.username}'/>
        </div>
        <div id='post_reactions_box'>
            <div id='post_reactions_box_left'>
                <button data-like-id='${post.current_user_like_id}' data-post-id = '${post.id}' onclick='likeUnlike(event)' data-curr-liked='${post.current_user_like_id ? 'yes':'no'}' aria-label = 'user_liked' aria-checked = ${post.current_user_like_id ? 'True':'False'}>
                <i class="fa${post.current_user_like_id ? 's':'r'} fa-heart"></i>
                </button>
                <i class="far fa-comment"></i>
                <i class="far fa-paper-plane"></i>                       
            </div>
                <button data-bookmark-id='${post.current_user_bookmark_id}' data-post-id = '${post.id}' onclick='bookmarkUnbookmark(event)' data-curr-bookmarked='${post.current_user_bookmark_id ? 'yes':'no'}' aria-label = 'user_bookmarked' aria-checked = ${post.current_user_bookmark_id ? 'True':'False'}>
                <i class="fa${post.current_user_bookmark_id ? 's':'r'} fa-bookmark"></i>
                </button>
        </div>
        <div id='post_likes_box'>
            <p> ${post.likes.length} likes</p>
        </div>
        <div id='post_titles_box'>
            <p><b>${post.user.username}</b> ${post.caption}</p>
        </div>
        <div id='post_time_box'>
        <p>${post.display_time}</p>
        </div>
        <div id='post_comments_box'>
        ${displayComments(post.comments,post.id)}
        </div>
        <div id='post_your_comment_box'>
            <i class="far fa-smile"></i>
            <input type='text' placeholder='Add a comment...' id='comment_form' aria-label="comment box">
            <button onclick='postComment(event)' data-post-id = '${post.id}'> 
                <b>Post</b>
            </button>
        </div>
    </div>
    `;
};

const displayPosts = () => {
    fetch('api/posts/?limit=10')
        .then(response => response.json())
        .then(posts => {
            const html = posts.map(posts2Html).join('\n');
            document.querySelector('#feed').innerHTML = html;
        })
};

const follow_button_handler = (user_id) => {
    id = '#' + 'follow_' + user_id;
    if (document.querySelector(id).innerHTML == 'unfollow'){
        unfollow_id = document.querySelector(id).getAttribute("unfollow_id");
        const data = {
            'id' : unfollow_id
        };
        document.querySelector(id).innerHTML = 'follow';
        document.querySelector(id).ariaChecked  = 'False';
        fetch('/api/following/'+unfollow_id, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch(err => {
            console.error(err);
            alert('Error!');
        });
    
    }
    else{
        document.querySelector(id).innerHTML = 'unfollow';
        document.querySelector(id).ariaChecked  = 'True';
        const data = {
            'user_id' : user_id
        };
        fetch('/api/following', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            document.querySelector(id).setAttribute("unfollow_id", data.id);
        })
        .catch(err => {
            console.error(err);
            alert('Error!');
        });
    }
};

const initPage = () => {
    displayStories();
    displaySuggestions();
    displayProfile();
    displayPosts();
};

// invoke init page to display stories:
initPage();
var view_post_id;
window.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
    destoryModal(event,view_post_id)      
    }
  })
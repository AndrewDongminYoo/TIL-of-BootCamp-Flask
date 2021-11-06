const thumbnail = (til_post) => {
    const { title, description, site_name, url, image, registered, modified, shared, comment, name } = til_post;
    return `
        <li class="list_has_image animation_up_late">
            <a href="${url}" target="_blank" class="link_post #post_list">
                <div class="post_title has_image">
                    <strong class="tit_subject">${title}</strong>
                    <div class="wrap_sub_content"></div>
                    <em class="tit_sub"></em>
                    <span class="article_content">${description}...</span>
                    <span class="mobile_d_n post_append">
                        <span>공유</span>
                        <span class="num_txt">${shared}</span>
                        <span class="ico_dot"></span>
                        <span>댓글</span>
                        <span class="num_txt">${comment}</span>
                        <span class="ico_dot"></span>
                        <span class="publish_time">${moment(registered).fromNow()}</span>
                        <span class="ico_dot"></span>
                        <span class="txt_by">${site_name}</span>
                        <span class="ico_dot"></span>
                        <span>By ${name}</span>
                    </span>
                </div>
                    <div class="post_thumb" style="background-image: url('${image}')">
                </div>    
            </a>
        </li>`

}

const rankAuthor = (author, count) => {
    const { username, url, image, hobby, specialty } = author;
    return `
        <a class="item_recommend" href="${url}" target="_blank">
            <span class="thumb_g">
                <img src="${image}" width="36" height="36" class="img_thumb" alt="${username}">
            </span>
            <div class="detail_recommend">
                <div class="inner_recommend">
                    <span class="txt_recommend">${username} 🔥</span>
                    <span class="txt_info">
                        <span class="txt_g">글 ${count}</span>
                        <span class="ico_dot"></span>
                        <span class="txt_g">${hobby}</span>
                        <span class="txt_g">${specialty}</span>
                    </span>
                </div>
            </div>
        </a>`
}

const unrankAuthor = (author) => {
    const { username, url, image, hobby, specialty } = author;
    return `
        <a class="item_recommend" href="${url}" target="_blank">
            <span class="thumb_g">
                <img src="${image}" width="36" height="36" class="img_thumb" alt="${username}">
            </span>
            <div class="detail_recommend">
                <div class="inner_recommend">
                    <span class="txt_recommend">${username}</span>
                    <span class="txt_info">
                        <span class="ico_dot"></span>
                        <span class="txt_g">${hobby}</span>
                        <span class="txt_g">${specialty}</span>
                    </span>
                </div>
            </div>
        </a>`
}

const suggest = (author) => {
    const { username, url, image, member_card } = author;
    return `                            
        <li class="animation_up_late">
            <a href="${url}" class="link_g #user_recomm" target="_blank" data-tiara-search_term="${username}">
                <img src="${image}" width="120" height="120" class="thumb_img" alt="${username}">
                <strong class="tit_wirter">${username}</strong>
                <span class="txt_wirter">${member_card}</span>
            </a>
        </li>`
}
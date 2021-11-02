import config from './config.json';

const secretKey = config.secretKey;
const apiKey = config.apiKey;
const background = "https://scrap.kakaocdn.net/dn/cNyWaL/hyL5K4urQQ/PWUPB1xuDotr1XBrvXIn21/img.png?width=1200&amp;height=630&amp;face=0_0_1200_630"

const thumbnail = (til_post) => {
    const { title, description, url, image, reg_date, shared, comment, author } = til_post;
    return `
        <li class="list_has_image animation_up_late"></li><a href="${url}" target="_blank" class="link_post #post_list">
        <div class="post_title has_image"></div><strong class="tit_subject">${title}</strong>
        <div class="wrap_sub_content"></div><em class="tit_sub"></em></em><span class="article_content">${description}</span></div>
        <span class="mobile_d_n post_append"></span><span>공유</span><span class="num_txt">${shared}</span><span class="ico_dot"></span></span><span>댓글</span><span class="num_txt">${comment}</span><span class="ico_dot"></span></span><span class="publish_time">${reg_date}</span><span class="ico_dot"></span></span><span class="txt_by">by</span><span>${author}</span></span></div>
        <div class="post_thumb">
            <img class="mobile_d_n img_thumb" src="${image}" alt="이미지정보">
            <img class="pc_d_n img_thumb" src="${image}" alt="이미지정보">
        </div>
        <span class="pc_d_n post_append"></span><span>공유</span><span class="num_txt">${shared}</span><span class="ico_dot"></span></span><span>댓글</span><span class="num_txt">${comment}</span><span class="ico_dot"></span></span><span class="publish_time">${reg_date}</span><span class="ico_dot"></span></span><span class="ico_brunch txt_by">by</span><span>By ${author}</span></span></a>
        </li>`
}

const rankAuthor = (author) => {
    const { username, url, image } = author;
    return `
        <a class="item_recommend" href="${url}" target="_blank">
            <span class="thumb_g">
                <img src="${image}" width="36" height="36" class="img_thumb" alt="${username}">
            </span>
            <div class="detail_recommend">
                <div class="inner_recommend">
                    <span class="txt_recommend">${username}</span>
                </div>
            </div>
        </a>`
}
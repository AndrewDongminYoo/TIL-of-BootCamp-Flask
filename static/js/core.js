const thumbnail = (til_post) => {
    const { title, description, site_name, url, image, registered, shared, comment, name } = til_post;
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

const getRank = () => {
    fetch('/api/rank')
        .then(res => res.json())
        .then(results => {
            let rankers = []
            results
                .forEach(person => {
                    let template = rankAuthor(person, person["blog_list"].length)
                    rankers.push(template)
                })
            document.querySelector("#rec1").innerHTML = rankers.join("")
        })
}

const comingSoon = () => {
    fetch("/api/none")
        .then(res => res.json())
        .then((result) => {
            let names = [];

            result.forEach((nbc, i) => {
                names.push(`<a class="keyword_elem"
                   href="https://teamsparta.notion.site/0dd2d4c1d21e41dabf60c45cf2c0c9a6?v=226b3128e1f14d8393e0ce475946446c"
                   target="_blank">${(i % 2 === 0 ? "" : " ") + nbc}</a>`)
            });
            let keyword = document.getElementById("keywordItemListBlock")
            keyword.innerHTML = names.join("")
        })
}

const cannotCrawl = () => {
    fetch('/api/notion_naver_medium')
        .then(res => res.json())
        .then(results => {
            let rankers = []
            results.forEach((person) => {
                let template = unrankAuthor(person)
                rankers.push(template)
            })
            document.querySelector("#rec2").innerHTML = rankers.join("")
        })
}

const KeyPress = (event) => {
    if (event.key === 'Enter') {
        const query = document.querySelector("#txt_search").value
        window.location.href = "#" + query;
    }
}

const router = async () => {

    const query = window.location.hash.substr(1);
    let res;
    if (query) {
        res = await fetch(`/api/list?query=${query}`);
    } else {
        res = await fetch("/api/list");
    }
    let result = await res.json()
    let postList = [];
    result.forEach((post) => {
        postList.push(thumbnail(post))
    })
    cannotCrawl();
    getRank();
    comingSoon();
    let articles = document.querySelector(".list_article")
    articles.innerHTML = postList.join("")
    return 200;
}

window.addEventListener("hashchange", router)
router().then(res=>console.log(res));

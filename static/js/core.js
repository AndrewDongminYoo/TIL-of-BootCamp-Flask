// import config from './config.json';
//
// const secretKey = config.secretKey;
// const apiKey = config.apiKey;
// const background = "https://scrap.kakaocdn.net/dn/cNyWaL/hyL5K4urQQ/PWUPB1xuDotr1XBrvXIn21/img.png?width=1200&amp;height=630&amp;face=0_0_1200_630"

window.onload = () => {
    getRank();
    getPost();
}

const getRank = () => {
    fetch('/api/rank')
        .then(res => res.json())
        .then(results => {
            let rankers = []
            results.forEach((person)=> {
            let template = rankAuthor(person)
                rankers.push(template)
            })
            document.querySelector(".search_recommend").innerHTML=rankers.join("")
        })
}

const getPost = () => {
    fetch("/api/list")
        .then(res=>res.json())
        .then(results=>{
            let postList = [];
            results.forEach((post)=>{
                let template = thumbnail(post)
                postList.push(template)
            })
            document.querySelector(".list_article").innerHTML=postList.join("")
        })
}
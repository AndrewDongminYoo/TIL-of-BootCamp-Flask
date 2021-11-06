const getRank = () => {
    fetch('/api/rank')
        .then(res => res.json())
        .then(results => {
            let rankers = []
            Object.entries(results)
                .sort(([e,])=>-parseInt(e))
                .forEach(([cnt, person])=> {
                    let template = rankAuthor(person, cnt)
                        rankers.push(template)
            })
            document.querySelector("#rec1").innerHTML=rankers.join("")
        })
}

const cannotCrawl = () => {
    fetch('/api/notion_naver_medium')
        .then(res => res.json())
        .then(results => {
            let rankers = []
            results.forEach((person)=> {
            let template = unrankAuthor(person)
                rankers.push(template)
            })
            document.querySelector("#rec2").innerHTML=rankers.join("")
        })
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
    let articles = document.querySelector(".list_article")
    articles.innerHTML = postList.join("")
}

const KeyPress = (event) => {
    if (event.key === 'Enter') {
        const query = document.querySelector("#txt_search").value
        window.location.href="#"+query;
    }
}

const comingSoon = () => {
    fetch("/api/none")
        .then(res=>res.json())
        .then(result=>{
            let names = [];
            result.forEach((nbc)=> {
                names.push(`<a class="keyword_elem"
                   href="https://teamsparta.notion.site/0dd2d4c1d21e41dabf60c45cf2c0c9a6?v=226b3128e1f14d8393e0ce475946446c"
                   target="_blank">${nbc}</a>`)
            });
            let keyword =  document.getElementById("keywordItemListBlock")
            keyword.innerHTML=names.join("")
        })
}

window.addEventListener("hashchange", router)
router();
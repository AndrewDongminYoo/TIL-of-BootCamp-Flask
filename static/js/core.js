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
import config from './config.json';

const secretKey = config.secretKey;
const apiKey = config.apiKey;
const background = "https://scrap.kakaocdn.net/dn/cNyWaL/hyL5K4urQQ/PWUPB1xuDotr1XBrvXIn21/img.png?width=1200&amp;height=630&amp;face=0_0_1200_630"

const thumbnail = (til_post) => {
    const { title, description, host, url, image } = til_post;
    return `<figure id="" contenteditable="false" data-ke-type="opengraph" data-ke-align="alignCenter"
            data-og-type="website" data-og-title="${title}"
            data-og-description="${description}"
            data-og-host="${host}" data-og-source-url="${url}"
            data-og-url="${url}"
            data-og-image="${image}">
        <a href="$[url}" target="_blank" rel="noopener"
           data-source-url="$[url}" style="">
            <div class="og-image"
                 style="background-image: url('${background}');">
                &nbsp;
            </div>
            <div class="og-text">
                <p class="og-title" data-ke-size="size16">${title}</p>
                <p class="og-desc" data-ke-size="size16">${description}...</p>
                <p class="og-host" data-ke-size="size16">${host}</p>
            </div>
        </a>
    </figure>`
}
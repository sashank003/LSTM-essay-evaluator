// JavaScript Document
document.getElementById("text").value = localStorage.getItem("comment");
var sp = document.getElementById("sp");
function bodyOnloadHandler(){ 
	
	"use strict";
	if (window.location=='http://localhost:5000/'){
		localStorage.setItem("comment", "");
	}
	if (window.location=='http://localhost:5000/submit'){
		if (document.getElementById("text").value==""){
			sp.innerHTML= 0;
		}
	}
}



function savetext() {
	"use strict";
    var comment = document.getElementById("text").value;
    if (comment == "") {
        alert("Please enter your text");
//		location.reload();
		localStorage.setItem("comment", "");
        return true;
    }
    localStorage.setItem("comment", comment);
//	alert = function(){};
	
//    location.reload();
    return true;
    //return true;
}



function savefile() {
	"use strict";
    var fullPath = document.getElementById("file").value;
	fullPath = fullPath.replace(/^.*[\\\/]/, '');
    if (fullPath == "") {
        alert("Please select your file");
		window.location = '/getfile';
//		location.reload();
		localStorage.setItem("comment", "");
        return true;
    }
	alert('file selected: ' + fullPath);
	localStorage.setItem("comment", "");
//    location.reload();
    return true;
}




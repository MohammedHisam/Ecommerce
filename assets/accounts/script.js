const home = document.getElementById("home");
const login = document.getElementById("login");
const register = document.getElementById("register");
const close_nav = document.getElementsByTagName("ul");

const same = function () {
    home.classList.remove("current-list-item");
    document.getElementsByTagName("body")[0].style.overflow = "hidden";
    document.getElementById("body").style.filter = "blur(3px)";
    for (let i = 0; i < close_nav.length; ++i)
        close_nav[i].style.display = "none";
}

function form_open(element) {
    same();
    if (element === "login") {
        register.classList.remove("current-list-item");
        login.classList.add("current-list-item");
        document.getElementById("register-form").style.display = "none";
        document.getElementById("login-form").style.display = "block";

    } else {
        login.classList.remove("current-list-item");
        register.classList.add("current-list-item");
        document.getElementById("login-form").style.display = "none";
        document.getElementById("register-form").style.display = "block";

    }
}


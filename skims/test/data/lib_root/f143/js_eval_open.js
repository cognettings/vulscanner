function functionAWithConsoleLog(req) {
    var a = 13
    var c = Math.floor((Math.random() * 100) + 1);
    localStorage.getItem('key');
    try {
        if(a == "") throw "empty";
        if(isNaN(a)) throw "not a number";
        c = Number(a);
        if(c < 5) throw "too low";
        if(c > 10) throw "too high";
        eval('alert("Your query string was ' + unescape(document.location.search) + '");');
        eval(req.query.input)
        eval("Your query string is a literal string and it is reasonably safe.") // Compliant
        // eval('alert("Your query string was ' + unescape(document.location.search) + '");');
    }
    catch(err) {
        // a comment
        /* a comment */
        /*
            a comment
        */
    }
}

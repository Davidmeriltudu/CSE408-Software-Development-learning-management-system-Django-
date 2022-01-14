$(function(){
var counter = 0;
var timer = document.getElementById('timeVariable');
var timeleft = parseInt(timer.textContent)*10;
console.log(timeleft)
var timeUp = false

function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
console.log(csrftoken);

function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function convertSeconds(s)
{
    var min = Math.floor(s/60);
    var sec = s%60;
    if(min == 0 && sec == 0)
        timeUp = true
    var min_str = min.toString()
    var sec_str = sec.toString()
    var length_min = min_str.length
    var length_sec = sec_str.length
    if(length_min==1)
        min_str = "0"+min_str
    if(length_sec == 1)
        sec_str = "0"+sec_str

    return min_str+":"+sec_str;
}

function setup()
{
    timer.innerHTML = convertSeconds(timeleft-counter);

    function timeIt()
    {
    if(timeUp == true)
        {
            var nameNo = 0;
            var name = "form-"+nameNo.toString()+"-choice";
            var choicePkList = [];

            while(document.getElementsByName(name))
            {
                choices = document.getElementsByName(name);
                console.log(choices)
                for (var i = 0; i < choices.length; i++)
                {
                    if(choices[i].checked)
                    {
                        choicePkList.push(choices[i].value);
                    }
                    choices[i].value = -1;
                    nameNo++;
                    name = "form-"+nameNo.toString()+"-choice";
                }
            }
            console.log(choicePkList)
            var quiz_pk = $('body').data('quiz_pk');
            var dict = {'choicePkList': choicePkList, 'quiz_pk': quiz_pk}
            $.ajax({
                type: "POST",
                url: "/home/quizStudent/timeUp/",
                data: JSON.stringify({
                    'dict': dict,
                    'csrfmiddlewaretoken': csrftoken,
                }),
                success: function(data){
                    console.log("success");
                    window.location.href = data;
                },
                failure: function(data){
                    console.log("failure");
                    console.log(data);
                },
            })
        }
        counter++;
        timer.innerHTML = convertSeconds(timeleft-counter);
    }
    setInterval(timeIt,1000);
}
setup()
});
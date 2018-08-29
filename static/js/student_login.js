/**
 * Created by haier on 2017-12-09.
 */
$("#subBtn").on("click", function () {

    $.ajax(
        {
            url: "/login/",
            type: "POST",

            data: {
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                user: $("#username").val(),
                pwd: $("#password").val()


            },
            success: function (data) {

                var dat = JSON.parse(data);

                if (dat["state"] == "login_success") {
                    location.href = "/"

                }
                if (dat["state"] == "user_none") {
                    $("#username").focus();
                    var use = $("#helpBlock2");
                    use.parent().addClass("has-error");
                    use.html("请输入用户名")
                }
                if (dat["state"] == "pwd_none") {
                    $("#password").focus();
                    var pwd = $("#helpBlock3");
                    pwd.parent().addClass("has-error");
                    pwd.html("请输入登录密码")
                }


                if (dat["state"] == "failed") {

                    $(".failed").html("用户名或密码错误").css("color", "red")
                }


            }
        }
    )
});
function Auth() {
    var self = this;
}

Auth.prototype.run = function () {
    var self = this;
    self.listenLoginEvent();
};

$(function () {  // 直接运行
    var auth = new Auth();
    auth.run();
});

Auth.prototype.listenLoginEvent = function () {
    var self = this;
    var telephoneInput = $("#InputTelephone");
    var passwordInput = $("#InputPassword");
    var rememberInput = $("#rememberMe");
    var submitBtn = $("#login-btn");

    submitBtn.click(function () {
        event.preventDefault();  // 阻止表单的默认提交

        var telephone = telephoneInput.val();
        var password = passwordInput.val();
        var remember = rememberInput.val();
        var token = null;
        csrf_ajax.get({
            'url': '/users/token/',
            'success': function (result) {
                if(result['csrftoken']){
                    token = result['csrftoken'];
                }
            },
            'token': token,
        });

        csrf_ajax.post({
            'url': '/users/login/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember ? 1 : 0,  // remember是string
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    more_sweetalert.alertSuccess("登陆成功, 点击回到首页", function () {
                        window.location.href = "/";
                    });
                } else {
                    var objectDict = result['message'];  //后端返dict()
                    // 如果是string
                    if (typeof objectDict === 'string' || objectDict.constructor === String) {
                        window.messageBox.showError(objectDict);
                    } else {
                        // 如果是dict
                        for (var key in objectDict) {
                            var messageValues = objectDict[key];  // list()
                            var message = messageValues[0];  // list中的首个值
                            window.messageBox.showError(message);
                        }
                    }
                }
            },
            'error': function (error) {
                more_sweetalert.alertErrorToast("逻辑问题，获取tokening, 请再点一次")

            },
        })
    })
};
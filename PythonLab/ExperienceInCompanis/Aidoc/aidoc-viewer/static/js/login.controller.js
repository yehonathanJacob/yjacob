function LoginController() {

    this.login = function (element) {


        $('.logout-link').hide();

        $('.quit-app-link').on('click', function () {
            aidocViewer.utils.extensionUtils.attemptQuit();
            return false;
        });

        if (aidocViewer.services.ConfigService.showSupportLink) {
            aidocViewer.utils.supportUtils.getSupportPhone().then(function (supportPhone) {
                $('.login-support-phone-number').text(supportPhone);
                $('.login-support-container').removeClass('hidden');
            });
        }

        var loginForm = $('#login-form');
        var username = $('#inputUsername');
        var password = $('#inputPassword');
        var browser_type = this.get_browser_type();
        username.focus();

        loginForm.on('submit', function (e) {
            e.preventDefault();

            var loginData = {
                username: username.val(),
                password: password.val(),
                browser_type: browser_type
            };

            aidocViewer.services.AuthService.login(loginData)
                .success(function () {
                    page.redirect('/');
                })
                .error(function (httpObj, textStatus) {
                    if (httpObj.status == 401) {
                        bootbox.alert('Invalid user name or password');
                    } else {
                        bootbox.alert('Something went wrong while trying to login. Please contact support for assistance');
                    }
                });
        });
    }

    this.get_browser_type = function () {


        isSafari = /constructor/i.test(window.HTMLElement) || (function (p) {
            return p.toString() === "[object SafariRemoteNotification]";
        })(!window['safari'] || safari.pushNotification);

        if (isSafari)
            return 'Safari';

        isChrome = !!window.chrome && !!window.chrome.webstore;

        if (isChrome)
            return 'Chrome';

        isIE = /*@cc_on!@*/false || !!document.documentMode;

        if (isIE)
            return 'Internet Explorer';

        isEdge = !isIE && !!window.StyleMedia;

        if (isEdge)
            return 'Edge';

        isFirefox = typeof InstallTrigger !== 'undefined';

        if (isFirefox)
            return 'Firefox';
        return 'Unknown'
    }

}

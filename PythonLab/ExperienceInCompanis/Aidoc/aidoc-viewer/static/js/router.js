var mainContent = $('#main-content');
var globals = {
    lastOpenUid: null,
    lastChosenFilter: null,
    worklist: [],
    username: null
};

// Prevent scrolling on iOS
document.body.addEventListener('touchmove', function (e) {
    e.preventDefault();
});

// Try to open the secondary window on page load (might trigger a popup warning)
$(function () {
    aidocViewer.services.WindowManager.openSecondaryWindow();
});

$(window).on('unload', function () {
    aidocViewer.services.WindowManager.closeSecondaryWindow();
});

// Disable the image cache in cornerstone (we implement the cache ourselves)
cornerstone.imageCache.setMaximumSizeBytes(0);

page('*', function(ctx, next) {
    if (ctx.path.indexOf('/scan') === 0) {
        if (!aidocViewer.services.WindowManager.isSecondaryWindowOpen()) {
            aidocViewer.services.WindowManager.openSecondaryWindow();
        }

        aidocViewer.services.WindowManager.initViewer();
    } else {
        aidocViewer.services.WindowManager.destroyViewer();
        aidocViewer.services.ToolboxService.close();
    }

    next();
});

// transition "middleware"
page('*', function (ctx, next) {
    mainContent.LoadingOverlay('hide', true);

    if (ctx.init) {
        next()
    } else {
        mainContent.addClass('transition');
        setTimeout(function () {
            mainContent.removeClass('transition');
            next();
        }, 300);
    }
});

page('*', function (ctx, next) {
    $('.tooltip').tooltip('destroy');
    aidocViewer.services.ToolboxService.close();
    next();
});

page('/', pageLoader.bind(null, 'templates/worklist.html'), resetCornerstone, checkLogin, index);
page('/worklist/:username', pageLoader.bind(null, 'templates/worklist.html'), resetCornerstone, checkLogin, worklist);
page('/logout', logout);
page('/login', pageLoader.bind(null, 'templates/login.html'), login);
page('/scan/*', startTimeMeasurement, resetCornerstone);
page('/scan/:uid', pageLoader.bind(null, 'templates/scan.html'), checkLogin, showScan);
page('/admin', pageLoader.bind(null, 'templates/users.html'), checkLogin, adminUsersView);
page('/admin/metrics', pageLoader.bind(null, 'templates/metrics.html'), checkLogin, adminMetricsView);
page('/admin/users', pageLoader.bind(null, 'templates/users.html'), checkLogin, adminUsersView);
page('/admin/users/add-user', pageLoader.bind(null, 'templates/add_user.html'), checkLogin, adminAddUserView);
page('/admin/upload-data', pageLoader.bind(null, 'templates/upload.html'), checkLogin, adminUploadDataView);
page('*', notfound);
page();

function showLoadingOverlay() {
    mainContent.LoadingOverlay('show', {
        image: '',
        color: 'black',
        fade: [0, 600],
        fontawesome: 'fa fa-spinner fa-pulse'
    });
}

function pageLoader(url, ctx, next) {
    loadTemplate(url).then(function (template) {
        ctx.template = $(template);
        next();
    });
}

function index(ctx) {
    mainContent.empty();
    mainContent.append(ctx.template);
    new WorklistController(ctx.template, globals.lastOpenUid, mainContent);

    ga('send', 'pageview', 'worklist');
}

function worklist(ctx) {
    mainContent.empty();
    mainContent.append(ctx.template);
    globals.username = ctx.params.username;
    new WorklistController(ctx.template, globals.lastOpenUid, mainContent);

    ga('send', 'pageview', 'worklist');
}

function login(ctx) {
    $('.logout-link').hide();
    mainContent.empty();
    mainContent.append(ctx.template);
    new LoginController().login(ctx.template);

    ga('send', 'pageview', 'login');
}

function resetCornerstone(ctx, next) {
    aidocViewer.tools.findingsScrollSynchronizer.destroy();
    aidocViewer.utils.referenceLines.updateImageSynchronizer.destroy();

    var enabledElements = cornerstone.getEnabledElements().slice(0);
    enabledElements.forEach(function (enabledElement) {
        cornerstone.disable(enabledElement.element);
    });

    aidocViewer.services.ScanService.reset();
    next();
}

function startTimeMeasurement(ctx, next) {
    aidocViewer.utils.timingUtils.start();
    next();
}

function showScan(ctx) {
    var uid = ctx.params.uid;
    globals.lastOpenUid = uid;
    mainContent.empty();
    mainContent.append(ctx.template);

    aidocViewer.services.ScanCache.preloadCache(globals.worklist, uid);

    new ScanController(uid, ctx.template, mainContent);

    ga('send', 'pageview', 'scan', {
        uid: uid
    });
}

function adminView(ctx, showSubView) {
    var user = aidocViewer.services.AuthService.user;

    if (user.role !== 'admin') {
        page.redirect('/');
    } else {
        mainContent.empty();
        mainContent.append(ctx.template);
         new AdminController().addSideBar(ctx.template);
        showSubView(ctx.template);

        ga('send', 'pageview', 'admin');
    }
}

function adminMetricsView(ctx) {
    adminView(ctx,new AdminController().showMetrics);
}

function adminUsersView(ctx) {
    adminView(ctx,new AdminController().showUsers);
}

function adminAddUserView(ctx) {
    adminView(ctx,new AdminController().addUser);
}

function adminUploadDataView(ctx) {
    adminView(ctx,new AdminController().uploadData);
}


function checkLogin(ctx, next) {
    if (!is_browser_supported()) {
        mainContent.empty();
        mainContent.append($('<div class="overlay overlay-text"><h1>Aidoc Validation Platform is only supported in' +
            ' <a overlay overlay-text href="https://www.google.com/chrome">Google Chrome</a></h1></div>'));
        return;
    }
    $('.logout-link').show();

    // if (ctx.state.user) {
    //     next();
    // }

    showLoadingOverlay();

    aidocViewer.services.AuthService.checkLogin()
        .then(function (user) {
            mainContent.LoadingOverlay('hide');
            ga('set', 'userId', user ? user.id : '');
            next();
        }, function (httpObj) {
            mainContent.LoadingOverlay('hide');

            if (httpObj.status === 401) {
                page.redirect('/login');
            }
        });
}

function is_browser_supported(){
    var isChrome = Boolean(window.chrome);

    return isChrome;
}


function logout(ctx) {
    globals.lastOpenUid = null;
    globals.lastChosenFilter = null;
    aidocViewer.services.ScanCache.clear();

    showLoadingOverlay();

    aidocViewer.services.AuthService.logout().complete(function () {
        mainContent.LoadingOverlay('hide');

        page.redirect('/login');
    });
}

function notfound() {
    mainContent.text('not found');
}

$(document).ajaxError(function (event, jqXHR, settings, thrownError) {
    if (jqXHR.status === 401) {
        aidocViewer.services.AuthService.user = null;
        page.redirect('/login');
    }
});

// Add generic error logging functions
window.addEventListener('error', function (e) {
    ga('send', 'exception', {
        exDescription: 'JavaScript Error ' + e.message + ' ' + e.filename + ': ' + e.lineno
    });
});

jQuery(document).ajaxError(function (e, request, settings, thrownError) {
    var message = 'Ajax Error ' + settings.url;

    if (e.result) {
        message += ' ' + e.result;
    }

    if (thrownError) {
        message += ': ' + thrownError;
    }

    ga('send', 'exception', {
        exDescription: message
    });
});

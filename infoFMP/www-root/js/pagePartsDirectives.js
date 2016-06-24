var pagePartsDirectives = angular.module('pagePartsDirectives', []);

pagePartsDirectives.directive('profileFields', ['languageService',
    'beforeAuthorizedOps', 'checkCreds', 'UserService', 'getLocale', 'getToken',
    'accountProfilePostProcess', '$uibModal', 'setActiveTab', 'getActiveTab',
    function profileFields(languageService, beforeAuthorizedOps, checkCreds,
        UserService, getLocale, getToken, accountProfilePostProcess, $uibModal,
        setActiveTab, getActiveTab) {
        return {
            restrict: 'A',
            templateUrl: 'partials/directives/profileFields.html',
            link: function (scope, el, attrs) {
                scope.lang = JSON.parse(languageService());
                
                scope.setTabActive = function(index){
                    setActiveTab(index);
                };
                //这里明明返回的是整数，却还要一个parseInt!! 搞了半天
                scope.active = parseInt(getActiveTab(), 10);
                
                scope.updateBasicProfile = function(){
                    var updateBasicProfileModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'partials/modals/updateBasicProfileModal.html',
                        controller: 'UpdateBasicProfileModalInstanceCtrl',
                        size: 'md',
                        resolve: {
                            lang: function () {
                                return scope.lang;
                            },
                            user: function(){
                                return scope.user;
                            }
                        }
                    });

                    updateBasicProfileModalInstance.result.then(
                        function () {
                            //nothing to do
                        },
                        function () {
                            //nothing to do
                        });
                };

                scope.changePassword = function () {
                    var updatePasswordModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'partials/modals/updatePasswordModal.html',
                        controller: 'UpdatePasswordModalInstanceCtrl',
                        size: 'md',
                        resolve: {
                            lang: function () {
                                return scope.lang;
                            }
                        }
                    });

                    updatePasswordModalInstance.result.then(
                        function () {
                            //nothing to do
                        },
                        function () {
                            //nothing to do
                        });
                };

                beforeAuthorizedOps();
                //scope.user = attrs.user;
                if (checkCreds()) {
                    scope.user = {};

                    var locale = scope.locale = getLocale();
                    var cred = getToken();

                    UserService.GetByCred(locale, cred).then(
                        function (res) {
                            if (res.success) {
                                scope.user = res.user;
                                scope.user.profile = res.profile;
                                accountProfilePostProcess(scope, res);
                            } else {
                            }
                        });
                }
            }
        };
    }]);

//注册表单共用部分的指令
pagePartsDirectives.directive('registerFormCommonParts', ['languageService',
    function (languageService) {
        return {
            restrict: 'A',
            templateUrl: 'partials/directives/registerCommonParts.html',
            link: function (scope, el, attrs) {
                scope.lang = JSON.parse(languageService());
            }
        };
    }]);

pagePartsDirectives.directive('publicMenu', ['getLocale', '$route',
    'checkCreds', 'deleteCreds', '$uibModal', '$rootScope',
    'tmhDynamicLocale', '$locale', 'getLocale', 'setLocale', 'languageService',
    function (getLocale, $route, checkCreds, deleteCreds, $uibModal,
        $rootScope, tmhDynamicLocale, $locale, getLocale, setLocale,
        languageService) {
        return {
            restrict: 'A',
            templateUrl: 'partials/directives/menu.html',
            link: function (scope, el, attrs) {

                scope.isLogin = checkCreds();

                scope.activeClass = JSON.parse(attrs.activeMenu);
                //这里有个坑！！！ JSON.parse is safer than eval, DO NOT USE eval()
                //scope.lang = eval(attrs.lang);
                scope.lang = JSON.parse(languageService());

                scope.languageList = [
                    {
                        'name': 'en-US, English',
                        'url': 'images/cn.png'
                    },
                    {
                        'name': 'en-US, English',
                        'url': 'images/us.png'
                    },
                    {
                        'name': 'fr-FR, français',
                        'url': 'images/fr.png'
                    },
                ];

                //设置cookie中语言的代码
                //也是作为指令模板中方法的原型演示
                scope.localeSelected = getLocale();

                scope.toConfirm = function () {
                    var logoutConfirmModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'confirmModal.html',
                        controller: 'LogoutConfirmModalInstanceCtrl',
                        size: 'sm',
                        resolve: {
                            lang: function () {
                                return scope.lang;
                            }
                        }
                    });

                    logoutConfirmModalInstance.result.then(
                        function () {
                            deleteCreds();
                            $route.reload();
                        },
                        function () {
                            //nothing to do
                        });
                };

                $rootScope.availableLocales = {
                    'en-us': 'English',
                    'zh-cn': '中  文'};
                $rootScope.$locale = $locale;
                tmhDynamicLocale.set(getLocale());
                $rootScope.model = {selectedLocale: getLocale()};
                scope.changeLocale = function (selectedLocale) {
                    //console.log(selectedLocale);                   
                    tmhDynamicLocale.set(selectedLocale);
                    //console.log($locale);
                    setLocale(selectedLocale);
                    $route.reload();
                };
            }
        };
    }]);

pagePartsDirectives.directive('mediaObject', function () {
    return {
        restrict: 'A',
        templateUrl: 'partials/directives/mediaobj.html',
        link: function (scope, el, attrs) {
            scope.media = JSON.parse(attrs.media);
        }
    };
});

pagePartsDirectives.directive('mediaList', function () {
    return {
        restrict: 'A',
        templateUrl: 'partials/directives/medialist.html',
        link: function (scope, el, attrs) {
            scope.items = JSON.parse(attrs.items);
            scope.lang = JSON.parse(attrs.lang);
        }
    };
});

pagePartsDirectives.directive('uploadComponent', function () {
    return {
        restrict: 'A',
        templateUrl: 'partials/directives/upload.html',
        link: function (scope, el, attrs) {
            scope.ui = JSON.parse(attrs.ui);
        }
    };
});
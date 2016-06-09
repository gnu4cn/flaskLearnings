var pagePartsDirectives = angular.module('pagePartsDirectives', []);

pagePartsDirectives.directive('profileAccordion', [
    function profileAccordion() {
        return {
            restrict: 'A',
            templateUrl: 'partials/directives/profileAccordion.html',
            link: function (scope, el, attrs) {
                scope.lang = JSON.parse(attrs.lang);
                scope.user = JSON.parse(attrs.user);
            }
        };
    }]);

//注册表单共用部分的指令
pagePartsDirectives.directive('registerFormCommonParts', [
    function(){
        return {
            restrict: 'A',
            templateUrl: 'partials/directives/registerCommonParts.html',
            link: function (scope, el, attrs) {
                scope.lang = JSON.parse(attrs.lang);
                
            }
        };
    }]);

pagePartsDirectives.directive('publicMenu', ['setLocale', 'getLocale', '$route',
    'checkCreds', 'deleteCreds', '$uibModal', 'setamMomentLocal',
    function (setLocale, getLocale, $route, checkCreds, deleteCreds, $uibModal, setamMomentLocal) {
        return {
            restrict: 'A',
            templateUrl: 'partials/directives/menu.html',
            link: function (scope, el, attrs) {

                scope.isLogin = checkCreds();

                scope.activeClass = JSON.parse(attrs.activeMenu);
                //这里有个坑！！！ JSON.parse is safer than eval, DO NOT USE eval()
                //scope.lang = eval(attrs.lang);
                scope.lang = JSON.parse(attrs.lang);

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

                scope.selectLocale = function () {
                    var locale = scope.localeSelected;
                    if (locale !== undefined) {
                        setLocale(locale);
                        setamMomentLocal(locale);
                        $route.reload();
                    }
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
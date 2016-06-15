'use strict';

var infoFMPControllers = angular.module('infoFMPControllers', []);

infoFMPControllers.controller('ProfileCtrl', ['$scope', 'getToken',
    'languageService', 'checkCreds', 'UserService', 'getLocale',
    'beforeAuthorizedOps',
    function ProfileCtrl($scope, getToken, languageService, checkCreds,
        UserService, getLocale, beforeAuthorizedOps) {

        $scope.currentMenu = {
            about: '',
            news: '',
            notices: '',
            profile: 'active',
            login: '',
            register: ''
        };
        $scope.lang = languageService();
        var userLocale = getLocale();
        var userCred = getToken();

        ////检查登录凭据是否过期
        beforeAuthorizedOps();
        
        //这里再度检查登录凭据，耗时一下午，尽然不需要business service的返回值，这么简单
        //就实现了。
        if (checkCreds()) {
            // 功能性代码开始
            //获取user_table数据
            UserService.GetByCred(userLocale, userCred).then(
                function (res) {
                    if (res.success) {
                        //console.log(res.user);
                        $scope.user = res.user;
                        $scope.user.created_at = new Date(res.user.created_at);
                    } else {
                    }
                });
        }

    }]);

infoFMPControllers.controller('CredInvalidModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'lang', 'message', '$sce',
    function ($scope, $uibModalInstance, lang, message, $sce) {
        //console.log(JSON.stringify(lang));
        $scope.message = $sce.trustAsHtml(message);
        $scope.lang = lang;
        $scope.ok = function () {
            $uibModalInstance.close(true);
        };
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };
    }]);

infoFMPControllers.controller('LogoutConfirmModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'lang', '$sce',
    function ($scope, $uibModalInstance, lang, $sce) {
        $scope.logoutTips = $sce.trustAsHtml(lang.logoutTips);
        $scope.lang = lang;
        $scope.ok = function () {
            $uibModalInstance.close(true);
        };
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };
    }]);

infoFMPControllers.controller('LoginCtrl', ['$scope', '$location',
    'languageService', 'UserService', '$timeout', '$q', 'getLocale', 'setCreds',
    function LoginCtrl($scope, $location, languageService, UserService,
        $timeout, $q, getLocale, setCreds) {
        $scope.currentMenu = {
            about: '',
            news: '',
            notices: '',
            profile: '',
            login: 'active',
            register: ''
        };

        $scope.lang = languageService();
        $scope.user = {};
        $scope.user.locale = getLocale();

        $scope.reset = function (form) {
            $scope.master = {};
            if (form) {
                form.$setPristine();
                form.$setUntouched();
            }
            $scope.user = angular.copy($scope.master);
            $scope.$broadcast('show-errors-reset');
            $scope.serverFault = false;
        };

        $scope.submitLogin = function () {
            var data = $scope.user;
            UserService.Login(data)
                .then(function (res) {
                    //发送请求成功
                    if (res.success) {
                        $scope.loginSuccess = true;
                        $scope.serverFault = false;
                        $scope.responseMsg = res.message;
                        setCreds(res.token);
                        var defer = $q.defer();
                        $timeout(function () {
                            $location.path('/');
                        }, 2000);
                        return defer.promise;
                    }
                    //发送请求失败
                    else {
                        $scope.responseMsg = res.message;
                        $scope.serverFault = true;
                    }
                });
        };
    }]);

infoFMPControllers.controller('RegisterStepOneCtrl', ['$scope', '$location',
    'languageService', 'PersonCategoryList', 'getLocale', 'setPersonCategory',
    function RegisterStepOneCtrl($scope, $location, languageService,
        PersonCategoryList, getLocale, setPersonCategory) {
        $scope.currentMenu = {
            about: '',
            news: '',
            notices: '',
            profile: '',
            login: '',
            register: 'active'
        };

        $scope.lang = languageService();

        var userLocale = getLocale();

        PersonCategoryList.get(
            {locale: userLocale},
            function success(response) {
                $scope.pCategories = response;
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            }
        );

        $scope.submitSelection = function () {
            var category_id = $scope.category.id;
            //console.log(category_id);
            if (category_id === undefined) {
                category_id = 6;
            }
            setPersonCategory(category_id);
            if (category_id < 5) {
                $location.path('/user/new-chinese-user');
            } else {
                $location.path('/user/new-foreign-user');
            }
        };
    }]);

infoFMPControllers.controller('NewForeignUserCtrl', ['$scope',
    'languageService', 'getLocale', 'getPersonCategory', 'UserService', '$q',
    '$timeout', '$location', 'GenderList',
    function ($scope, languageService, getLocale, getPersonCategory, UserService,
        $q, $timeout, $location, GenderList) {
        $scope.currentMenu = {
            about: '',
            news: '',
            notices: '',
            profile: '',
            login: '',
            register: 'active'
        };

        $scope.lang = languageService();

        $scope.user = {};
        var userLocale = $scope.user.locale = getLocale();

        GenderList.get(
            {locale: userLocale},
            function success(response) {
                $scope.Genders = response;
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            }
        );

        $scope.user.category = getPersonCategory();

        $scope.submitRegistration = function () {
            var data = $scope.user;

            UserService.Create(data)
                .then(function (res) {
                    //发送请求成功
                    if (res.success) {
                        $scope.registeredSuccess = true;
                        $scope.serverFault = false;
                        $scope.responseMsg = res.message;
                        var defer = $q.defer();
                        $timeout(function () {
                            $location.path('/user/login');
                        }, 3000);
                        return defer.promise;
                    }
                    //发送请求失败
                    else {
                        $scope.responseMsg = res.message;
                        $scope.registeredFail = true;
                        $scope.serverFault = true;
                    }
                });

        };
    }]);

infoFMPControllers.controller('NewChineseUserCtrl', ['$scope', 'languageService',
    'getLocale', 'getPersonCategory', 'UserService', '$q', '$timeout', '$location',
    function ($scope, languageService, getLocale, getPersonCategory,
        UserService, $q, $timeout, $location) {
        $scope.currentMenu = {
            about: '',
            news: '',
            notices: '',
            profile: '',
            login: '',
            register: 'active'
        };

        $scope.lang = languageService();

        $scope.user = {};
        $scope.user.locale = getLocale();

        $scope.user.category = getPersonCategory();

        $scope.submitRegistration = function () {
            var data = $scope.user;
            console.log(JSON.stringify(data));
            UserService.Create(data)
                .then(function (res) {
                    //发送请求成功
                    if (res.success) {
                        $scope.registeredSuccess = true;
                        $scope.serverFault = false;
                        $scope.responseMsg = res.message;
                        var defer = $q.defer();
                        $timeout(function () {
                            $location.path('/user/login');
                        }, 3000);
                        return defer.promise;
                    }
                    //发送请求失败
                    else {
                        $scope.responseMsg = res.message;
                        $scope.registeredFail = true;
                        $scope.serverFault = true;
                    }
                });
        };
    }]);

infoFMPControllers.controller('MainCtrl', ['$scope', 'languageService', 'checkCreds',
    function MainCtrl($scope, languageService) {
        $scope.currentMenu = {
            about: 'active',
            news: ' ',
            notices: ' ',
            profile: ' ',
            login: ' ',
            register: ' '
        };

        $scope.lang = languageService();

        $scope.media = {
            themeImg: 'media/logo.png',
            theme: 'about the FMP',
            title: '媒体标题，Media heading',
            content: "test： The former Microsoft executive excoriated by some industry \n\
watchers for the collapse of Nokia Mobile Phones, Stephen Elop, has re-emerged \n\
down under. Telstra says Elop is being appointed to the new role of Group \n\
Executive Technology, Innovation and Strategy, \"leading Telstra's strategy to \n\
become a world class technology company\" (stop giggling, you in the \n\
back row). Telstra cites Elop's \"deep technology experience\" and \"innate sense \n\
of customer expectations.\""
        };
        $scope.newNotice = '<p>Hello World!</p>';
    }]);
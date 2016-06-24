'use strict';

var Controllers = angular.module('Controllers', []);

Controllers.controller('ProfileCtrl', ['$scope',
    function ProfileCtrl($scope) {
        $scope.currentMenu = {
            about: '',
            news: '',
            notices: '',
            profile: 'active',
            login: '',
            register: ''
        };
    }]);

Controllers.controller('CredInvalidModalInstanceCtrl', ['$scope',
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

Controllers.controller('LogoutConfirmModalInstanceCtrl', ['$scope',
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

Controllers.controller('LoginCtrl', ['$scope', '$location',
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
            //console.log(JSON.stringify(data));
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

Controllers.controller('RegisterStepOneCtrl', ['$scope', '$location',
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

Controllers.controller('UpdateBasicProfileModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'lang', 'user', 'getToken', 'getLocale', 'UserService', '$location',
    'deleteCreds', '$q', '$timeout', 'GenderList', 'CountryList',
    function ($scope, $uibModalInstance, lang, user, getToken, getLocale,
        UserService, $location, deleteCreds, $q, $timeout, GenderList,
        CountryList) {
        $scope.lang = lang;
        //$scope.profile = user.profile;
        $scope.profile = {};

        //姓名及中文名字
        $scope.profile.firstName = user.profile.f_name;
        $scope.profile.lastName = user.profile.l_name;
        var userType = $scope.userType = parseInt(user.type, 10);
        
        if(userType<5){
            $scope.profile.idNumber = user.profile.id_number;
        }

        if (userType === 5) {
            $scope.profile.xingming = user.profile.xingming;
            //生日
            //http://stackoverflow.com/questions/17987647/moment-js-transform-to-date-object
            $scope.profile.birthday = user.profile.birthday.toDate();
            var today = new moment();
            $scope.minBirthday = today.subtract(60, 'years').toDate();

            //国内电话（外籍学员）
            $scope.zoneNumber = user.profile.country.zoneprefix;
            $scope.profile.home_number = user.profile.home_number;

            //家庭地址（外籍学员）
            $scope.profile.home_address = user.profile.home_address;
            $scope.country = user.profile.country.en_simp;
        }

        if (userType >= 5) {
            //性别
            var userLocale = getLocale();
            GenderList.get(
                {locale: userLocale},
                function success(response) {
                    $scope.Genders = response;
                    //下面的代码用于预置select选项
                    for (var i = 0; i < response.length; i++) {
                        if (response[i].id === user.profile.gender.id) {
                            $scope.profile.gender = response[i];
                            break;
                        }
                    }
                },
                function error(errorResponse) {
                    console.log(JSON.stringify(errorResponse));
                }
            );

            //国籍（参照性别）
            CountryList.get(
                {},
                function successs(response) {
                    $scope.countries = response;
                    for (var i = 0; i < response.length; i++) {
                        if (response[i].id === user.profile.country_id) {
                            $scope.countrySelected = response[i];
                            break;
                        }
                    }
                },
                function error(errorResponse) {
                    console.log(JSON.stringify(errorResponse));
                });

            //护照号码
            $scope.profile.passportNumber = user.profile.passport_number;
        }
    }]);

Controllers.controller('UpdatePasswordModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'lang', 'getToken', 'getLocale', 'UserService', '$location',
    'deleteCreds', '$q', '$timeout',
    function ($scope, $uibModalInstance, lang, getToken, getLocale,
        UserService, $location, deleteCreds, $q, $timeout) {
        $scope.lang = lang;
        $scope.ok = function () {
            $scope.data.cred = getToken();
            $scope.data.locale = getLocale();

            UserService.UpdatePassword($scope.data)
                .then(function (res) {
                    //发送请求成功
                    if (res.success) {
                        $scope.serverFault = false;
                        $scope.responseMsg = res.message;
                        if (res.updated) {
                            $scope.updatedSuccess = true;
                            $scope.oldPasswordIncorrect = false;
                            deleteCreds();
                            var defer = $q.defer();
                            $timeout(function () {
                                $location.path('/user/login');
                                $uibModalInstance.close(true);
                            }, 3000);
                            return defer.promise;
                        } else {
                            $scope.oldPasswordIncorrect = true;
                            $scope.updatedSuccess = false;
                            $scope.data.oldPassword = '';
                        }
                    }
                    //发送请求失败
                    else {
                        $scope.responseMsg = res.message;
                        $scope.serverFault = true;
                    }
                });
            //console.log(JSON.stringify($scope.data));

            //$uibModalInstance.close(true);
        };
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };
    }]);

Controllers.controller('ProfileExistedModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'lang', 'username',
    function ($scope, $uibModalInstance, lang, username) {
        //console.log(JSON.stringify(lang));
        $scope.username = username;
        $scope.lang = lang;
        $scope.ok = function () {
            $uibModalInstance.close(true);
        };
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };
    }]);

Controllers.controller('NewForeignUserCtrl', ['$scope',
    'languageService', 'getLocale', 'getPersonCategory', 'UserService', '$q',
    '$timeout', '$location', 'GenderList', 'CountryList',
    function ($scope, languageService, getLocale, getPersonCategory, UserService,
        $q, $timeout, $location, GenderList, CountryList) {
        $scope.currentMenu = {
            about: '',
            news: '',
            notices: '',
            profile: '',
            login: '',
            register: 'active'
        };

        $scope.lang = languageService();
        CountryList.get(
            {},
            function successs(response) {
                $scope.countries = response;
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            });

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
            $scope.user.countryId = $scope.countrySelected.id;
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

Controllers.controller('NewChineseUserCtrl', ['$scope', 'languageService',
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

Controllers.controller('MainCtrl', ['$scope', 'languageService',
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
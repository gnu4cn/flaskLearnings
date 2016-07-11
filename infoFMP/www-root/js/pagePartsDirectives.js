var pagePartsDirectives = angular.module('pagePartsDirectives', []);


pagePartsDirectives.directive('profileFields', ['languageService',
    'beforeAuthorizedOps', 'checkCreds', 'UserService', 'getLocale', 'getToken',
    'accountProfilePostProcess', '$uibModal', 'setActiveTab', 'getActiveTab',
    '$route',
    function profileFields(languageService, beforeAuthorizedOps, checkCreds,
        UserService, getLocale, getToken, accountProfilePostProcess, $uibModal,
        setActiveTab, getActiveTab, $route) {
        return {
            restrict: 'A',
            templateUrl: 'partials/directives/profileFields.html',
            link: function (scope, el, attrs) {
                scope.lang = JSON.parse(languageService());

                scope.setTabActive = function (index) {
                    setActiveTab(index);
                };
                //这里明明返回的是整数，却还要一个parseInt!! 搞了半天
                scope.active = parseInt(getActiveTab(), 10);                              

                scope.addPhoto = function () {
                    var uibModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'partials/modals/SingleImageProfileModal.html',
                        controller: 'SingleImageProfileModalInstanceCtrl',
                        size: 'md',
                        resolve: {
                            user: function () {
                                return scope.user;
                            }
                        }
                    });

                    uibModalInstance.result.then(
                        function () {
                            $route.reload();
                        },
                        function () {
                            //nothing to do
                        });
                };
                
                scope.changePhoto = scope.addPhoto;

                scope.updateBasicProfileStaff = function () {
                    var uibModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'partials/modals/BasicProfileStaffModal.html',
                        controller: 'BasicProfileStaffModalInstanceCtrl',
                        size: 'md',
                        resolve: {
                            user: function () {
                                return scope.user;
                            }
                        }
                    });

                    uibModalInstance.result.then(
                        function () {
                            $route.reload();
                        },
                        function () {
                            //nothing to do
                        });
                };

                scope.updateBasicProfileStaffFamily = function () {
                    var uibModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'partials/modals/BasicProfileStaffFamilyModal.html',
                        controller: 'BasicProfileStaffFamilyModalInstanceCtrl',
                        size: 'md',
                        resolve: {
                            lang: function () {
                                return scope.lang;
                            },
                            user: function () {
                                return scope.user;
                            }
                        }
                    });

                    uibModalInstance.result.then(
                        function () {
                            $route.reload();
                        },
                        function () {
                            //nothing to do
                        });
                };

                scope.updateBasicProfileTrainee = function () {
                    var uibModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'partials/modals/BasicProfileTraineeModal.html',
                        controller: 'BasicProfileTraineeModalInstanceCtrl',
                        size: 'md',
                        resolve: {
                            lang: function () {
                                return scope.lang;
                            },
                            user: function () {
                                return scope.user;
                            }
                        }
                    });

                    uibModalInstance.result.then(
                        function () {
                            $route.reload();
                        },
                        function () {
                            //nothing to do
                        });
                };

                scope.updateBasicProfileTraineeFamily = function () {
                    var uibModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'partials/modals/BasicProfileTraineeFamilyModal.html',
                        controller: 'BasicProfileTraineeFamilyModalInstanceCtrl',
                        size: 'md',
                        resolve: {
                            lang: function () {
                                return scope.lang;
                            },
                            user: function () {
                                return scope.user;
                            }
                        }
                    });

                    uibModalInstance.result.then(
                        function () {
                            $route.reload();
                        },
                        function () {
                            //nothing to do
                        });
                };

                scope.updatePassportVISATrainee = function () {
                    var uibModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'partials/modals/PassportVISATraineeModal.html',
                        controller: 'PassportVISATraineeModalInstanceCtrl',
                        size: 'md',
                        resolve: {
                            lang: function () {
                                return scope.lang;
                            },
                            user: function () {
                                return scope.user;
                            }
                        }
                    });

                    uibModalInstance.result.then(
                        function () {
                            $route.reload();
                        },
                        function () {
                            //nothing to do
                        });
                };

                scope.updatePassportVISATraineeFamily = function () {
                    var uibModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'partials/modals/PassportVISATraineeFamilyModal.html',
                        controller: 'PassportVISATraineeFamilyModalInstanceCtrl',
                        size: 'md',
                        resolve: {
                            lang: function () {
                                return scope.lang;
                            },
                            user: function () {
                                return scope.user;
                            }
                        }
                    });

                    uibModalInstance.result.then(
                        function () {
                            $route.reload();
                        },
                        function () {
                            //nothing to do
                        });
                };

                scope.addStaffFamily = function () {
                    var uibModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'partials/modals/StaffFamilyModal.html',
                        controller: 'StaffFamilyModalInstanceCtrl',
                        size: 'md',
                        resolve: {
                            user: function () {
                                return scope.user;
                            }
                        }
                    });

                    uibModalInstance.result.then(
                        function () {
                            $route.reload();
                        },
                        function () {
                            //nothing to do
                        });
                };

                scope.addTraineeFamily = function () {
                    var uibModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'partials/modals/TraineeFamilyModal.html',
                        controller: 'TraineeFamilyModalInstanceCtrl',
                        size: 'md',
                        resolve: {
                            user: function () {
                                return scope.user;
                            }
                        }
                    });

                    uibModalInstance.result.then(
                        function () {
                            $route.reload();
                        },
                        function () {
                            //nothing to do
                        });
                };

                scope.changePassword = function () {
                    var uibModalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: 'partials/modals/PasswordModal.html',
                        controller: 'PasswordModalInstanceCtrl',
                        size: 'sm'
                    });

                    uibModalInstance.result.then(
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
                            //console.log(JSON.stringify(res));
                            if (res.success) {
                                scope.user = res.user;
                                scope.user.profile = res.profile;
                                //console.log(JSON.stringify(scope.user));
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

pagePartsDirectives.directive('addFamilyFormCommonParts', ['languageService',
    function (languageService) {
        return {
            restrict: 'A',
            templateUrl: 'partials/directives/addFamilyFormCommonParts.html',
            link: function (scope, el, attrs) {
                scope.lang = JSON.parse(languageService());
            }
        };
    }]);

pagePartsDirectives.directive('publicMenu', ['getLocale', '$route',
    'checkCreds', 'deleteCreds', '$uibModal', '$rootScope',
    'tmhDynamicLocale', '$locale', 'getLocale', 'setLocale', 'languageService',
    'setActiveTab', 'forgetVISANumber',
    function (getLocale, $route, checkCreds, deleteCreds, $uibModal,
        $rootScope, tmhDynamicLocale, $locale, getLocale, setLocale,
        languageService, setActiveTab, forgetVISANumber) {
        return {
            restrict: 'A',
            templateUrl: 'partials/directives/menu.html',
            link: function (scope, el, attrs) {

                scope.isLogin = checkCreds();

                scope.activeClass = JSON.parse(attrs.activeMenu);
                //这里有个坑！！！ JSON.parse is safer than eval, DO NOT USE eval()
                //scope.lang = eval(attrs.lang);
                scope.lang = JSON.parse(languageService());

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
                            setActiveTab(0);
                            deleteCreds();
                            forgetVISANumber();
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

// 这是用于显示上传图片预览的。
pagePartsDirectives.directive('ngThumb', ['$window', function ($window) {
        var helper = {
            support: !!($window.FileReader && $window.CanvasRenderingContext2D),
            isFile: function (item) {
                return angular.isObject(item) && item instanceof $window.File;
            },
            isImage: function (file) {
                var type = '|' + file.type.slice(file.type.lastIndexOf('/') + 1) + '|';
                return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
            }
        };

        return {
            restrict: 'A',
            template: '<canvas/>',
            link: function (scope, element, attributes) {
                if (!helper.support)
                    return;

                var params = scope.$eval(attributes.ngThumb);

                if (!helper.isFile(params.file))
                    return;
                if (!helper.isImage(params.file))
                    return;

                var canvas = element.find('canvas');
                var reader = new FileReader();

                reader.onload = onLoadFile;
                reader.readAsDataURL(params.file);

                function onLoadFile(event) {
                    var img = new Image();
                    img.onload = onLoadImage;
                    img.src = event.target.result;
                }

                function onLoadImage() {
                    var width = params.width || this.width / this.height * params.height;
                    var height = params.height || this.height / this.width * params.width;
                    canvas.attr({width: width, height: height});
                    canvas[0].getContext('2d').drawImage(this, 0, 0, width, height);
                }
            }
        };
    }]);
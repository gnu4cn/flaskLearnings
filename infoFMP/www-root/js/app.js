'use strict';

var infoFMP = angular.module('infoFMP', [
    'ngRoute',
    'infoFMPControllers',
    'services',
    'formTypesDirectives',
    'pagePartsDirectives',
    'ui.bootstrap',
    'textAngular',
    'angularFileUpload',
    'bussinessServices',
    'ui.bootstrap.showErrors',
    'angularMoment',
    'languageService',
    'ngMaterial',
    'tmh.dynamicLocale'
]);

//infoFMP.run(['getLocale', 'amMoment',
//    function(getLocale, amMoment){
//        amMoment.changeLocale(getLocale());
//    }]);

infoFMP.config(['$routeProvider', '$locationProvider', '$provide', 'showErrorsConfigProvider', 
    'tmhDynamicLocaleProvider',
    function ($routeProvider, $locationProvider, $provide, showErrorsConfigProvider, 
    tmhDynamicLocaleProvider) {
        //angular-dynamic-locale
        tmhDynamicLocaleProvider.localeLocationPattern('js/libs/angular-locale_{{locale}}.js');
        //angular-showerrors
        showErrorsConfigProvider.showSuccess(true);
        // routes
        $routeProvider
            .when('/', {
                templateUrl: 'partials/main.html',
                controller: 'MainCtrl'
            })
            .when('/user/register-step-1', {
                templateUrl: 'partials/register-step-1.html',
                controller: 'RegisterStepOneCtrl'
            })
            .when('/user/login', {
                templateUrl: 'partials/login.html',
                controller: 'LoginCtrl'
            })
            .when('/user/new-chinese-user', {
                templateUrl: 'partials/newChineseUser.html',
                controller: 'NewChineseUserCtrl'
            })
            .when('/user/new-foreign-user', {
                templateUrl: 'partials/newForeignUser.html',
                controller: 'NewForeignUserCtrl'
            })
            .when('/user/profile', {
                templateUrl: 'partials/profile.html',
                controller: 'ProfileCtrl'
            });
        $locationProvider.html5Mode(false).hashPrefix('!');

        //注意这里注入的依赖是 $uibModal
        $provide.decorator('taOptions', ['taRegisterTool', '$delegate', '$uibModal',
            function (taRegisterTool, taOptions, $uibModal) {
                taOptions.forceTextAngularSanitize = true;
                taOptions.keyMappings = [];
                taOptions.toolbar = [
                    ['h1', 'h2', 'h3', 'p', 'pre', 'quote'],
                    ['bold', 'italics', 'underline', 'ul', 'ol', 'redo', 'undo', 'clear'],
                    ['justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull'],
                    ['html', 'customInsertImage', 'insertCarousel', 'insertLink']
                ];

                taRegisterTool('colorGreen', {
                    iconclass: "fa fa-square green",
                    action: function () {
                        this.$editor().wrapSelection('forecolor', 'green');
                    }
                });

                taRegisterTool('customInsertImage', {
                    iconclass: "fa fa-image",
                    action: function (deferred, restoreSelection) {
                        $uibModal.open({
                            animation: true,
                            size: 'lg',
                            controller: 'InsertImageModalInstance',
                            templateUrl: 'partials/modals/insertimage.html'
                        }).result.then(
                            function (result) {
                                restoreSelection();
                                // document.execCommand 是标准化的，
                                // http://quirksmode.org/dom/execCommand.html
                                document.execCommand('insertImage', true, result);
                                deferred.resolve();
                            },
                            function () {
                                deferred.resolve();
                            }
                        );
                        return false;
                    }
                });

                taRegisterTool('insertCarousel', {
                    buttontext: '插入幻灯片',
                    iconclass: "fa fa-film",
                    action: function (deferred, restoreSelection) {
                        $uibModal.open({
                            controller: 'InsertCarouselModalInstance',
                            templateUrl: 'partials/modals/insertcarousel.html'
                        }).result.then(
                            function (result) {
                                restoreSelection();
                                document.execCommand('insertHTML', true, result);
                                deferred.resolve();
                            },
                            function () {
                                deferred.resolve();
                            }
                        );
                        return false;
                    }
                });

                taOptions.toolbar[0].push('colorGreen');
                return taOptions; // whatever you return will be the taOptions
            }]);
    }]);


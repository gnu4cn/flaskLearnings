'use strict';

var formTypesDirectives = angular.module('formTypesDirectives', []);

formTypesDirectives.directive('typeChineseName', [
    function typeFirstname() {
        var NAME_REGEX = /^([\u4e00-\u9fa5])[\u4e00-\u9fa5]{1,3}$/;
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    return ctrl.$isEmpty(modelValue) || NAME_REGEX.test(viewValue);
                };
            }
        };

    }]);

formTypesDirectives.directive('typeFirstname', [
    function typeFirstname() {
        var NAME_REGEX = /^([A-Z\u4e00-\u9fa5])[ÆÐƎƏƐƔĲŊŒẞÞǷȜæðǝəɛɣĳŋœĸſßþƿȝĄƁÇĐƊĘĦĮƘŁØƠŞȘŢȚŦŲƯY̨Ƴąɓçđɗęħįƙłøơşșţțŧųưy̨ƴÁÀÂÄǍĂĀÃÅǺĄÆǼǢƁĆĊĈČÇĎḌĐƊÐÉÈĖÊËĚĔĒĘẸƎƏƐĠĜǦĞĢƔáàâäǎăāãåǻąæǽǣɓćċĉčçďḍđɗðéèėêëěĕēęẹǝəɛġĝǧğģɣĤḤĦIÍÌİÎÏǏĬĪĨĮỊĲĴĶƘĹĻŁĽĿʼNŃN̈ŇÑŅŊÓÒÔÖǑŎŌÕŐỌØǾƠŒĥḥħıíìiîïǐĭīĩįịĳĵķƙĸĺļłľŀŉńn̈ňñņŋóòôöǒŏōõőọøǿơœŔŘŖŚŜŠŞȘṢẞŤŢṬŦÞÚÙÛÜǓŬŪŨŰŮŲỤƯẂẀŴẄǷÝỲŶŸȲỸƳŹŻŽẒŕřŗſśŝšşșṣßťţṭŧþúùûüǔŭūũűůųụưẃẁŵẅƿýỳŷÿȳỹƴźżžẓa-zA-Z .\u4e00-\u9fa5]{0,}$/;
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    return ctrl.$isEmpty(modelValue) || NAME_REGEX.test(viewValue);
                };
            }
        };

    }]);

formTypesDirectives.directive('typeLastname', [
    function typeLastname() {
        var NAME_REGEX = /^([A-Z\u4e00-\u9fa5])[ÆÐƎƏƐƔĲŊŒẞÞǷȜæðǝəɛɣĳŋœĸſßþƿȝĄƁÇĐƊĘĦĮƘŁØƠŞȘŢȚŦŲƯY̨Ƴąɓçđɗęħįƙłøơşșţțŧųưy̨ƴÁÀÂÄǍĂĀÃÅǺĄÆǼǢƁĆĊĈČÇĎḌĐƊÐÉÈĖÊËĚĔĒĘẸƎƏƐĠĜǦĞĢƔáàâäǎăāãåǻąæǽǣɓćċĉčçďḍđɗðéèėêëěĕēęẹǝəɛġĝǧğģɣĤḤĦIÍÌİÎÏǏĬĪĨĮỊĲĴĶƘĹĻŁĽĿʼNŃN̈ŇÑŅŊÓÒÔÖǑŎŌÕŐỌØǾƠŒĥḥħıíìiîïǐĭīĩįịĳĵķƙĸĺļłľŀŉńn̈ňñņŋóòôöǒŏōõőọøǿơœŔŘŖŚŜŠŞȘṢẞŤŢṬŦÞÚÙÛÜǓŬŪŨŰŮŲỤƯẂẀŴẄǷÝỲŶŸȲỸƳŹŻŽẒŕřŗſśŝšşșṣßťţṭŧþúùûüǔŭūũűůųụưẃẁŵẅƿýỳŷÿȳỹƴźżžẓa-zA-Z .\u4e00-\u9fa5]{0,}$/;
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    return ctrl.$isEmpty(modelValue) || NAME_REGEX.test(viewValue);
                };
            }
        };

    }]);

// 身份证好验证代码(不再检查是否已存在)
formTypesDirectives.directive('typeIdNumberUpdate', ['checkIDCardNumber',
    function (checkIDCardNumber) {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    return ctrl.$isEmpty(modelValue) || checkIDCardNumber(viewValue);
                };
            }
        };
    }]);

// 身份证好验证代码
formTypesDirectives.directive('typeIdNumber', ['checkIDCardNumber', 'ProfileService',
    'getPersonCategory', '$uibModal', '$location', '$parse', '$q', '$timeout',
    'languageService',
    function (checkIDCardNumber, ProfileService, getPersonCategory, $uibModal,
        $location, $parse, $q, $timeout, languageService) {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    return ctrl.$isEmpty(modelValue) || checkIDCardNumber(viewValue);
                };
                ctrl.$asyncValidators.isExisted = function (modelValue, viewValue) {
                    var data = {};
                    data.idNumber = modelValue || viewValue;
                    data.category = getPersonCategory();
                    var lang = languageService();
                    return ProfileService.CheckIDNumber(data)
                        .then(function (res) {
                            if (res.success) {
                                if (!res.existed) {
                                    //不存在时， 设置该表单字段有效
                                    var defer = $q.defer();
                                    $timeout(
                                        function () {
                                            ctrl.$setValidity('isExisted', !res.existed);
                                            $parse(attrs.ngModel).assign(scope, ctrl.$viewValue);
                                            //$parse(attrs.ngModel).assign(scope, ctrl.$viewValue.split(','));
                                        }, 1000);
                                    return defer.promise;
                                } else {
                                    //存在时，设置该表单字段无效，并弹出一个提示对话框
                                    var defer = $q.defer();
                                    $timeout(
                                        function () {
                                            ctrl.$setValidity('isExisted', !res.existed);
                                            var ProfileExistedModalInstance = $uibModal.open({
                                                animation: true,
                                                templateUrl: '/partials/modals/profileexistedIDNumber.html',
                                                controller: 'ProfileExistedModalInstanceCtrl',
                                                size: 'md',
                                                resolve: {
                                                    lang: function () {
                                                        return JSON.parse(lang);
                                                    },
                                                    username: function () {
                                                        return res.username;
                                                    }
                                                }
                                            });

                                            ProfileExistedModalInstance.result.then(
                                                function () {
                                                    $location.path('/user/login');
                                                },
                                                function () {

                                                });
                                        }, 50);
                                    return defer = $q.defer();
                                }
                            } else {
                                alert(res.message);
                            }
                        });
                };
            }
        };
    }]);

formTypesDirectives.directive('typeMobile', [function () {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    var MOBILE_REGEX = /(^(13\d|15[^4,\D]|17[13678]|18\d)\d{8}|170[^346,\D]\d{7})$/;
                    return ctrl.$isEmpty(modelValue) || MOBILE_REGEX.test(viewValue);
                };
            }
        };
    }]);

formTypesDirectives.directive('typeHomeNumber', [function () {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    var HOME_NUMBER_REGEX = /^[a-zA-Z0-9\-().\s]{6,15}$/;
                    return ctrl.$isEmpty(modelValue) || HOME_NUMBER_REGEX.test(viewValue);
                };
            }
        };
    }]);

formTypesDirectives.directive('typeHomeAddress', [function () {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    var HOME_ADDRESS_REGEX = /^([ÆÐƎƏƐƔĲŊŒẞÞǷȜæðǝəɛɣĳŋœĸſßþƿȝĄƁÇĐƊĘĦĮƘŁØƠŞȘŢȚŦŲƯY̨Ƴąɓçđɗęħįƙłøơşșţțŧųưy̨ƴÁÀÂÄǍĂĀÃÅǺĄÆǼǢƁĆĊĈČÇĎḌĐƊÐÉÈĖÊËĚĔĒĘẸƎƏƐĠĜǦĞĢƔáàâäǎăāãåǻąæǽǣɓćċĉčçďḍđɗðéèėêëěĕēęẹǝəɛġĝǧğģɣĤḤĦIÍÌİÎÏǏĬĪĨĮỊĲĴĶƘĹĻŁĽĿʼNŃN̈ŇÑŅŊÓÒÔÖǑŎŌÕŐỌØǾƠŒĥḥħıíìiîïǐĭīĩįịĳĵķƙĸĺļłľŀŉńn̈ňñņŋóòôöǒŏōõőọøǿơœŔŘŖŚŜŠŞȘṢẞŤŢṬŦÞÚÙÛÜǓŬŪŨŰŮŲỤƯẂẀŴẄǷÝỲŶŸȲỸƳŹŻŽẒŕřŗſśŝšşșṣßťţṭŧþúùûüǔŭūũűůųụưẃẁŵẅƿýỳŷÿȳỹƴźżžẓA-Za-z\u4e00-\u9fa5])[ÆÐƎƏƐƔĲŊŒẞÞǷȜæðǝəɛɣĳŋœĸſßþƿȝĄƁÇĐƊĘĦĮƘŁØƠŞȘŢȚŦŲƯY̨Ƴąɓçđɗęħįƙłøơşșţțŧųưy̨ƴÁÀÂÄǍĂĀÃÅǺĄÆǼǢƁĆĊĈČÇĎḌĐƊÐÉÈĖÊËĚĔĒĘẸƎƏƐĠĜǦĞĢƔáàâäǎăāãåǻąæǽǣɓćċĉčçďḍđɗðéèėêëěĕēęẹǝəɛġĝǧğģɣĤḤĦIÍÌİÎÏǏĬĪĨĮỊĲĴĶƘĹĻŁĽĿʼNŃN̈ŇÑŅŊÓÒÔÖǑŎŌÕŐỌØǾƠŒĥḥħıíìiîïǐĭīĩįịĳĵķƙĸĺļłľŀŉńn̈ňñņŋóòôöǒŏōõőọøǿơœŔŘŖŚŜŠŞȘṢẞŤŢṬŦÞÚÙÛÜǓŬŪŨŰŮŲỤƯẂẀŴẄǷÝỲŶŸȲỸƳŹŻŽẒŕřŗſśŝšşșṣßťţṭŧþúùûüǔŭūũűůųụưẃẁŵẅƿýỳŷÿȳỹƴźżžẓa-zA-Z #,.\u4e00-\u9fa5]{10,}$/;
                    return ctrl.$isEmpty(modelValue) || HOME_ADDRESS_REGEX.test(viewValue);
                };
            }
        };
    }]);

//这里就仅对护照号码规则进行检查，不再检查是否已注册了。
//暂行这样处理，待后续进一步在viewValue与modelValue不一致时，在与数据库进行比对，给出提示
//信息。
formTypesDirectives.directive('typePassportNumberUpdate', ['checkPassportNumber',
    function (checkPassportNumber) {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    return ctrl.$isEmpty(modelValue) || checkPassportNumber(viewValue);
                };
            }
        };
    }]);

formTypesDirectives.directive('typePassportNumber', ['checkPassportNumber',
    'ProfileService', '$q', '$timeout', '$location', '$parse', '$uibModal',
    'getPersonCategory', 'languageService',
    function (checkPassportNumber, ProfileService, $q, $timeout, $location,
        $parse, $uibModal, getPersonCategory, languageService) {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    return ctrl.$isEmpty(modelValue) || checkPassportNumber(viewValue);
                };
                ctrl.$asyncValidators.isExisted = function (modelValue, viewValue) {
                    var data = {};
                    data.passportNumber = modelValue || viewValue;
                    data.category = getPersonCategory();
                    var lang = languageService();
                    return ProfileService.CheckIDNumber(data)
                        .then(function (res) {
                            if (res.success) {

                                if (!res.existed) {
                                    //不存在时， 设置该表单字段有效
                                    var defer = $q.defer();
                                    $timeout(
                                        function () {
                                            ctrl.$setValidity('isExisted', !res.existed);
                                            $parse(attrs.ngModel).assign(scope, ctrl.$viewValue);
                                            //$parse(attrs.ngModel).assign(scope, ctrl.$viewValue.split(','));
                                        }, 1000);
                                    return defer.promise;
                                } else {
                                    //存在时，设置该表单字段无效，并弹出一个提示对话框
                                    var defer = $q.defer();
                                    $timeout(
                                        function () {
                                            ctrl.$setValidity('isExisted', !res.existed);
                                            var ProfileExistedModalInstance = $uibModal.open({
                                                animation: true,
                                                templateUrl: '/partials/modals/profileexistedPassportNumber.html',
                                                controller: 'ProfileExistedModalInstanceCtrl',
                                                size: 'md',
                                                resolve: {
                                                    lang: function () {
                                                        return JSON.parse(lang);
                                                    },
                                                    username: function () {
                                                        return res.username;
                                                    }
                                                }
                                            });

                                            ProfileExistedModalInstance.result.then(
                                                function () {
                                                    $location.path('/user/login');
                                                },
                                                function () {

                                                });
                                        }, 50);
                                    return defer = $q.defer();
                                }
                            } else {
                                alert(res.message);
                            }
                        });
                };
            }
        };
    }]);

//input 类型的指令
formTypesDirectives.directive('typeUsername', ['$q', 'UserService', '$timeout',
    '$parse',
    function ($q, UserService, $timeout, $parse) {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    var USERNAME_REGEXP = /^[a-zA-Z0-9]+$/;
                    return ctrl.$isEmpty(modelValue) || USERNAME_REGEXP.test(viewValue);
                };
                ctrl.$asyncValidators.isExisted = function (modelValue, viewValue) {
                    var value = modelValue || viewValue;
                    return UserService.CheckUsername(value)
                        .then(function (res) {
                            if (res.success) {
                                var defer = $q.defer();
                                $timeout(
                                    function () {
                                        ctrl.$setValidity('isExisted', !res.exists);
                                        $parse(attrs.ngModel).assign(scope, ctrl.$viewValue);
                                        //$parse(attrs.ngModel).assign(scope, ctrl.$viewValue.split(','));
                                    }, 1000);
                                return defer.promise;
                            } else {
                                alert(res.message);
                            }
                        });
                };
            }
        };
    }]);


formTypesDirectives.directive('typePassword', function () {
    var PASSWORD_REGEXP = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/;
    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {
            ctrl.$validators.typePassword = function (modelValue, viewValue) {
                return ctrl.$isEmpty(modelValue) || PASSWORD_REGEXP.test(viewValue);
            };
        }
    };
});

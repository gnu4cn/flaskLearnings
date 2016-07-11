'use strict';

var formTypesDirectives = angular.module('formTypesDirectives', []);

var TRAINEE_FAMILY_CAT = '6';
var STAFF_FAMILY_CAT = '1';

formTypesDirectives.directive('typeVisaNumber', [
    function () {
        var VISA_REGEX = /^([0HIJGC])[0-9]{7,}$/;
        var NULL_REGEX = /^(\u65E0\/Null)$/;
        var RESIDENT_CERT_REGEX_JS = /^(JS)(\()([1-2])[0-9](\))[0-9]{2,}$/;
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    return ctrl.$isEmpty(modelValue) || VISA_REGEX.test(viewValue) || NULL_REGEX.test(viewValue) || RESIDENT_CERT_REGEX_JS.test(viewValue);
                };
            }
        };
    }]);

formTypesDirectives.directive('typeFlightNumber', [
    function () {
        //http://academe.co.uk/2014/01/validating-flight-codes/
        var FLIGHT_NUMBER_REGEX = /^([a-z][a-z]|[a-z][0-9]|[0-9][a-z])[a-z]?[0-9]{1,4}[a-z]?$/i;
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    return ctrl.$isEmpty(modelValue) || FLIGHT_NUMBER_REGEX.test(viewValue);
                };
            }
        };
    }]);

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

// 身份证号码验证 -- 添加校内家属时
formTypesDirectives.directive('typeIdNumberFamily', ['checkIDCardNumber',
    'ProfileService', 'getToken', '$parse', '$q', '$timeout',
    function (checkIDCardNumber, ProfileService, getToken, $parse, $q, $timeout) {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {
                ctrl.$validators.format = function (modelValue, viewValue) {
                    return ctrl.$isEmpty(modelValue) || checkIDCardNumber(viewValue);
                };
                //这里使用了$asyncValidators，就需要一个promise
                ctrl.$asyncValidators.isExisted = function (modelValue, viewValue) {
                    var data = {};
                    data.idNumber = modelValue || viewValue;
                    data.category = STAFF_FAMILY_CAT;
                    data.cred = getToken();

                    //console.log(JSON.stringify(data));
                    // 异步验证器是需要返回promise的。
                    var deferred = $q.defer();
                    //这里加入一个等待，目的是现实pending消息。
                    $timeout(function () {
                        ProfileService.CheckProfile(data)
                            .then(function (res) {
                                if (res.success) {
                                    if (res.appended) {
                                        ctrl.$setValidity('isExisted', false);
                                    } else {
                                        ctrl.$setValidity('isExisted', true);
                                        $parse(attrs.ngModel).assign(scope, ctrl.$viewValue);
                                    }
                                } else {
                                    alert(res.message);
                                }
                            });
                    }, 1000);
                    return deferred.promise;
                };
            }
        };
    }]);

// 身份证号码验证， 这个是很复杂的了
formTypesDirectives.directive('typeIdNumberRegister', ['checkIDCardNumber',
    'ProfileService', '$parse', '$uibModal', '$location', '$q', 'getPersonCategory',
    '$timeout',
    function (checkIDCardNumber, ProfileService, $parse, $uibModal, $location,
        $q, getPersonCategory, $timeout) {
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

                    //console.log(JSON.stringify(data));

                    // 异步验证器是需要返回promise的。
                    var deferred = $q.defer();
                    //加入$timeout, 已显示pending消息。
                    $timeout(function () {
                        ProfileService.CheckProfile(data)
                            .then(function (res) {
                                if (res.success) {
                                    if (res.registered) {
                                        ctrl.$setValidity('isExisted', false);
                                        //弹出一个对话框
                                        var ModalInstance = $uibModal.open({
                                            animation: true,
                                            templateUrl: '/partials/modals/ProfileexistedIDNumber.html',
                                            controller: 'ProfileExistedModalInstanceCtrl',
                                            size: 'md',
                                            resolve: {
                                                username: function () {
                                                    return res.username;
                                                }
                                            }
                                        });

                                        ModalInstance.result.then(
                                            function () {
                                                $location.path('/user/login');
                                            },
                                            function () {

                                            });
                                    } else {
                                        ctrl.$setValidity('isExisted', true);
                                        $parse(attrs.ngModel).assign(scope, ctrl.$viewValue);
                                    }
                                } else {
                                    alert(res.message);
                                }
                            });
                    }, 1000);
                    return deferred.promise;
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
                    var HOME_ADDRESS_REGEX = /^([#ÆÐƎƏƐƔĲŊŒẞÞǷȜæðǝəɛɣĳŋœĸſßþƿȝĄƁÇĐƊĘĦĮƘŁØƠŞȘŢȚŦŲƯY̨Ƴąɓçđɗęħįƙłøơşșţțŧųưy̨ƴÁÀÂÄǍĂĀÃÅǺĄÆǼǢƁĆĊĈČÇĎḌĐƊÐÉÈĖÊËĚĔĒĘẸƎƏƐĠĜǦĞĢƔáàâäǎăāãåǻąæǽǣɓćċĉčçďḍđɗðéèėêëěĕēęẹǝəɛġĝǧğģɣĤḤĦIÍÌİÎÏǏĬĪĨĮỊĲĴĶƘĹĻŁĽĿʼNŃN̈ŇÑŅŊÓÒÔÖǑŎŌÕŐỌØǾƠŒĥḥħıíìiîïǐĭīĩįịĳĵķƙĸĺļłľŀŉńn̈ňñņŋóòôöǒŏōõőọøǿơœŔŘŖŚŜŠŞȘṢẞŤŢṬŦÞÚÙÛÜǓŬŪŨŰŮŲỤƯẂẀŴẄǷÝỲŶŸȲỸƳŹŻŽẒŕřŗſśŝšşșṣßťţṭŧþúùûüǔŭūũűůųụưẃẁŵẅƿýỳŷÿȳỹƴźżžẓA-Za-z\u4e00-\u9fa5])[,.，。0-9ÆÐƎƏƐƔĲŊŒẞÞǷȜæðǝəɛɣĳŋœĸſßþƿȝĄƁÇĐƊĘĦĮƘŁØƠŞȘŢȚŦŲƯY̨Ƴąɓçđɗęħįƙłøơşșţțŧųưy̨ƴÁÀÂÄǍĂĀÃÅǺĄÆǼǢƁĆĊĈČÇĎḌĐƊÐÉÈĖÊËĚĔĒĘẸƎƏƐĠĜǦĞĢƔáàâäǎăāãåǻąæǽǣɓćċĉčçďḍđɗðéèėêëěĕēęẹǝəɛġĝǧğģɣĤḤĦIÍÌİÎÏǏĬĪĨĮỊĲĴĶƘĹĻŁĽĿʼNŃN̈ŇÑŅŊÓÒÔÖǑŎŌÕŐỌØǾƠŒĥḥħıíìiîïǐĭīĩįịĳĵķƙĸĺļłľŀŉńn̈ňñņŋóòôöǒŏōõőọøǿơœŔŘŖŚŜŠŞȘṢẞŤŢṬŦÞÚÙÛÜǓŬŪŨŰŮŲỤƯẂẀŴẄǷÝỲŶŸȲỸƳŹŻŽẒŕřŗſśŝšşșṣßťţṭŧþúùûüǔŭūũűůųụưẃẁŵẅƿýỳŷÿȳỹƴźżžẓa-zA-Z #,.\u4e00-\u9fa5]{8,}$/;
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

formTypesDirectives.directive('typePassportNumberFamily', ['checkPassportNumber',
    'ProfileService', '$q', '$timeout', '$parse', 'getToken',
    function (checkPassportNumber, ProfileService, $q, $timeout, $parse, getToken) {
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
                    data.category = TRAINEE_FAMILY_CAT;
                    data.cred = getToken();

                    // 异步验证器是需要返回promise的。
                    var deferred = $q.defer();
                    //这里加入一个等待，目的是现实pending消息。
                    $timeout(function () {
                        console.log(JSON.stringify(data));
                        ProfileService.CheckProfile(data)
                            .then(function (res) {
                                if (res.success) {
                                    if (res.appended) {
                                        //已被添加时，设置该表单字段无效
                                        ctrl.$setValidity('isExisted', false);
                                    } else {
                                        //尚未被添加时， 设置该表单字段有效
                                        ctrl.$setValidity('isExisted', true);
                                        $parse(attrs.ngModel).assign(scope, ctrl.$viewValue);
                                    }
                                } else {
                                    alert(res.message);
                                }
                            });
                    }, 1000);
                    return deferred.promise;
                };
            }
        };
    }]);

formTypesDirectives.directive('typePassportNumberRegister', ['checkPassportNumber',
    'ProfileService', '$q', '$timeout', '$location', '$parse', '$uibModal',
    'getPersonCategory',
    function (checkPassportNumber, ProfileService, $q, $timeout, $location,
        $parse, $uibModal, getPersonCategory) {
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

                    // 异步验证器是需要返回promise的。
                    var deferred = $q.defer();
                    ProfileService.CheckProfile(data)
                        .then(function (res) {
                            if (res.success) {
                                if (res.registered) {
                                    //已被注册时，设置该表单字段无效，并弹出一个提示对话框
                                    $timeout(
                                        function () {
                                            ctrl.$setValidity('isExisted', false);
                                            var ModalInstance = $uibModal.open({
                                                animation: true,
                                                templateUrl: '/partials/modals/ProfileexistedPassportNumber.html',
                                                controller: 'ProfileExistedModalInstanceCtrl',
                                                size: 'md',
                                                resolve: {
                                                    username: function () {
                                                        return res.username;
                                                    }
                                                }
                                            });

                                            ModalInstance.result.then(
                                                function () {
                                                    $location.path('/user/login');
                                                },
                                                function () {

                                                });
                                        }, 50);
                                } else {
                                    //尚未被注册时， 设置该表单字段有效
                                    $timeout(
                                        function () {
                                            ctrl.$setValidity('isExisted', true);
                                            $parse(attrs.ngModel).assign(scope, ctrl.$viewValue);
                                            //$parse(attrs.ngModel).assign(scope, ctrl.$viewValue.split(','));
                                        }, 1000);
                                }
                            } else {
                                alert(res.message);
                            }
                        });
                    return deferred.promise;
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

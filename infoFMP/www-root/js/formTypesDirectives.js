'use strict';

var formTypesDirectives = angular.module('formTypesDirectives', []);

formTypesDirectives.directive('typeFirstname', [
    function typeFirstname(){
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
    function typeLastname(){
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

// 身份证好验证代码
formTypesDirectives.directive('typeIdNumber', ['checkIDCardNumber',
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

formTypesDirectives.directive('typePassportNumber', ['checkPassportNumber',
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

//input 类型的指令
formTypesDirectives.directive('typeUsername', ['$q', 'UserService', '$timeout',
    '$parse',
    function ($q, UserService, $timeout, $parse) {
        var USERNAME_REGEXP = /^[a-zA-Z0-9]+$/;
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elm, attrs, ctrl) {

                ctrl.$validators.format = function (modelValue, viewValue) {
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

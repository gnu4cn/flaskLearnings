'use strict';

var bServices = angular.module('bServices', ['ngCookies']);

bServices.factory('updatePassportVISA', ['UserService', '$q',
    '$timeout',
    function (UserService, $q, $timeout) {
        return function (scope, uibModalInstance) {
            UserService.PassportVISAOperation(scope.data).then(
                function (res) {
                    scope.responseMsg = res.message;
                    if (res.success) {
                        scope.serverFault = false;
                        if (res.updated || res.created) {
                            scope.updatedFailed = false;
                            scope.updatedSuccess = true;
                            var defer = $q.defer();
                            $timeout(function () {
                                uibModalInstance.close(true);
                            }, 3000);
                            return defer.promise;
                        } else {
                            scope.updatedSuccess = false;
                            scope.updatedFailed = true;
                        }
                    } else {
                        scope.updatedSuccess = false;
                        scope.updatedFailed = false;
                        scope.serverFault = true;
                    }
                }
            );
        };
    }]);

bServices.factory('updateBasicProfile', ['UserService', '$q',
    '$timeout',
    function (UserService, $q, $timeout) {
        return function (scope, uibModalInstance) {
            UserService.UpdateBasicProfile(scope.profile).then(
                function (res) {
                    scope.responseMsg = res.message;
                    if (res.success) {
                        scope.serverFault = false;
                        if (res.updated) {
                            scope.updatedFailed = false;
                            scope.updatedSuccess = true;
                            var defer = $q.defer();
                            $timeout(function () {
                                uibModalInstance.close(true);
                            }, 3000);
                            return defer.promise;
                        } else {
                            scope.updatedSuccess = false;
                            scope.updatedFailed = true;
                        }
                    } else {
                        scope.updatedSuccess = false;
                        scope.updatedFailed = false;
                        scope.serverFault = true;
                    }
                }
            );
        };
    }]);

bServices.factory('accountProfilePostProcess', [function () {
        return function (scope, res) {
            scope.user.type = scope.userType = parseInt(scope.user.category.id, 10);
            var is_passport_visa_exists = scope.is_passport_visa_exists = res.profile.passport_visa !== undefined;
            var is_physical_exists = scope.is_physical_exists = res.profile.physical !== undefined;
            scope.is_socialedu_exists = res.profile.socialedu !== undefined;
            var is_career_exists = scope.is_career_exists = res.profile.career !== undefined;
            scope.is_toStaff_exists = res.profile.staff !== undefined;
            scope.is_toTrainee_exists = res.profile.trainee !== undefined;
            //console.log($scope.cred);
            //不能在today上生成新的日期，会破坏today。
            var today = new moment();

            if (scope.userType === 0) {
                scope.is_family_exists = res.profile.families.length > 0;
            }

            //生日（外籍学员）
            if (scope.userType === 5) {
                scope.is_contacts_exists = res.profile.contacts.length > 0;
                scope.is_working_exists = res.profile.workings.length > 0;
                scope.is_training_exists = res.profile.trainings.length > 0;
                scope.is_relative_exists = res.profile.relatives.length > 0;
                scope.is_study_abroad_exists = res.profile.studys_abroad.length > 0;
                scope.is_family_exists = res.profile.families.length > 0;

                //生日的判断
                var minBirthYear = moment().subtract(65, "years");
                //http://stackoverflow.com/questions/23263380/deprecation-warning-moment-construction-falls-back-to-js-date
                scope.birthday = scope.user.profile.birthday = new moment(new Date(res.profile.birthday));
                scope.birthday_invalid = scope.birthday.isAfter(today);
                scope.birthday_warning = scope.birthday.isBefore(minBirthYear);
            }

            //护照签证涉及的日期后处理
            if (is_passport_visa_exists) {
                var oneWeekLater = moment().add(7, "days");
                scope.visa_valid_date = scope.user.profile.visa_valid_date = new moment(res.profile.passport_visa.visa_valid_date);
                scope.visa_expired = scope.visa_valid_date.isBefore(today);
                scope.visa_expired_soon = scope.visa_valid_date.isBefore(oneWeekLater);
                //console.log(scope.user.profile.passport_visa.visa_valid_date.format("YYYY-MM-DD"));
                if (scope.userType === 5) {
                    var fourYearsAgo = moment().subtract(4, "years");
                    scope.entrance_date = scope.user.profile.passport_visa.entrance_date = new moment(res.profile.passport_visa.entrance_date);
                    scope.exit_date = scope.user.profile.passport_visa.exit_date = new moment(res.profile.passport_visa.exit_date);
                    scope.entrance_date_warning = scope.entrance_date.isBefore(fourYearsAgo);
                    scope.exit_date_invalid = scope.exit_date.isBefore(today);
                    scope.exit_date_warning = scope.exit_date.isBefore(oneWeekLater);
                }
            }

            //岗位日期的后处理（外籍学员）
            if (is_career_exists) {
                scope.user.profile.position_date = new moment(res.profile.career.position_date);
                scope.postion_date_invalid = scope.position_date.isAfter(today);
            }

            if (is_physical_exists) {
                scope.height_invalid = res.profile.physical.height < 140 && res.profile.physical.height > 300;
                scope.weight_invalid = res.profile.physical.weight < 30 && res.profile.physical.weight > 150;
                scope.shoesize_invalid = res.profile.physical.shoesize < 18 && res.profile.physical.shoesize > 55;
            }
        };
    }]);

bServices.factory('rememberVISANumber', ['$cookies',
    function ($cookies) {
        return function (number) {
            $cookies.put('visa_number', number);
        };
    }]);

bServices.factory('forgetVISANumber', ['$cookies',
    function ($cookies) {
        return function () {
            $cookies.remove('visa_number');
        };
    }]);

bServices.factory('getVISANumber', ['$cookies',
    function ($cookies) {
        return function () {
            var number = $cookies.get('visa_number');
            if (number !== undefined) {
                return number;
            } else {
                return '';
            }
        };
    }]);

bServices.factory('setActiveTab', ['$cookies',
    function ($cookies) {
        return function (index) {
            $cookies.put('active_tab', index);
        };
    }]);

bServices.factory('getActiveTab', ['$cookies',
    function ($cookies) {
        return function () {
            var active = $cookies.get('active_tab');
            if (active !== undefined) {
                return active;
            } else {
                return 0;
            }
        };
    }]);

bServices.factory('setLocale', ['$cookies',
    function setLocale($cookies) {
        return function (locale) {
            //这里有$cookies的用法
            $cookies.put('locale', locale);
        };
    }]);
bServices.factory('getLocale', ['$cookies',
    function getLocale($cookies) {
        return function () {
            var locale = $cookies.get('locale');
            if (locale !== undefined && locale !== '') {
                return locale;
            } else
                return 'en-us';
        };
    }]);
bServices.factory('setCreds',
    ['$cookies', function setCreds($cookies) {
            return function (token) {
                var cred = token.concat(":", 'unused');
                $cookies.put('Creds', cred);
            };
        }]);
bServices.factory('checkCreds',
    ['$cookies', function checkCreds($cookies) {
            return function () {
                var returnVal = false;
                var Creds = $cookies.get('Creds');
                if (Creds !== undefined && Creds !== "") {
                    returnVal = true;
                }
                return returnVal;
            };
        }]);
bServices.factory('getToken',
    ['$cookies', function getToken($cookies) {
            return function () {
                var returnVal = "";
                var Creds = $cookies.get('Creds');
                if (Creds !== undefined && Creds !== "") {
                    returnVal = Creds;
                }
                return returnVal;
            };
        }]);
bServices.factory('deleteCreds',
    ['$cookies', function deleteCreds($cookies) {
            return function () {
                $cookies.remove('Creds');
            };
        }]);
bServices.factory('beforeAuthorizedOps', ['checkCreds', 'getLocale', 'getToken',
    'UserService', 'languageService', '$location', '$uibModal', 'deleteCreds',
    function beforeAuthorizedOps(checkCreds, getLocale, getToken, UserService,
        languageService, $location, $uibModal, deleteCreds) {
        return function () {
            var userLocale = getLocale();
            var userCred = getToken();
            var lang = languageService();
            if (!checkCreds()) {
                $location.path('/user/login');
            } else {
                UserService.CheckCredValid(userLocale, userCred).then(
                    function (res) {
                        if (res.success) {
                        } else {
                            deleteCreds();
                            var CredInvalidModalInstance = $uibModal.open({
                                animation: true,
                                templateUrl: '/partials/modals/CredInvalid.html',
                                controller: 'CredInvalidModalInstanceCtrl',
                                size: 'sm',
                                resolve: {
                                    message: function () {
                                        return res.message;
                                    }
                                }
                            });
                            CredInvalidModalInstance.result.then(
                                function () {
                                    $location.path('/user/login');
                                },
                                function () {
                                    $location.path('/');
                                });
                        }
                    });
            }
        };
    }]);
bServices.factory('setamMomentLocal', ['amMoment',
    function setamMomentLocal(amMoment) {
        return function (locale) {
            amMoment.changeLocale(locale);
        };
    }]);
bServices.factory('checkPassportNumber',
    function checkPassportNumber() {
        return function (Number) {
            var PASSPORT_NUMBER_REGEXP = /^([A-Z0-9])[A-Z0-9]{3,8}$/;
            return PASSPORT_NUMBER_REGEXP.test(Number);
        };
    });
bServices.factory('setPersonCategory', ['$cookies',
    function setPersonCategory($cookies) {
        return function (category) {
            $cookies.put('PersonCategory', category);
        };
    }]);
bServices.factory('getPersonCategory', ['$cookies',
    function getPersonCategory($cookies) {
        return function () {
            var returnVal = $cookies.get('PersonCategory');
            if (returnVal !== undefined && returnVal !== '')
                return returnVal;
            else
                return 6;
        };
    }]);

// 这里创造性地将身份证号检查做成了业务逻辑服务！
bServices.factory('checkIDCardNumber',
    function () {
        return function (ID_Number) {
            var vcity = {
                11: "北京",
                12: "天津",
                13: "河北",
                14: "山西",
                15: "内蒙古",
                21: "辽宁",
                22: "吉林",
                23: "黑龙江",
                31: "上海",
                32: "江苏",
                33: "浙江",
                34: "安徽",
                35: "福建",
                36: "江西",
                37: "山东",
                41: "河南",
                42: "湖北",
                43: "湖南",
                44: "广东",
                45: "广西",
                46: "海南",
                50: "重庆",
                51: "四川",
                52: "贵州",
                53: "云南",
                54: "西藏",
                61: "陕西",
                62: "甘肃",
                63: "青海",
                64: "宁夏",
                65: "新疆",
                71: "台湾",
                81: "香港",
                82: "澳门",
                91: "国外"
            };
            //检查号码是否符合规范，包括长度，类型
            function isCardNo(card)
            {
                //身份证号码为15位或者18位，15位时全为数字，18位前17位为数字，最后一位是校验位，可能为数字或字符X
                var reg = /(^\d{15}$)|(^\d{17}(\d|X)$)/;
                if (reg.test(card) === false)
                {
                    //alert("demo");
                    return false;
                }

                return true;
            }
            ;
            //取身份证前两位,校验省份
            function checkProvince(card)
            {
                var province = card.substr(0, 2);
                if (vcity[province] === undefined)
                {
                    return false;
                }
                return true;
            }
            ;
            //检查生日是否正确
            function checkBirthday(card)
            {
                var len = card.length;
                //身份证15位时，次序为省（3位）市（3位）年（2位）月（2位）日（2位）校验位（3位），皆为数字
                if (len === 15)
                {
                    var re_fifteen = /^(\d{6})(\d{2})(\d{2})(\d{2})(\d{3})$/;
                    var arr_data = card.match(re_fifteen);
                    var year = arr_data[2];
                    var month = arr_data[3];
                    var day = arr_data[4];
                    var birthday = new Date('19' + year + '/' + month + '/' + day);
                    return verifyBirthday(birthday);
                }
                //身份证18位时，次序为省（3位）市（3位）年（4位）月（2位）日（2位）校验位（4位），校验位末尾可能为X
                if (len === 18)
                {
                    var re_eighteen = /^(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X)$/;
                    var arr_data = card.match(re_eighteen);
                    var year = arr_data[2];
                    var month = arr_data[3];
                    var day = arr_data[4];
                    var birthday = new Date(year + '/' + month + '/' + day);
                    return verifyBirthday(birthday);
                }
                return false;
            }
            ;
            //校验日期
            function verifyBirthday(date)
            {
                // 利用了moment.js来检查生日，但如设置为xxxx-02-31仍然能通过检查
                // 
                var oneHundredYearsAgo = moment().subtract(100, "years");
                var threeYearsAgo = moment().subtract(3, "years");
                var testDate = moment(date);
                //年月日是否合理
                if (testDate.isValid)
                {
                    //判断年份的范围（3岁到100岁之间)
                    if (oneHundredYearsAgo.isBefore(testDate) && threeYearsAgo.isAfter(testDate))
                    {
                        return true;
                    }
                    return false;
                }
                return false;
            }
            ;
            //校验位的检测
            function checkParity(card)
            {
                //15位转18位
                card = changeFivteenToEighteen(card);
                var len = card.length;
                if (len === 18)
                {
                    var arrInt = new Array(7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2);
                    var arrCh = new Array('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2');
                    var cardTemp = 0, i, valnum;
                    for (i = 0; i < 17; i++)
                    {
                        cardTemp += card.substr(i, 1) * arrInt[i];
                    }
                    valnum = arrCh[cardTemp % 11];
                    if (valnum === card.substr(17, 1))
                    {
                        return true;
                    }
                    return false;
                }
                return false;
            }
            ;
            //15位转18位身份证号
            function changeFivteenToEighteen(card)
            {
                if (card.length === 15)
                {
                    var arrInt = new Array(7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2);
                    var arrCh = new Array('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2');
                    var cardTemp = 0, i;
                    card = card.substr(0, 6) + '19' + card.substr(6, card.length - 6);
                    for (i = 0; i < 17; i++)
                    {
                        cardTemp += card.substr(i, 1) * arrInt[i];
                    }
                    card += arrCh[cardTemp % 11];
                    return card;
                }
                return card;
            }
            ;
            //是否为空
            if (ID_Number === '')
            {
                //alert('请输入身份证号，身份证号不能为空');
                //document.getElementById('card_no').focus;
                return true;
            }
            //校验长度，类型
            if (isCardNo(ID_Number) === false)
            {
                console.log('您输入的身份证号码不正确，请重新输入');
                //document.getElementById('card_no').focus;
                return false;
            }
            //检查省份
            if (checkProvince(ID_Number) === false)
            {
                console.log('您输入的身份证号码不正确,请重新输入');
                //document.getElementById('card_no').focus;
                return false;
            }
            //校验生日
            if (checkBirthday(ID_Number) === false)
            {
                console.log('您输入的身份证号码生日不正确,请重新输入');
                //document.getElementById('card_no').focus();
                return false;
            }
            //检验位的检测
            if (checkParity(ID_Number) === false)
            {
                console.log('您的身份证校验位不正确,请重新输入');
                //document.getElementById('card_no').focus();
                return false;
            }
            //alert('OK');
            return true;
        };
    });






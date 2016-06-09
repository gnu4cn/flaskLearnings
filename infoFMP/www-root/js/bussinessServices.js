'use strict';

var bussinessServices = angular.module('bussinessServices', ['ngCookies']);

bussinessServices.factory('setLocale', ['$cookies',
    function setLocale($cookies) {
        return function (locale) {
            //这里有$cookies的用法
            $cookies.put('locale', locale);
        };
    }]);

bussinessServices.factory('getLocale', ['$cookies',
    function getLocale($cookies) {
        return function () {
            var locale = $cookies.get('locale');
            if (locale !== undefined && locale !== '') {
                return locale;
            } else
                return 'en';
        };
    }]);

bussinessServices.factory('setCreds',
    ['$cookies', function setCreds($cookies) {
            return function (token) {
                var cred = token.concat(":", 'unused');
                $cookies.put('Creds', cred);
            };
        }]);

bussinessServices.factory('checkCreds',
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

bussinessServices.factory('getToken',
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

bussinessServices.factory('deleteCreds',
    ['$cookies', function deleteCreds($cookies) {
            return function () {
                $cookies.remove('Creds');
            };
        }]);

bussinessServices.factory('beforeAuthorizedOps', ['checkCreds', 'getLocale', 'getToken',
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
                                templateUrl: '/partials/modals/credInvalid.html',
                                controller: 'CredInvalidModalInstanceCtrl',
                                size: 'sm',
                                resolve: {
                                    lang: function () {
                                        return lang;
                                    },
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
                                    deleteCreds();
                                    $location.path('/');
                                });
                        }
                    });
            }
        };
    }]);

bussinessServices.factory('setamMomentLocal', ['amMoment',
    function setamMomentLocal(amMoment) {
        return function (locale) {
            amMoment.changeLocale(locale);
        };
    }]);

bussinessServices.factory('checkPassportNumber',
    function checkPassportNumber() {
        return function(Number){
            var PASSPORT_NUMBER_REGEXP = /^[A-Z0-9<]{9}[0-9]{1}[A-Z]{3}[0-9]{7}[A-Z]{1}[0-9]{7}[A-Z0-9<]{14}[0-9]{2}$/;
            return PASSPORT_NUMBER_REGEXP.test(Number);
        };
    });
    
bussinessServices.factory('setPersonCategory', ['$cookies', 
    function setPersonCategory($cookies){
        return function(category){
            $cookies.put('PersonCategory', category);
        };
    }]);

bussinessServices.factory('getPersonCategory', ['$cookies', 
    function getPersonCategory($cookies){
        return function(){
            var returnVal =  $cookies.get('PersonCategory');
            if (returnVal !== undefined && returnVal !== '')
                return returnVal;            
            else 
                return 6;
        };
    }]);
// 这里创造性地将身份证号检查做成了业务逻辑服务！
bussinessServices.factory('checkIDCardNumber',
    function checkIDCardNumber() {
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
    
    




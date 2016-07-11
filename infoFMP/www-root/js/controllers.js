'use strict';

var WAITTIME = 1000;
var TFAMILY_CAT = '6';
var SFAMILY_CAT = '1';

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

Controllers.controller('SingleImageProfileModalInstanceCtrl', ['$scope', 'user',
    'languageService', 'FileUploader', 'getToken', 'MediaService', '$uibModal',
    'ProfileService', '$route', '$uibModalInstance',
    function ($scope, user, languageService, FileUploader, getToken,
        MediaService, $uibModal, ProfileService, $route, $uibModalInstance) {
        $scope.lang = JSON.parse(languageService());
        $scope.Buttons = [];

        var uploader = $scope.uploader = new FileUploader({
            //通过URL传入user_id, multipart/form-data是无法同时传输JSON数据的。
            url: '/api/upload/image/' + user.id.toString(),
            headers: {
                //这样为angular-file-uploader加入认证
                'Authorization': 'Basic ' + btoa(getToken())
            }
        });

        // FILTERS
        uploader.filters.push({
            name: 'imageFilter',
            fn: function (item /*{File|FileLikeObject}*/, options) {
                var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
                return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
            }
        });

        uploader.onSuccessItem = function () {
            //这里要前往前一个tab页，并刷新图片清单了。
            //这里可以什么也不做，哈哈！！
            $scope.uploadFailed = false;
            $scope.uploadSuccess = true;
        };

        uploader.onAfterAddingFile = function (fileItem) {
            $scope.uploadFailed = false;
            $scope.uploadSuccess = false;
        };

        uploader.onErrorItem = function (fileItem, response, status, headers) {
            $scope.uploadFailed = true;
            $scope.FileUploading = fileItem._file.name;
        };

        $scope.selectImage = function (imageId) {
            var uibModalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'partials/modals/SetProfilePhotoModal.html',
                controller: 'SetProfilePhotoModalInstanceCtrl',
                size: 'md',
                resolve: {
                    imageId: function () {
                        return imageId;
                    }
                }
            });

            uibModalInstance.result.then(
                function () {
                    //set the picture as profile photo
                    var data = {};
                    data.user_id = user.id;
                    data.thumbnail_id = imageId;
                    ProfileService.SetProfilePhoto(data).then(
                        function (res) {
                            if (res.set) {
                                $scope.setProfilePhotoFailed = false;
                                $scope.setProfilePhotoSuccess = true;
                                $route.reload();
                                $uibModalInstance.close(true);
                            } else {
                                $scope.setProfilePhotoFailed = true;
                                $scope.setProfilePhotoSuccess = false;
                            }
                        });
                },
                function () {
                    //nothing to do
                });
        };

        $scope.imagePreview = function (imageId) {

        };

        $scope.deleteImage = function (imageId) {

        };

        $scope.thumbnailsRefresh = function () {
            $scope.setProfilePhotoFailed = false;
            $scope.setProfilePhotoSuccess = false;
            $scope.uploadSuccess = false;
            MediaService.GetThumbnails({'user_id': user.id}).then(
                function (res) {
                    if (res.success) {
                        $scope.months = res.months;
                    } else {

                    }
                });
        };
    }]);

Controllers.controller('SetProfilePhotoModalInstanceCtrl', ['$scope', 'imageId',
    'languageService', 'MediaService', '$uibModalInstance',
    function ($scope, imageId, languageService, MediaService, $uibModalInstance) {
        $scope.lang = JSON.parse(languageService());

        MediaService.RetrieveOriginbyThumbnailId(imageId).then(
            function (res) {
                $scope.originSrc = res.uri;
            });

        $scope.ok = function () {
            $uibModalInstance.close(true);
        };
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };
    }]);

Controllers.controller('CredInvalidModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'message', '$sce', 'languageService',
    function ($scope, $uibModalInstance, message, $sce, languageService) {
        //console.log(JSON.stringify(lang));
        $scope.message = $sce.trustAsHtml(message);
        $scope.lang = JSON.parse(languageService());
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
    'languageService', 'UserService', '$timeout', 'getLocale', 'setCreds',
    'setActiveTab',
    function LoginCtrl($scope, $location, languageService, UserService,
        $timeout, getLocale, setCreds, setActiveTab) {
        $scope.currentMenu = {
            about: '',
            news: '',
            notices: '',
            profile: '',
            login: 'active',
            register: ''
        };
        $scope.lang = JSON.parse(languageService());
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
                    $scope.responseMsg = res.message;
                    //发送请求成功
                    if (res.success) {
                        $scope.loginSuccess = true;
                        $scope.serverFault = false;
                        setActiveTab(0);
                        setCreds(res.token);
                        $timeout(function () {
                            $location.path('/');
                        }, 2000);
                    }
                    //发送请求失败
                    else {
                        $scope.loginSuccess = false;
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
        $scope.lang = JSON.parse(languageService());
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

Controllers.controller('PassportVISATraineeModalInstanceCtrl', ['$scope', 'user',
    'lang', 'getLocale', 'PassportTypeList', 'CertTypeList', '$uibModalInstance',
    'getToken', 'updatePassportVISA', 'rememberVISANumber', 'getVISANumber',
    'forgetVISANumber',
    function ($scope, user, lang, getLocale, PassportTypeList, CertTypeList,
        $uibModalInstance, getToken, updatePassportVISA, rememberVISANumber,
        getVISANumber, forgetVISANumber) {
        $scope.lang = lang;
        var userLocale = getLocale();

        $scope.data = {};

        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };

        var today = new moment();

        $scope.minArriveDate = today.toDate();

        $scope.submitChanges = function () {
            $scope.data.locale = userLocale;
            $scope.data.cred = getToken();
            $scope.data.passport_type = $scope.passport_type.id;
            $scope.data.visa_type = $scope.visa_type.id;
            $scope.data.visa_valid_date = new moment($scope.visa_valid_date).add(1, 'days');
            $scope.data.arrive_date = new moment($scope.arrive_date).add(1, 'days');
            $scope.data.return_date = new moment($scope.return_date).add(1, 'days');
            forgetVISANumber();
            updatePassportVISA($scope, $uibModalInstance);
        };

        $scope.setVisaNumber = function () {
            if ($scope.visa_type.id === '3') {
                rememberVISANumber($scope.data.VISANumber);
                $scope.data.VISANumber = '无/Null';
            } else {
                $scope.data.VISANumber = getVISANumber();
            }
        };

        PassportTypeList.get(
            {locale: userLocale},
            function success(response) {
                var pp_types = $scope.PassportTypes = response;
                if (user.profile.passport_visa !== undefined) {
                    for (var i = 0; i < pp_types.length; i++) {
                        if (pp_types[i].id === user.profile.passport_visa.passport_type.id) {
                            $scope.passport_type = pp_types[i];
                        }
                    }
                }
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            }
        );

        CertTypeList.get(
            {locale: userLocale},
            function success(response) {
                var visa_types = $scope.VISATypes = response;
                if (user.profile.passport_visa !== undefined) {
                    for (var i = 0; i < visa_types.length; i++) {
                        if (visa_types[i].id === user.profile.passport_visa.visa_type.id) {
                            $scope.visa_type = visa_types[i];
                        }
                    }
                }
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            }
        );

        if (user.profile.passport_visa === undefined) {
            $scope.passport_type = undefined;
            $scope.visa_type = undefined;
            $scope.data.VISANumber = '';
            $scope.data.arrive_flight = '';
            $scope.data.return_flight = '';
        } else {
            $scope.data.VISANumber = user.profile.passport_visa.visa_number;
            $scope.visa_valid_date = new moment(user.profile.passport_visa.visa_valid_date).toDate();
            //学员的进出境信息
            $scope.arrive_date = new moment(user.profile.passport_visa.entrance_date).toDate();
            $scope.data.arrive_flight = user.profile.passport_visa.entrance_flight;
            $scope.return_date = new moment(user.profile.passport_visa.exit_date).toDate();
            $scope.data.return_flight = user.profile.passport_visa.exit_flight;
        }

    }]);


Controllers.controller('PassportVISATraineeFamilyModalInstanceCtrl', ['$scope', 'user',
    'lang', 'getLocale', 'PassportTypeList', 'CertTypeList', '$uibModalInstance',
    'rememberVISANumber', 'getVISANumber', 'getToken', 'updatePassportVISA',
    'forgetVISANumber',
    function ($scope, user, lang, getLocale, PassportTypeList, CertTypeList,
        $uibModalInstance, rememberVISANumber, getVISANumber, getToken, updatePassportVISA,
        forgetVISANumber) {
        $scope.lang = lang;
        var userLocale = getLocale();

        $scope.data = {};

        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };

        $scope.setVisaNumber = function () {
            if ($scope.visa_type.id === '3') {
                rememberVISANumber($scope.data.VISANumber);
                $scope.data.VISANumber = '无/Null';
            } else {
                $scope.data.VISANumber = getVISANumber();
            }
        };

        $scope.submitChanges = function () {
            $scope.data.locale = userLocale;
            $scope.data.cred = getToken();
            $scope.data.passport_type = $scope.passport_type.id;
            $scope.data.visa_type = $scope.visa_type.id;
            $scope.data.visa_valid_date = new moment($scope.visa_valid_date).add(1, 'days');
            forgetVISANumber();
            updatePassportVISA($scope, $uibModalInstance);
        };

        PassportTypeList.get(
            {locale: userLocale},
            function success(response) {
                var pp_types = $scope.PassportTypes = response;
                if (user.profile.passport_visa !== undefined) {
                    for (var i = 0; i < pp_types.length; i++) {
                        if (pp_types[i].id === user.profile.passport_visa.passport_type.id) {
                            $scope.passport_type = pp_types[i];
                            break;
                        }
                    }
                }
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            }
        );

        CertTypeList.get(
            {locale: userLocale},
            function success(response) {
                var visa_types = $scope.VISATypes = response;
                if (user.profile.passport_visa !== undefined) {
                    for (var i = 0; i < visa_types.length; i++) {
                        if (visa_types[i].id === user.profile.passport_visa.visa_type.id) {
                            $scope.visa_type = visa_types[i];
                            break;
                        }
                    }
                }
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            }
        );

        if (user.profile.passport_visa === undefined) {
            $scope.passport_type = undefined;
            $scope.visa_type = undefined;
            $scope.data.VISANumber = '';
        } else {
            $scope.data.VISANumber = user.profile.passport_visa.visa_number;
            $scope.visa_valid_date = new moment(user.profile.passport_visa.visa_valid_date).toDate();
        }

    }]);

Controllers.controller('BasicProfileStaffModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'user', 'getToken', 'getLocale', 'languageService',
    'updateBasicProfile', 'DepartmentList', 'DepartmentPositions',
    function ($scope, $uibModalInstance, user, getToken, getLocale, languageService,
        updateBasicProfile, DepartmentList, DepartmentPositions) {
        $scope.lang = JSON.parse(languageService());
        var userLocale = getLocale();
        //$scope.profile = user.profile;
        $scope.profile = {};
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };
        $scope.updatePostionList = function () {
            console.log(JSON.stringify($scope.department));
            DepartmentPositions.get(
                {
                    locale: userLocale,
                    d_id: $scope.department.id
                },
                function success(response) {
                    console.log(JSON.stringify(response));
                    $scope.positions = response;
                },
                function error(errorResponse) {
                    console.log(JSON.stringify(errorResponse));
                });
        };
        $scope.submitChanges = function () {
            $scope.profile.cred = getToken();
            $scope.profile.locale = userLocale;
            $scope.profile.position = $scope.position.id;
            $scope.profile.category = user.type.toString();

            updateBasicProfile($scope, $uibModalInstance);
        };

        //姓名及中文名字
        $scope.profile.firstName = user.profile.f_name;
        $scope.profile.lastName = user.profile.l_name;
        $scope.profile.idNumber = user.profile.id_number;
        $scope.profile.mobile = user.profile.mobile;
        DepartmentList.get(
            {locale: userLocale},
            function success(response) {
                $scope.departments = response;
                //下面的代码用于预置select选项
                for (var i = 0; i < response.length; i++) {
                    if (response[i].id === user.profile.position.DEPARTMENT.id) {
                        $scope.department = response[i];
                        break;
                    }
                }
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            });
        DepartmentPositions.get(
            {
                locale: userLocale,
                d_id: user.profile.position.DEPARTMENT.id
            },
            function success(response) {
                //console.log(JSON.stringify(response));
                $scope.positions = response;
                //下面的代码用于预置select选项
                for (var i = 0; i < response.length; i++) {
                    if (response[i].id === user.profile.position.id) {
                        $scope.position = response[i];
                        break;
                    }
                }
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            });
    }]);
Controllers.controller('BasicProfileStaffFamilyModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'updateBasicProfile', 'lang', 'user', 'getToken', 'getLocale',
    function ($scope, $uibModalInstance, updateBasicProfile, lang, user,
        getToken, getLocale) {
        $scope.lang = lang;
        var userLocale = getLocale();
        //$scope.profile = user.profile;
        $scope.profile = {};
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };
        $scope.submitChanges = function () {
            $scope.profile.cred = getToken();
            $scope.profile.locale = userLocale;
            $scope.profile.category = user.type.toString();

            updateBasicProfile($scope, $uibModalInstance);
        };

        //姓名及中文名字
        $scope.profile.firstName = user.profile.f_name;
        $scope.profile.lastName = user.profile.l_name;
        $scope.profile.idNumber = user.profile.id_number;
        $scope.profile.mobile = user.profile.mobile;
    }]);
Controllers.controller('BasicProfileTraineeModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'lang', 'user', 'getToken', 'getLocale',
    'updateBasicProfile', 'GenderList', 'CountryList',
    function ($scope, $uibModalInstance, lang, user, getToken, getLocale,
        updateBasicProfile, GenderList, CountryList) {
        $scope.lang = lang;
        var userLocale = getLocale();
        //$scope.profile = user.profile;
        $scope.profile = {};
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };
        $scope.submitChanges = function () {
            $scope.profile.cred = getToken();
            $scope.profile.locale = userLocale;
            $scope.profile.category = user.type.toString();
            $scope.profile.gender = $scope.gender.id;
            $scope.profile.country_id = $scope.countrySelected.id;

            //这里要对birthday做后处理，很有意思。
            $scope.profile.birthday = new moment($scope.birthday).add(1, 'days');
            //console.log(JSON.stringify($scope.profile));

            updateBasicProfile($scope, $uibModalInstance);
        };

        //姓名及中文名字
        $scope.profile.firstName = user.profile.f_name;
        $scope.profile.lastName = user.profile.l_name;
        $scope.profile.xingming = user.profile.xingming;

        //生日
        //http://stackoverflow.com/questions/17987647/moment-js-transform-to-date-object
        $scope.birthday = user.profile.birthday.toDate();
        var today = new moment();
        $scope.minBirthday = today.subtract(60, 'years').toDate();

        //国内电话（外籍学员）
        $scope.zoneNumber = user.profile.country.zoneprefix;
        $scope.profile.home_number = user.profile.home_phone;
        //家庭地址（外籍学员）
        $scope.profile.home_address = user.profile.home_address;
        $scope.country = user.profile.country.en_simp;
        $scope.profile.mobile = user.profile.mobile;
        //性别
        GenderList.get(
            {locale: userLocale},
            function success(response) {
                $scope.Genders = response;
                //下面的代码用于预置select选项
                for (var i = 0; i < response.length; i++) {
                    if (response[i].id === user.profile.gender.id) {
                        $scope.gender = response[i];
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
    }]);

Controllers.controller('BasicProfileTraineeFamilyModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'lang', 'user', 'getToken', 'getLocale',
    'updateBasicProfile', 'GenderList', 'CountryList',
    function ($scope, $uibModalInstance, lang, user, getToken, getLocale,
        updateBasicProfile, GenderList, CountryList) {
        $scope.lang = lang;
        var userLocale = getLocale();
        //$scope.profile = user.profile;
        $scope.profile = {};
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };
        $scope.submitChanges = function () {
            $scope.profile.cred = getToken();
            $scope.profile.locale = userLocale;
            $scope.profile.category = user.type.toString();
            $scope.profile.gender = $scope.gender.id;
            $scope.profile.country_id = $scope.countrySelected.id;

            updateBasicProfile($scope, $uibModalInstance);
        };

        //姓名及中文名字
        $scope.profile.firstName = user.profile.f_name;
        $scope.profile.lastName = user.profile.l_name;
        $scope.profile.mobile = user.profile.mobile;
        //性别
        GenderList.get(
            {locale: userLocale},
            function success(response) {
                $scope.Genders = response;
                //下面的代码用于预置select选项
                for (var i = 0; i < response.length; i++) {
                    if (response[i].id === user.profile.gender.id) {
                        $scope.gender = response[i];
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
]);
Controllers.controller('PasswordModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'getToken', 'getLocale', 'UserService', '$location',
    'deleteCreds', '$timeout', 'languageService',
    function ($scope, $uibModalInstance, getToken, getLocale,
        UserService, $location, deleteCreds, $timeout, languageService) {

        $scope.lang = JSON.parse(languageService());

        $scope.ok = function () {
            $scope.data.cred = getToken();
            $scope.data.locale = getLocale();
            UserService.UpdatePassword($scope.data)
                .then(function (res) {
                    $scope.responseMsg = res.message;
                    //发送请求成功
                    if (res.success) {
                        $scope.serverFault = false;
                        if (res.updated) {
                            $scope.updatedSuccess = true;
                            $scope.oldPasswordIncorrect = false;
                            deleteCreds();
                            $timeout(function () {
                                $location.path('/user/login');
                                $uibModalInstance.close(true);
                            }, 3000);
                        } else {
                            $scope.oldPasswordIncorrect = true;
                            $scope.updatedSuccess = false;
                            $scope.data.oldPassword = '';
                        }
                    }
                    //发送请求失败
                    else {
                        $scope.serverFault = true;
                        $scope.updatedSuccess = false;
                        $scope.oldPasswordIncorrect = false;
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
    '$uibModalInstance', 'username', 'languageService',
    function ($scope, $uibModalInstance, username, languageService) {
        //console.log(JSON.stringify(lang));
        $scope.username = username;
        $scope.lang = JSON.parse(languageService());
        $scope.ok = function () {
            $uibModalInstance.close(true);
        };
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };
    }]);

Controllers.controller('StaffFamilyModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'user', 'ProfileService', '$timeout', 'languageService',
    function ($scope, $uibModalInstance, user, ProfileService, $timeout,
        languageService) {
        //console.log(JSON.stringify(lang));
        $scope.lang = JSON.parse(languageService());

        $scope.getFamilyProfile = function () {
            //等待验证完成, 这样的写法比较奇葩。
            $timeout(
                function () {
                    //当id_number字段有效时，才获取现有数据
                    if ($scope.append.id_number.$valid) {
                        $scope.checkingIfExists = true;
                        $scope.familyFound = false;
                        var data = {};
                        data.category = SFAMILY_CAT;
                        data.idNumber = $scope.data.idNumber;
                        //这里不在需要检查是否已添加，因为在前面已经检查过了
                        //data.cred = getToken();
                        //这里加入一个$timeout, 目的是现实checkingIfExists消息。
                        $timeout(function () {
                            ProfileService.CheckProfile(data)
                                .then(function (res) {
                                    //console.log(JSON.stringify(res));
                                    $scope.checkingIfExists = false;
                                    if (res.success) {
                                        if (res.existed) {
                                            $scope.familyFound = true;
                                            $scope.data.firstName = res.profile.f_name;
                                            $scope.data.lastName = res.profile.l_name;
                                            $scope.data.mobile = res.profile.mobile;
                                            $scope.data.family_id = res.profile.id;
                                        } else {
                                            $scope.familyFound = false;
                                            var idNumber = $scope.data.idNumber;

                                            var master = {};
                                            $scope.data = angular.copy(master);
                                            $scope.data.idNumber = idNumber;
                                        }
                                    } else {
                                        alert(res.message);
                                    }
                                });
                        }, 1000);
                    } else {
                        $scope.checkingIfExists = false;
                        $scope.familyFound = false;
                        var idNumber = $scope.data.idNumber;

                        var master = {};
                        $scope.data = angular.copy(master);
                        $scope.data.idNumber = idNumber;
                    }
                }, WAITTIME);
        };

        $scope.submitFamily = function () {
            $scope.data.own_id = user.profile.id;
            $scope.data.own_category = user.person_type;
            //console.log(JSON.stringify($scope.data));

            ProfileService.AppendFamily($scope.data).then(
                function (res) {
                    if (res.success) {
                        $scope.familyFound = false;
                        $scope.checkingIfAppended = false;
                        $scope.serverFault = false;
                        if (res.appended) {
                            $scope.appendSuccess = true;
                            $scope.appendedFail = false;
                            $scope.responseMsg = $scope.lang.familyAppendSuccess;
                        } else {
                            $scope.appendSuccess = false;
                            $scope.appendedFail = true;
                            $scope.responseMsg = $scope.lang.familyAppendFailed;
                        }
                        $timeout(function () {
                            $uibModalInstance.close(true);
                        }, 1500);
                    } else {
                        $scope.familyFound = false;
                        $scope.checkingIfAppended = false;
                        $scope.appendedFail = false;
                        $scope.appendSuccess = false;
                        $scope.serverFault = true;
                        $scope.responseMsg = $scope.lang.serviceRequestFault;
                    }
                });
        };
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };
    }]);

Controllers.controller('TraineeFamilyModalInstanceCtrl', ['$scope',
    '$uibModalInstance', 'user', 'ProfileService', '$timeout', 'languageService',
    'CountryList', 'GenderList', 'getLocale',
    function ($scope, $uibModalInstance, user, ProfileService, $timeout,
        languageService, CountryList, GenderList, getLocale) {
        //console.log(JSON.stringify(lang));
        $scope.lang = JSON.parse(languageService());

        CountryList.get(
            {},
            function successs(response) {
                $scope.countries = response;
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            });

        GenderList.get(
            {locale: getLocale()},
            function success(response) {
                $scope.Genders = response;
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            }
        );

        $scope.getFamilyProfile = function () {
            //等待验证完成, 这样的写法比较奇葩。
            $timeout(
                function () {
                    //当id_number字段有效时，才获取现有数据
                    if ($scope.append.passport_number.$valid) {
                        $scope.checkingIfExists = true;
                        $scope.familyFound = false;
                        var data = {};
                        data.category = TFAMILY_CAT;
                        data.passportNumber = $scope.data.passportNumber;
                        //这里不在需要检查是否已添加，因为在前面已经检查过了
                        //data.cred = getToken();
                        //这里加入一个$timeout, 目的是现实checkingIfExists消息。
                        $timeout(function () {
                            console.log(JSON.stringify(data));
                            ProfileService.CheckProfile(data)
                                .then(function (res) {
                                    //console.log(JSON.stringify(res));
                                    $scope.checkingIfExists = false;
                                    if (res.success) {
                                        if (res.existed) {
                                            $scope.familyFound = true;
                                            $scope.data.firstName = res.profile.f_name;
                                            $scope.data.lastName = res.profile.l_name;
                                            $scope.data.mobile = res.profile.mobile;
                                            $scope.data.family_id = res.profile.id;
                                            //设置国籍和性别字段
                                            for (var i = 0; i < $scope.Genders.length; i++) {
                                                if ($scope.Genders[i].id === res.profile.gender) {
                                                    $scope.genderSelected = $scope.Genders[i];
                                                    break;
                                                }
                                            }
                                            for (var i = 0; i < $scope.countries.length; i++) {
                                                if ($scope.countries[i].id === res.profile.country_id) {
                                                    $scope.countrySelected = $scope.countries[i];
                                                    break;
                                                }
                                            }
                                        } else {
                                            $scope.familyFound = false;
                                            var passportNumber = $scope.data.passportNumber;

                                            var master = {};
                                            $scope.data = angular.copy(master);
                                            $scope.data.passportNumber = passportNumber;
                                            $scope.countrySelected = undefined;
                                        }
                                    } else {
                                        alert(res.message);
                                    }
                                });
                        }, 1000);
                    } else {
                        $scope.checkingIfExists = false;
                        $scope.familyFound = false;
                        var passportNumber = $scope.data.passportNumber;

                        var master = {};
                        $scope.data = angular.copy(master);
                        $scope.data.passportNumber = passportNumber;
                    }
                }, WAITTIME);
        };

        $scope.submitFamily = function () {
            $scope.data.own_id = user.profile.id;
            $scope.data.own_category = user.person_type;
            $scope.data.gender = $scope.genderSelected.id;
            $scope.data.country_id = $scope.countrySelected.id;

            console.log(JSON.stringify($scope.data));

            ProfileService.AppendFamily($scope.data).then(
                function (res) {
                    console.log(JSON.stringify(res));
                    if (res.success) {
                        $scope.familyFound = false;
                        $scope.checkingIfAppended = false;
                        $scope.serverFault = false;
                        if (res.appended) {
                            $scope.appendSuccess = true;
                            $scope.appendedFail = false;
                            $scope.responseMsg = $scope.lang.familyAppendSuccess;
                        } else {
                            $scope.appendSuccess = false;
                            $scope.appendedFail = true;
                            $scope.responseMsg = $scope.lang.familyAppendFailed;
                        }
                        $timeout(function () {
                            $uibModalInstance.close(true);
                        }, 1500);
                    } else {
                        $scope.familyFound = false;
                        $scope.checkingIfAppended = false;
                        $scope.appendedFail = false;
                        $scope.appendSuccess = false;
                        $scope.serverFault = true;
                        $scope.responseMsg = $scope.lang.serviceRequestFault;
                    }
                });
        };
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);
        };
    }]);

Controllers.controller('NewForeignUserCtrl', ['$scope',
    'languageService', 'getLocale', 'getPersonCategory', 'UserService',
    '$timeout', '$location', 'GenderList', 'CountryList', 'ProfileService',
    function ($scope, languageService, getLocale, getPersonCategory, UserService,
        $timeout, $location, GenderList, CountryList, ProfileService) {
        $scope.currentMenu = {
            about: '',
            news: '',
            notices: '',
            profile: '',
            login: '',
            register: 'active'
        };
        $scope.lang = JSON.parse(languageService());
        $scope.reset = function (form) {
            var master = {};
            if (form) {
                form.$setPristine();
                form.$setUntouched();
            }
            $scope.user = angular.copy(master);
            $scope.$broadcast('show-errors-reset');
            $scope.serverFault = false;
        };
        CountryList.get(
            {},
            function successs(response) {
                $scope.countries = response;
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            });
        $scope.user = {};
        var userLocale = getLocale();
        GenderList.get(
            {locale: userLocale},
            function success(response) {
                $scope.Genders = response;
                //设置国籍和性别字段
                for (var i = 0; i < $scope.Genders.length; i++) {
                    if ($scope.Genders[i].id === '1') {
                        $scope.genderSelected = $scope.Genders[i];
                        break;
                    }
                }
            },
            function error(errorResponse) {
                console.log(JSON.stringify(errorResponse));
            }
        );
        $scope.user.category = getPersonCategory();
        //
        $scope.getProfile = function () {
            //等待验证完成, 这样的写法比较奇葩。
            $timeout(
                function () {
                    //同样实在字段有效时，才去获取现有数据
                    if ($scope.register.passport_number.$valid) {
                        $scope.checkingIfProfileExists = true;
                        var data = {};
                        data.category = getPersonCategory();
                        data.passportNumber = $scope.user.passportNumber;
                        //data.cred = getToken();
                        //console.log(JSON.stringify(data));
                        //加入$timeout，以显示checkingIfProfileExists消息。
                        $timeout(function () {
                            console.log(JSON.stringify(data));
                            ProfileService.CheckProfile(data)
                                .then(function (res) {
                                    //console.log(JSON.stringify(res));
                                    $scope.checkingIfProfileExists = false;
                                    if (res.success) {
                                        if (res.existed) {
                                            $scope.profileFound = true;
                                            $scope.user.profile_id = res.profile.id;
                                            $scope.user.firstName = res.profile.f_name;
                                            $scope.user.lastName = res.profile.l_name;
                                            //设置国籍和性别字段
                                            for (var i = 0; i < $scope.Genders.length; i++) {
                                                if ($scope.Genders[i].id === res.profile.gender) {
                                                    $scope.genderSelected = $scope.Genders[i];
                                                    break;
                                                }
                                            }
                                            for (var i = 0; i < $scope.countries.length; i++) {
                                                if ($scope.countries[i].id === res.profile.country_id) {
                                                    $scope.countrySelected = $scope.countries[i];
                                                    break;
                                                }
                                            }
                                        } else {
                                            $scope.profileFound = false;
                                            $scope.user.firstName = '';
                                            $scope.user.lastName = '';
                                            $scope.genderSelected = undefined;
                                            $scope.countrySelected = undefined;
                                        }
                                    } else {
                                        alert(res.message);
                                    }
                                });
                        }, 1000);
                    } else {
                        $scope.checkingIfProfileExists = false;
                        $scope.profileFound = false;
                        $scope.user.firstName = '';
                        $scope.user.lastName = '';
                        $scope.genderSelected = undefined;
                        $scope.countrySelected = undefined;

                    }
                }, WAITTIME);
        };
        //
        $scope.submitRegistration = function () {
            $scope.user.locale = getLocale();
            $scope.user.category = getPersonCategory();
            $scope.user.country_id = $scope.countrySelected.id;
            $scope.user.gender = $scope.genderSelected.id;
            var data = $scope.user;
            console.log(JSON.stringify(data));
            UserService.Create(data)
                .then(function (res) {
                    $scope.responseMsg = res.message;
                    //发送请求成功
                    if (res.success) {
                        $scope.registeredSuccess = true;
                        $scope.serverFault = false;
                        $timeout(function () {
                            $location.path('/user/login');
                        }, 3000);
                    }
                    //发送请求失败
                    else {
                        $scope.registeredFail = true;
                        $scope.serverFault = true;
                    }
                });
        };
    }]);
Controllers.controller('NewChineseUserCtrl', ['$scope', 'languageService',
    'getLocale', 'getPersonCategory', 'UserService', '$timeout', '$location',
    'ProfileService',
    function ($scope, languageService, getLocale, getPersonCategory,
        UserService, $timeout, $location, ProfileService) {
        $scope.currentMenu = {
            about: '',
            news: '',
            notices: '',
            profile: '',
            login: '',
            register: 'active'
        };
        $scope.lang = JSON.parse(languageService());
        $scope.user = {};
        $scope.reset = function (form) {
            var master = {};
            if (form) {
                form.$setPristine();
                form.$setUntouched();
            }
            $scope.user = angular.copy(master);
            $scope.$broadcast('show-errors-reset');
            $scope.serverFault = false;
        };
        //
        $scope.getProfile = function () {
            //等待验证完成, 这样的写法比较奇葩。
            $timeout(
                function () {
                    //同样实在字段有效时，才去获取现有数据
                    if ($scope.register.id_number.$valid) {
                        $scope.checkingIfProfileExists = true;
                        var data = {};
                        data.category = getPersonCategory();
                        data.idNumber = $scope.user.idNumber;
                        //data.cred = getToken();
                        //console.log(JSON.stringify(data));
                        //加入$timeout，以显示checkingIfProfileExists消息。
                        $timeout(function () {
                            ProfileService.CheckProfile(data)
                                .then(function (res) {
                                    //console.log(JSON.stringify(res));
                                    $scope.checkingIfProfileExists = false;
                                    if (res.success) {
                                        if (res.existed) {
                                            $scope.profileFound = true;
                                            $scope.user.firstName = res.profile.f_name;
                                            $scope.user.lastName = res.profile.l_name;
                                            $scope.user.profile_id = res.profile.id;
                                        } else {
                                            $scope.profileFound = false;
                                            $scope.user.firstName = '';
                                            $scope.user.lastName = '';
                                        }
                                    } else {
                                        alert(res.message);
                                    }
                                });
                        }, 1000);
                    } else {
                        $scope.checkingIfProfileExists = false;
                        $scope.profileFound = false;
                        $scope.user.firstName = '';
                        $scope.user.lastName = '';

                    }
                }, WAITTIME);
        };
        //
        $scope.submitRegistration = function () {
            $scope.user.locale = getLocale();
            $scope.user.category = getPersonCategory();
            var data = $scope.user;
            //console.log(JSON.stringify(data));
            UserService.Create(data)
                .then(function (res) {
                    $scope.checkingIfProfileExists = false;
                    $scope.profileFound = false;
                    $scope.responseMsg = res.message;
                    //发送请求成功
                    if (res.success) {
                        $scope.registeredSuccess = true;
                        $scope.serverFault = false;
                        $timeout(function () {
                            $location.path('/user/login');
                        }, 3000);
                    }
                    //发送请求失败
                    else {
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
        $scope.lang = JSON.parse(languageService());
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
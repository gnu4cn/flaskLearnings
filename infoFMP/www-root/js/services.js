'use strict';
// 有着以下服务：
// 
// 这些都只有get方法，属于基础数据
// 
// PersonCategory，从人员类别代码获取人员类别
// *PersonCategoryList，获取人员类别及类别代码清单
// Edu，从受教育程度代码获取教育程度
// *EduList，获取教育程度代码及教育程度清单
// CertType，从签证代码，获取签证类型
// *CertTypeList, 获取签证代码和签证类型的清单
// PassportType，从护照代码，获取护照类型
// *PassportTypeList, 获取护照类型代码及护照类型的清单
// Marriage，从婚姻状况代码，获取婚姻状况
// *MarriageList, 获取婚姻状况代码及婚姻状况的清单
// Gender
// *GenderList
// Religion
// *ReligionList
// Relation
// *RelationList
// TraineeRank, 从军衔代码，获取军衔及军种信息
// Service, 从军种代码，获取军种信息
// *ServiceList, 获取军种代码和军种名称的清单
// *ServiceRanks, 从军种代码，获取该军种下的军衔清单
// Country
// *CountryList
// Language
// *LanguageList
// CustomPort
// *CustomPortList
// Province
// *ProvinceList
// *ProvinceCities
// City, 从城市ID，获取城市和该城市所属省份的信息
// Postion，从职位代码，获取该职位及其所属部门的信息
// Department
// *DepartmentList
// *DepartmentPositions
// 加*号的，返回都是数组
//
// 下面的属于专门服务
//

var services = angular.module('services', ['ngResource']);

services.factory('ProfileService', ['$http', 'languageService',
    function ($http, languageService) {
        var lang = JSON.parse(languageService());
        var service = {};

        service.CheckIDNumber = CheckIDNumber;

        return service;

        function CheckIDNumber(data) {
            return $http({
                method: 'POST',
                url: '/api/profile/exists',
                headers: {
                    'Content-Type': 'application/json'
                },
                data: data
            }).then(
                handleSuccess,
                handleError(lang.serviceRequestFault)
                );
        }

        function handleSuccess(res) {
            //在请求成功后，直接返回响应数据
            return res.data;
        }

        function handleError(error) {
            return function () {
                //在请求失败后，构造出响应json
                return {success: false, message: error};
            };
        }
    }]);

services.factory('UserService', ['$http', 'languageService',
    function UserService($http, languageService) {
        var lang = JSON.parse(languageService());
        var service = {};

        service.GetAll = GetAll;
        service.GetById = GetById;
        service.GetByUsername = GetByUsername;
        service.CheckUsername = CheckUsername;
        service.Create = Create;
        service.Update = Update;
        service.Delete = Delete;
        service.Login = Login;
        service.GetByCred = GetByCred;
        service.CheckCredValid = CheckCredValid;
        service.UpdatePassword = UpdatePassword;

        return service;

        function UpdatePassword(data) {
            return $http({
                method: 'POST',
                url: '/api/user/password',
                headers: {
                    'Content-Type': 'application/json'
                },
                data: data
            }).then(
                handleSuccess,
                handleError(lang.serviceRequestFault)
                );
        }

        function GetAll() {
            return $http.get('/api/users')
                .then(
                    handleSuccess,
                    handleError(lang.serviceRequestFault)
                    );
        }

        function GetById(id) {
            return $http.get('/api/user/' + id)
                .then(
                    handleSuccess,
                    handleError(lang.serviceRequestFault)
                    );
        }

        function GetByCred(locale, cred) {
            return $http.get('/api/user/' + locale + '/' + cred)
                .then(
                    handleSuccess,
                    handleError(lang.serviceRequestFault)
                    );
        }

        function CheckCredValid(locale, cred) {
            return $http.get('/api/user/checkcredentialvalid/' + locale + '/' + cred)
                .then(
                    handleSuccess,
                    handleError(lang.serviceRequestFault)
                    );
        }

        function GetByUsername(username) {
            return $http.get('/api/user/' + username)
                .then(
                    handleSuccess,
                    handleError(lang.serviceRequestFault)
                    );
        }

        function CheckUsername(username) {
            return $http.get('/api/user/exist/' + username)
                .then(
                    handleSuccess,
                    handleError(lang.serviceRequestFault)
                    );
        }

        function Create(user) {
            return $http({
                method: 'POST',
                url: '/api/users',
                headers: {
                    'Content-Type': 'application/json'
                },
                data: user
            }).then(
                handleSuccess,
                handleError(lang.serviceRequestFault)
                );
        }

        function Login(user) {
            return $http({
                method: 'POST',
                url: '/api/user/login',
                headers: {
                    'Content-Type': 'application/json'
                },
                data: user
            }).then(
                handleSuccess,
                handleError(lang.serviceRequestFault)
                );
        }

        function Update(user) {
            return $http.put('/api/user/' + user.id, user)
                .then(
                    handleSuccess,
                    handleError(lang.serviceRequestFault)
                    );
        }

        function Delete(id) {
            return $http.delete('/api/user/' + id)
                .then(
                    handleSuccess,
                    handleError(lang.serviceRequestFault)
                    );
        }

        // private functions
        // 就是success和error, 对$http返回的内容进行后处理，只提取返回值，最终
        // 返回的是json

        function handleSuccess(res) {
            //在请求成功后，直接返回响应数据
            return res.data;
        }

        function handleError(error) {
            return function () {
                //在请求失败后，构造出响应json
                return {success: false, message: error};
            };
        }
    }]);

///////////////////////////////////////////////////////////
////////基础数据服务
///////////////////////////////////////////////////////////
services.factory('PersonCategory', ['$resource',
    function PersonCategory($resource) {
        return $resource('/pcategory/:locale/:p_c_id',
            {},
            {
                get: {method: 'GET', cache: false, isArray: false}
            });
    }]);

services.factory('PersonCategoryList', ['$resource',
    function PersonCategoryList($resource) {
        return $resource('/api/pcategories/:locale',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('Edu', ['$resource',
    function Edu($resource) {
        return $resource('/api/edu/:locale/:e_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('EduList', ['$resource',
    function PersonCategoryList($resource) {
        return $resource('/api/edus/:locale',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('CertType', ['$resource',
    function CertType($resource) {
        return $resource('/api/cert_type/:locale/:c_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('CertTypeList', ['$resource',
    function CertTypeList($resource) {
        return $resource('/api/cert_types/:locale',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('PassportType', ['$resource',
    function PassportType($resource) {
        return $resource('/api/pp_type/:locale/:p_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('PassportTypeList', ['$resource',
    function PassportTypeList($resource) {
        return $resource('/api/pp_types/:locale',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('Marriage', ['$resource',
    function Marriage($resource) {
        return $resource('/api/marriage/:locale/:m_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('MarriageList', ['$resource',
    function MarriageList($resource) {
        return $resource('/api/marriages/:locale',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('Gender', ['$resource',
    function Gender($resource) {
        return $resource('/api/gender/:locale/:g_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('GenderList', ['$resource',
    function GenderList($resource) {
        return $resource('/api/genders/:locale',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('Religion', ['$resource',
    function Religion($resource) {
        return $resource('/api/religion/:locale/:r_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('ReligionList', ['$resource',
    function ReligionList($resource) {
        return $resource('/api/religions/:locale',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('Relation', ['$resource',
    function Relation($resource) {
        return $resource('/api/relation/:locale/:r_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('RelationList', ['$resource',
    function RelationList($resource) {
        return $resource('/api/relations/:locale',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('TraineeRank', ['$resource',
    function TraineeRank($resource) {
        return $resource('/api/trnee_rank/:locale/:tr_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('Service', ['$resource',
    function Service($resource) {
        return $resource('/api/service/:locale/:s_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('ServiceList', ['$resource',
    function ServiceList($resource) {
        return $resource('/api/services/:locale',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('ServiceRanks', ['$resource',
    function ServiceRanks($resource) {
        return $resource('/api/service/:s_id/:locale/ranks',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('Country', ['$resource',
    function Country($resource) {
        return $resource('/api/country/:c_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('CountryList', ['$resource',
    function CountryList($resource) {
        return $resource('/api/countries',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('Language', ['$resource',
    function Language($resource) {
        return $resource('/api/language/:l_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('LanguageList', ['$resource',
    function LanguageList($resource) {
        return $resource('/api/language/all',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('CustomPort', ['$resource',
    function CustomPort($resource) {
        return $resource('/api/customport/:p_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('CustomPortList', ['$resource',
    function CustomPortList($resource) {
        return $resource('/api/customport/all',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('Province', ['$resource',
    function Province($resource) {
        return $resource('/api/province/:p_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('ProvinceList', ['$resource',
    function ProvinceList($resource) {
        return $resource('/api/province/all',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('ProvinceCities', ['$resource',
    function ProvinceCities($resource) {
        return $resource('/api/province/:p_id/cities',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('City', ['$resource',
    function City($resource) {
        return $resource('/api/city/:c_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('Position', ['$resource',
    function Position($resource) {
        return $resource('/api/position/:locale/:p_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('Department', ['$resource',
    function Department($resource) {
        return $resource('/api/department/:locale/:d_id',
            {},
            {get: {method: 'GET', cache: false, isArray: false}}
        );
    }]);

services.factory('DepartmentList', ['$resource',
    function DepartmentList($resource) {
        return $resource('/api/departments/:locale',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);

services.factory('DepartmentPositions', ['$resource',
    function DepartmentPositions($resource) {
        return $resource('/api/department/:d_id/:locale/positions',
            {},
            {
                get: {method: 'GET', cache: false, isArray: true}
            });
    }]);
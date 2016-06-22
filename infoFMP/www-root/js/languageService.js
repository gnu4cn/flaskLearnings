var languageService = angular.module('languageService', []);

languageService.factory('languageService', ['getLocale',
    function languageService(getLocale) {
        return function () {
            var languagesData = [];
            languagesData['zh-cn'] = {
                yourBirthday: '请输入您的生日',
                credNotValidTips: '这是由于登入时间过长造成的，请重新登入。要重新登入，请点击"确定"， 否则点击"取消"。',
                credNotValid: '登录凭据已过期',
                UpdatePassword: '修改密码',
                AdministratorAdded: '由管理员添加',
                Created: '帐号注册于',
                CardNumber: '一卡通卡号',
                accountAndPassword: '帐号及密码',
                PersonCategoryHelp: '请选择您所属的人员类别。',
                UsernameHelpLogin: '你在这里注册的用户名/帐号。',
                PasswordHelpLogin: '该用户名/帐号所对应的密码/口令。',
                PersonCategory: '您是',
                logoutTips: '登出后，如要访问特定信息，需要重新登入。登出请点击"登出"， 否则请点击"取消"。',
                yestoLogout: '确认要登出？',
                menuLogout: '登 出',
                loginSubmit: '登 入',
                Ok: '确 定',
                Cancel: '取 消',
                ToggleMenu: '菜单开关',
                label: '昆山校区',
                brandColor: "color: #404040",
                menuAbout: '关于昆山校区',
                menuNews: '新 闻',
                menuNotices: '通 知',
                profile: '个人资料',
                User: '用户 ',
                Username: '用户名',
                PleaseInputaUsername: '请输入一个用户名',
                Agreement: '注册条款',
                UsernameHelp: '可以包含大小写字母、数字，不能包含特殊符号, 最少 5 个字符。',
                CheckingifThisUsernameisAvailable: '检查此用户名是否可用...',
                ThisUsernameisAlreadyTaken: '此用户名已被使用。',
                UsernameContainSpecialCharactors: '用户名包含了特殊字符。',
                Password: '密码',
                PasswordHelp: '口令密码应至少包含一个大小写字母、数字、特殊符号，最少 8 个字符。',
                PasswordisNotQualified: '口令密码未能满足要求',
                Required: '该字段是必需的',
                usernameMinlengthError: '最少 5 个字符。',
                isOk: '没有问题',
                passwordMinlengthError: '密码最少 8 个字符。',
                Reset: '重 置',
                newuserSubmit: '注 册',
                menuLogin: '登 入',
                menuRegister: '用户注册',
                RegisteredSuccessfully: '注册成功，前往登陆页面......',
                RegisteredFailed: '注册失败，服务端问题。',
                serviceRequestFault: '服务请求失败。',
                profileMenuDropdown: '个人资料下拉菜单。',
                Category: '人员类别',
                showPassword: '显示密码',
                hidePassword: '隐藏密码',
                passportNumber: '护照号码',
                IDNumber: '身份证号',
                YourIDNumber: '您的身份证号码',
                YourPassportNumber: '您的护照号码',
                IDNumberHelp: '身份证号码是18位的数字，特殊的身份证号码为17位数字并以大写的X结尾。',
                PassportNumberHelp: '仅包含大写字母和数字，4-9 位',
                IdNumberNotQualified: '身份证号码不正确',
                PassportNumberNotQualified: '护照号码不正确。',
                NextStep: '下一步 》',
                firstName: '姓氏',               
                lastName: '名称',
                firstNameHelp: '姓名中的第一个或第二个汉字。应以汉字/大写字母开头，不能包含特殊符号和数字。',
                PleaseInputaFirstname: '请输入您的姓氏',
                PleaseInputaLastname: '请输入您的名字',
                NoSpecialCharactors: '不能包含特殊字符。',
                lastNameHelp: '您的名字。应以汉字/大写字母开头，不能包含特殊符号和数字。',
                PleaseSetAPassword: '请提供一个密码',
                Gender: '性别',
                selectPersonCategory: '请选择你的组别',
                visaNumber: '签证编号',
                YourVisaNumber: '签证/居留许可/编号',
                selectGender: '请选择性别',
                Birthday: '生日',
                selectLanguage: '选择语言',
                BadNameFormat: '错误的姓名格式。'
            };
            languagesData['en-us'] = {
                BadNameFormat: 'Bad name format.',
                yourBirthday: 'Your birthday',
                selectLanguage: 'Select a lanauage',
                Birthday: 'Birthday',
                Gender: 'Gender',
                YourVisaNumber: 'VISA/Certificate number',
                visaNumber: 'VISA number',
                selectPersonCategory: 'Select your group',
                selectGender: 'Select a gender',
                PleaseSetAPassword: 'Please provide a password.',
                NoSpecialCharactors: 'Special charactors not allowed.',
                PleaseInputaLastname: 'Last name',
                PleaseInputaFirstname: 'First name',
                firstNameHelp: 'First name or given name. It should begin with upper case charactor, special charactors and digits are not allowed.',
                lastNameHelp: 'Last name or family name. It should begin with upper case charactor, special charactors and digits are not allowed.',
                firstName: 'First name',            
                lastName: 'Last name',
                NextStep: 'Next >>',
                PassportNumberNotQualified: 'Passport number not qualified',
                IdNumberNotQualified: 'ID number not qualified.',
                PassportNumberHelp: 'Only include upper case alphabets and digits, 4-9 of them.',
                IDNumberHelp: '18 digits, or 17 digits and a X as trailing end.',
                YourPassportNumber: 'Passport No.',
                YourIDNumber: 'ID number',
                passportNumber: 'Passport Number',
                IDNumber: 'ID Number',
                hidePassword: 'Hide the password',
                showPassword: 'Show the password',
                Category: 'Personnel category',
                credNotValidTips: 'This is because you logged in after a long time, now you should login again. To login again, press "Ok", else press "Cancel".',
                credNotValid: 'User credential expired',
                UpdatePassword: 'Change pasword',
                AdministratorAdded: 'Added by administrators',
                Created: 'Account created at',
                CardNumber: 'Campus Card Number',
                accountAndPassword: 'Account and password',
                PersonCategoryHelp: 'Please specify which group you belongs to.',
                UsernameHelpLogin: 'The account/username you have registered here.',
                PasswordHelpLogin: 'The password for your username.',
                PersonCategory: 'You are',
                logoutTips: 'After logged out, to check specific infomation, you need to login again. To logout, press "OK", else press "Cancel".',
                yestoLogout: 'Do you really want to logout?',
                menuLogout: 'Logout',
                loginSubmit: 'Login',
                Ok: 'Ok',
                Cancel: 'Cancel',
                languageSelect: 'Select language',
                profileMenuDropdown: 'Dropdown menu fro profile',
                ToggleMenu: 'Toggle menu',
                label: '昆山校区/Kunshan School',
                brandColor: "color: #404040",
                menuAbout: 'About',
                menuLogin: 'Login',
                menuRegister: 'Register',
                menuNews: 'News',
                menuNotices: 'Notices',
                profile: 'Profile',
                User: 'User ',
                Username: 'Username',
                PleaseInputaUsername: 'Please give a username.',
                Agreement: 'AGREEMENTS',
                UsernameHelp: 'It can be upper/lower case alphabets, digits, NO SPECIAL CHARATORS, at least 5 of them.',
                CheckingifThisUsernameisAvailable: 'Check whether it is available or not...',
                ThisUsernameisAlreadyTaken: 'It is occupied.',
                UsernameContainSpecialCharactors: 'Special charactor in it.',
                Password: 'Password',
                PasswordHelp: 'One upper/lower alphabet, digit and special charactor need, and at least 8 of them.',
                PasswordisNotQualified: 'Password not qualified.',
                Required: 'Needed',
                usernameMinlengthError: 'At least 5 charactors.',
                isOk: 'That\'s OK',
                passwordMinlengthError: 'At least 8 charactors.',
                Reset: 'Reset',
                newuserSubmit: 'Register',
                RegisteredSuccessfully: 'Registered Successfully, moving to index page.',
                RegisteredFailed: 'Registered failed, server problem.',
                serviceRequestFault: 'Service request failed.'
            };
            return JSON.stringify(languagesData[getLocale()]);
        };

    }]);
# -*- coding: utf-8 -*-
class lang(object):
    data = {
        'PasswordUpdateSuccessfully': {
            'zh-cn': '成功! 需要用新密码登入, 现在前往登录页面......',
            'en-us': 'Successful! now moving to the login page...'
        },
        'OldPasswordNotCorrect': {
            'zh-cn': '原密码不正确，请输入正确的原密码。',
            'en-us': 'The old password is incorrect!',
        },
        'createProfileFailed': {
            'zh-cn': '建立个人资料失败。',
            'en-us': 'Create profile failed.'
        },
        'makeRelationshipFailed': {
            'zh-cn': '建立关系失败。',
            'en-us': 'Make relationship failed.'
        },
        'fetchChineseProfileFailed': {
            'zh-cn': '获取用户资料失败。',
            'en-us': 'Fetch profile failed.'
        },
        'UsernameNotExistorPasswordNotCorrect': {
            'zh-cn': '用户名不存在或密码不正确, 请重新输入用户名密码。',
            'en-us': 'Username not exist, or password not correct! '
        },
        'LoginedSuccessful': {
            'zh-cn': '登入成功，前往首页......',
            'en-us': 'Logined successfully, moving to index page... '
        },
        'createUserSuccessfully': {
            'zh-cn': "成功创建用户，前往登入页面......",
            'en-us': "User created successfully, moving to the login page... "
        },
        'ErrorOccuredWhenWriteDB': {
            'en-us': 'Error occured when write the data into database. ',
            'zh-cn': '在将数据存入数据库时出错。',
        },
        'makeUserInstanceError': {
            'zh-cn': '服务器错误：实例化 User 对象出错。',
            'en-us': 'Server error: making User Object instance failed. '
        },
        'makeProfileInstanceFail': {
            'zh-cn': '实例化 Profile 对象出错',
            'en-us': 'Make Profile instance Failed'
        },
        'usernameOrpasswordOrcategoryIsBlank': {
            'zh-cn': '用户名或密码或人员类别为空。',
            'en-us': 'Username or password or person category is blank. '
        },
        'FailedtoGetUserAccountInfo': {
            'zh-cn': '获取用户帐号信息失败。',
            'en-us': 'Failed to get user account infomation. '
        },
        'GetUserAccountInfoSuccessfully': {
            'zh-cn': '成功获取到用户帐号信息。',
            'en-us': 'Get user account infomation successfully. '
        },
        'CredentialIncorrectOrExpired': {
            'zh-cn': '用户凭据不正确或已过期，请重新登入。',
            'en-us': 'User credential incorrect or expired, please login again. '
        },
        'usernameAlreadyExist': {
            'zh-cn': '用户名已存在。',
            'en-us': 'Username already exist. '
        },
    }

    @classmethod
    def get_item(self, item, lang):
        return self.data[item][lang]

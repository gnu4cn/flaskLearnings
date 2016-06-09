# -*-coding: utf-8-*-
# 定义了这些常量：PRSN_CAT, POSITION, DEPARTMENT, SERVICE, TRNEE_RANK, RELATION
# RELIGION, GENDER, MARRIAGE, PPRT_TYPE, CERT_TYPE, EDU
MALE = '1'
FEMALE = '0'
ROLE_USER = 0
ROLE_ADMIN = 1
TOKEN_EXPIRE = 1200

class ConstantBase(object):

    data = NotImplemented

    @classmethod
    def get_list(self, locale):
        r = []

        for k in self.data.keys():
            t = {}
            t['id'] = k
            t['data'] = self.data[k][locale]
            r.append(t)

        return r

    @classmethod
    def get_by_id(self, id, locale):
        r = {}
        r['data'] = self.data[id][locale]
        r['id'] = id

        return r

class ARTICLE_CAT(ConstantBase):
    data = {
        '0': {
            'en': 'News',
            'zh-cn': u'新闻',
        },
        '1': {
            'en': 'Notices',
            'zh-cn': u'通知',
        },
    }

class PRSN_CAT(ConstantBase):
    data = {
        '0': {
            'en': 'Chinese - Staff',
            'zh-cn': '中方人员 - 工作人员',
        },
        '1': {
            'en': 'Chinese - Staff Family',
            'zh-cn': '中方人员 - 员工家属',
        },
        '2': {
            'en': 'Chinese - Others',
            'zh-cn': '中方人员 - 外部人员',
        },
        '5': {
            'en': 'Foreigner - Trainee',
            'zh-cn': '外籍人员 - 学员',
        },
        '6': {
            'en': 'Foreigner - Trainee Family',
            'zh-cn': '外籍人员 - 学员家属',
        },
        '7': {
            'en': 'Foreigner - Others',
            'zh-cn': '外籍人员 - 外部人员',
        },

    }

class DEPARTMENT(ConstantBase):
    data = {
        '0': {
            'zh-cn': '机关',
            'en': 'Head Office',
        },
        '1': {
            'zh-cn': '管理处',
            'en': 'Administrative Office',
        },
        '2': {
            'zh-cn': '学员队',
            'en': 'Trainee\'s Affairs Office',
        },
        '3': {
            'zh-cn': '客房部',
            'en': 'Housekeeping Service',
        },
        '4': {
            'zh-cn': '餐厅',
            'en': 'Food Service',
        },
        '5': {
            'zh-cn': '工程部',
            'en': 'Engineering Service',
        },
        '6': {
            'zh-cn': '保安',
            'en': 'Security Service',
        },
        '7': {
            'zh-cn': '教研室',
            'en': 'Teaching and Research Office',
        },
        '8': {
            'zh-cn': '厨房',
            'en': 'Cooking Service',
        },
    }

    @classmethod
    def get_sub_list(self, d_id, locale):
        r = []

        for k in POSITION.data.keys():
            t = {}
            if k.startswith(d_id):
                t['id'] = k
                t['position'] = POSITION.data[k][locale]

                r.append(t)

        return r

class POSITION(ConstantBase):
    data = {
        '00': {
            'zh-cn': '主任',
            'en': 'Director',
        },
        '01': {
            'en': 'Political Commissar',
            'zh-cn': '政委',
        },
        '02': {
            'zh-cn': '副主任',
            'en': 'Vice Director',
        },
        '10': {
            'zh-cn': '管理处处长',
            'en': 'Head of the Administration Office',
        },
        '04': {
            'zh-cn': '干事',
            'en': 'Administrative Secretary',
        },
        '05': {
            'zh-cn': '参谋',
            'en': 'Staff Officer',
        },
        '06': {
            'zh-cn': '助理',
            'en': 'Aissistant',
        },
        '07': {
            'zh-cn': '客房部经理',
            'en': 'Housekeeping Manager',
        },
        '08': {
            'zh-cn': '会计',
            'en': 'Accountant',
        },
        '09': {
            'zh-cn': '食堂管理员',
            'en': 'Canteean Administrator',
        },
        '0F': {
            'zh-cn': '机关其他人员',
            'en': 'Other Office members',
        },
        '11': {
            'zh-cn': '管理处参谋',
            'en': 'Staff Officer of Administration Office'
        },
        '12': {
            'zh-cn': '管理处人员',
            'en': 'Personnel of Ad. Office',
        },
    '13': {
        'zh-cn': '司机',
        'en': 'Driver',
    },
    '20': {
        'zh-cn': '学员队队长',
        'en': 'Head of Trainee\'s Affairs Office',
    },
    '21': {
        'zh-cn': '学员队助理',
        'en': 'Aissistant of Trainee\'s Affairs Office',
    },
    '30': {
        'zh-cn': '客房部服务员主管',
        'en': 'Head of Housekeeping Service',
    },
    '31': {
        'zh-cn': '客房部服务员',
        'en': 'Housekeeping Service',
    },
    '40': {
        'zh-cn': '餐厅服务员主管',
        'en': 'Head of Food Service',
    },
    '41': {
        'zh-cn': '餐厅服务员',
        'en': 'Food Service',
    },
    '50': {
        'zh-cn': '工程部主管',
        'en': 'Head of Engineering Department',
    },
    '51': {
        'zh-cn': '工程部工作人员',
        'en': 'Engineering Service',
    },
    '60': {
        'zh-cn': '保安主管',
        'en': 'Head of Security Service',
    },
    '61': {
        'zh-cn': '保安',
        'en': 'Security Service'
    },
    '70': {
        'zh-cn': '教研室主任',
        'en': 'Head of Teaching and Research Office',
    },
    '71': {
        'zh-cn': '教研室副主任',
        'en': 'Excutive Head of T. R. Office',
    },
    '72': {
        'zh-cn': '教员',
        'en': 'Instructor',
    },
    '80': {
        'zh-cn': '厨房负责人',
        'en': 'Head of Cooking Service',
    },
    '81': {
        'zh-cn': '厨师',
        'en': 'Chef',
    },
    '82': {
        'zh-cn': '帮厨',
        'en': 'Kitchen workers',
    },
    }

    @classmethod
    def get_by_id(self, id, locale):

        r = {}

        r['DEPARTMENT'] = DEPARTMENT.get_by_id(id[0], locale)

        r['data'] = self.data[id][locale]

        r['id'] = id

        return r


class PPRT_TYPE(ConstantBase):
    data = {
        '0': {
            'en': 'Diplomatic',
            'zh-cn': '外交',
        },
        '1': {
            'en': 'Official',
            'zh-cn': '公务',
        },
        '2': {
            'en': 'Passport(tourist/regular)',
            'zh-cn': '普通',
        },
        'F': {
            'en': 'Other',
            'zh-cn': '其它',
        },
    }

class CERT_TYPE(ConstantBase):
    data = {
        '0': {
            'en': 'Residence visa',
            'zh-cn': '居留登记',
        },
        '1': {
            'en': 'R',
            'zh-cn': 'R',
        },
        '2': {
            'en': 'Official visas',
            'zh-cn': '公务',
        },
        '3': {
            'en': 'Visa-free',
            'zh-cn': '免',
        },
        '4': {
            'en': 'F',
            'zh-cn': 'F',
        },
        '5': {
            'en': 'X1',
            'zh-cn': 'X1',
        },
        '6': {
            'en': 'S1',
            'zh-cn': 'S1',
        },
        '7': {
            'en': 'L',
            'zh-cn': 'L',
        },
    }

class RELIGION(ConstantBase):
    data = {
        '00': {
            'en': 'None',
            'zh-cn': '无',
        },
        '01': {
            'en': 'Taoism',
            'zh-cn': '道教',
        },
        '02': {
            'en': 'Buddism',
            'zh-cn': '佛教',
        },
        '03': {
            'en': 'Christianity',
            'zh-cn': '基督教',
        },
        '04': {
            'en': 'Catholicism',
            'zh-cn': '天主教',
        },
        '05': {
            'en': 'Islam',
            'zh-cn': '伊斯兰教',
        },
        '06': {
            'en': 'Hinduism',
            'zh-cn': '印度教',
        },
        '07': {
            'en': 'Orthodox Christianity',
            'zh-cn': '东正教',
        },
        '08': {
            'en': 'Roman Catholicism',
            'zh-cn': '罗马天主教',
        },
        'FF': {
            'en': 'Other',
            'zh-cn': '其它',
        },
    }

class SERVICE(ConstantBase):
    data = {
        '00': {
            'en': 'Army',
            'zh-cn': '陆军',
        },
        '01': {
            'en': 'Marine Corps',
            'zh-cn': '海军陆战队',
        },
        '02': {
            'en': 'Air Force',
            'zh-cn': '空军',
        },
        '03': {
            'en': 'Navy',
            'zh-cn': '海军',
        },
    }

    @classmethod
    def get_sub_list(self, s_id, locale):
        r = []

        for k in TRNEE_RANK.data.keys():
            t = {}
            if k.startswith(s_id):
                t['id'] = k
                t['data'] = TRNEE_RANK.data[k][locale]

                r.append(t)

        return r

class TRNEE_RANK(ConstantBase):
    data = {
        ##陆军
        '0000': {
            'en': 'General of the Army(GA)',
            'zh-cn': '元帅',
        },
        '0001': {
            'en': 'General(GEN)',
            'zh-cn': '上将',
        },
        '0002': {
            'en': 'Lieutenant General(LTG)',
            'zh-cn': '中将',
        },
        '0003': {
            'en': 'Major-general(MG)',
            'zh-cn': '少将',
        },
        '0004': {
            'en': 'Brigadier General(BG)',
            'zh-cn': '准将',
        },
        '0005': {
            'en': 'Senior Colonel(S. Col)',
            'zh-cn': '大校',
        },
        '0006': {
            'en': 'Colonel(COL)',
            'zh-cn': '上校',
        },
        '0007': {
            'en': 'Lieutenant Colonel(LTC)',
            'zh-cn': '中校',
        },
        '0008': {
            'en': 'Major(MAJ)',
            'zh-cn': '少校',
        },
        '0009': {
            'en': 'Captain(CPT)',
            'zh-cn': '上尉',
        },
        '000A': {
            'en': 'First Lieutenant(1LT)',
            'zh-cn': '中尉',
        },
        '000B': {
            'en': 'Second Lieutenant(2LT)',
            'zh-cn': '少尉',
        },
        '000C': {
            'en': 'Chief Warrant Officer 5(CW5)',
            'zh-cn': '五级准尉',
        },
    '000D': {
        'en': 'Chief Warrant Officer 4(CW4)',
        'zh-cn': '四级准尉',
    },
    '000E': {
        'en': 'Chief Warrant Officer 3(CW3)',
        'zh-cn': '三级准尉',
    },
    '000F': {
        'en': 'Chief Warrant Officer 2(CW2)',
        'zh-cn': '二级准尉',
    },
    '0010': {
        'en': 'Warrant Officer(WO1)',
        'zh-cn': '一级准尉',
    },
    '0011': {
        'en': 'Sergeant Major of the Army(SMA)',
        'zh-cn': '陆军总军士长',
    },
    '0012': {
        'en': 'Command Sergeant Major(CSM)',
        'zh-cn': '军士长',
    },
    '0013': {
        'en': 'Sergeant Major(SGM)',
        'zh-cn': '军士长',
    },
    '0014': {
        'en': 'First Sergeant(1SG)',
        'zh-cn': '军士长',
    },
    '0015': {
        'en': 'Master Sergeant(MSG)',
        'zh-cn': '军士长',
    },
    '0016': {
        'en': 'Sergeant First Class(SFC)',
        'zh-cn': '军士长',
    },
    '0017': {
        'en': 'Staff Sergeant(SSG)',
        'zh-cn': '上士',
    },
    '0018': {
        'en': 'Sergeant(SGT)',
        'zh-cn': '中士',
    },
    '0019': {
        'en': 'Corporal(CPL)',
        'zh-cn': '下士',
    },
    '001A': {
        'en': 'Specialist(SPC)',
        'zh-cn': '专业军士',
    },
    '001B': {
        'en': 'Private First Class(PFC)',
        'zh-cn': '一等兵',
    },
    '001C': {
        'en': 'Private 2(PV2)',
        'zh-cn': '二等兵',
    },
    '001D': {
        'en': 'Private(PV1)',
        'zh-cn': '新兵',
    },
    '00FF': {
        'en': 'Civilian Service',
        'zh-cn': '文职人员',
    },
    ##海军陆战队
    '0101': {
        'en': 'General(Gen)',
        'zh-cn': '上将',
    },
    '0102': {
        'en': 'Lieutenant General(LtGen)',
        'zh-cn': '中将',
    },
    '0103': {
        'en': 'Major-general(MajGen)',
        'zh-cn': '少将',
    },
    '0104': {
        'en': 'Brigadier General(BGen)',
        'zh-cn': '准将',
    },
    '0105': {
        'en': 'Senior Colonel(S. Col)',
        'zh-cn': '大校',
    },
    '0106': {
        'en': 'Colonel(Col)',
        'zh-cn': '上校',
    },
    '0107': {
        'en': 'Lieutenant Colonel(LtCol)',
        'zh-cn': '中校',
    },
    '0108': {
        'en': 'Major(Maj)',
        'zh-cn': '少校',
    },
    '0109': {
        'en': 'Captain(Capt)',
        'zh-cn': '上尉',
    },
    '010A': {
        'en': 'First Lieutenant(1stLt)',
        'zh-cn': '中尉',
    },
    '010B': {
        'en': 'Second Lieutenant(2ndLt)',
        'zh-cn': '少尉',
    },
    '010C': {
        'en': 'Chief Warrant Officer 5(CWO5)',
        'zh-cn': '五级准尉',
    },
    '010D': {
        'en': 'Chief Warrant Officer 4(CWO4)',
        'zh-cn': '四级准尉',
    },
    '010E': {
        'en': 'Chief Warrant Officer 3(CWO3)',
        'zh-cn': '三级准尉',
    },
    '010F': {
        'en': 'Chief Warrant Officer 2(CWO2)',
        'zh-cn': '二级准尉',
    },
    '0110': {
        'en': 'Warrant Officer(WO1)',
        'zh-cn': '一级准尉',
    },
    '0111': {
        'en': 'Sergeant Major of the Marine Corps(SgtMajMC)',
        'zh-cn': '军士长',
    },
    '0112': {
        'en': 'Master Gunnery Sergeant(MGySgt)',
        'zh-cn': '军士长',
    },
    '0113': {
        'en': 'First Sergeant(1stSgt)',
        'zh-cn': '军士长',
    },
    '0114': {
        'en': 'Master Sergeant(MSgt)',
        'zh-cn': '军士长',
    },
    '0115': {
        'en': 'Gunnery Sergeant(GySgt)',
        'zh-cn': '军士长',
    },
    '0116': {
        'en': 'Staff Sergeant(SSgt)',
        'zh-cn': '上士',
    },
    '0117': {
        'en': 'Sergeant(Sgt)',
        'zh-cn': '中士',
    },
    '0118': {
        'en': 'Corporal(Cpl)',
        'zh-cn': '下士',
    },
    '0119': {
        'en': 'Lance Corporal(LCpL)',
        'zh-cn': '准下士',
    },
    '011A': {
        'en': 'Private First Class(PFC)',
        'zh-cn': '一等兵',
    },
    '011B': {
        'en': 'Private(Pvt)',
        'zh-cn': '列兵',
    },
    '01FF': {
        'en': 'Civilian Service',
        'zh-cn': '文职人员',
    },
    ##空军
    '0200': {
        'en': 'General of the Air Force(GAF)',
        'zh-cn': '五星上将',
    },
    '0201': {
        'en': 'General(Gen)',
        'zh-cn': '上将',
    },
    '0202': {
        'en': 'Lieutenant General(Lt Ge)',
        'zh-cn': '中将',
    },
    '0203': {
        'en': 'Major General(Maj G)',
        'zh-cn': '少将',
    },
    '0204': {
        'en': 'Brigadier General(Brig)',
        'zh-cn': '准将',
    },
    '0206': {
        'en': 'Colonel(Col)',
        'zh-cn': '上校',
    },
    '0207': {
        'en': 'Lieutenant Colonel(Lt Co)',
        'zh-cn': '中校',
    },
    '0208': {
        'en': 'Major(Maj)',
        'zh-cn': '少校',
    },
    '0209': {
        'en': 'Captain(Capt)',
        'zh-cn': '上尉',
    },
    '020A': {
        'en': 'First Lieutenant(1st L)',
        'zh-cn': '中尉',
    },
    '020B': {
        'en': 'Second Lieutenant(2d Lt)',
        'zh-cn': '少尉',
    },
    '020C': {
        'en': 'Cadet',
        'zh-cn': '军校生',
    },
    '020D': {
        'en': 'Chief Master Sergeant of the Air Force(CMSAF)',
        'zh-cn': '空军总军士长',
    },
    '020E': {
        'en': 'Command Chief Master Sergeant(CCM)',
        'zh-cn': '指挥军士长',
    },
    '020F': {
        'en': 'Chief Master Sergeant(CMSgt)',
        'zh-cn': '一级军士长',
    },
    '0210': {
        'en': 'Senior Master Sergeant(SMSgt)',
        'zh-cn': '二级军士长',
    },
    '0211': {
        'en': 'Master Sergeant(MSgt)',
        'zh-cn': '三级军士长',
    },
    '0212': {
        'en': 'Technical Sergeant(Tsgt)',
        'zh-cn': '上士',
    },
    '0213': {
        'en': 'Staff Sergeant(SSgt)',
        'zh-cn': '中士',
    },
    '0214': {
        'en': 'Senior Airman(SrA)',
        'zh-cn': '下士',
    },
    '0215': {
        'en': 'Airman First Class(A1C)',
        'zh-cn': '一等兵',
    },
    '0216': {
        'en': 'Airman(Amn)',
        'zh-cn': '二等兵',
    },
    '0217': {
        'en': 'Airman Basic(AB)',
        'zh-cn': '三等兵',
    },
    '02FF': {
        'en': 'Civilian Service',
        'zh-cn': '文职人员',
    },
    ##海军
    '0300': {
        'en': 'Fleet Admiral(FADM)',
        'zh-cn': '五星上将',
    },
    '0301': {
        'en': 'Admiral(ADM)',
        'zh-cn': '上将',
    },
    '0302': {
        'en': 'Vice Admiral(VADM)',
        'zh-cn': '中奖',
    },
    '0303': {
        'en': 'Rear Admiral(Uper Half, RADM)',
        'zh-cn': '少将',
    },
    '0304': {
        'en': 'Rear Admiral(Lower Half, RADL)',
        'zh-cn': '准将',
    },
    '0305': {
        'en': 'Captain(CAPT)',
        'zh-cn': '上校',
    },
    '0306': {
        'en': 'Commander(CDR)',
        'zh-cn': '中校',
    },
    '0307': {
        'en': 'Lieutenant Commander(LCDR)',
        'zh-cn': '少校',
    },
    '0308': {
        'en': 'Lieutenant(LT)',
        'zh-cn': '上尉',
    },
    '0309': {
        'en': 'Lieutenant Junior Grade(LTJG)',
        'zh-cn': '中尉',
    },
    '030A': {
        'en': 'Ensign(ENS)',
        'zh-cn': '少尉',
    },
    '030B': {
        'en': 'Chief Warrant Officer(CWO5)',
        'zh-cn': '五级准尉',
    },
    '030C': {
        'en': 'Chief Warrant Officer(CWO4)',
        'zh-cn': '四级准尉',
    },
    '030D': {
        'en': 'Chief Warrant Officer(CWO3)',
        'zh-cn': '三级准尉',
    },
    '030E': {
        'en': 'Chief Warrant Officer(CWO2)',
        'zh-cn': '二级准尉',
    },
    '030F': {
        'en': 'Fleet/Commander Master Chief Petty Officer',
        'zh-cn': '总军士长',
    },
    '0310': {
        'en': 'Master Chief Petty Officer(MCPO)',
        'zh-cn': '副总军士长',
    },
    '0311': {
        'en': 'Second Chief Petty Officer(SCPO)',
        'zh-cn': '高级军士',
    },
    '0312': {
        'en': 'Chief Petty Officer(CPO)',
        'zh-cn': '上士',
    },
    '0313': {
        'en': 'Petty Officer 1st Class(PO1)',
        'zh-cn': '一等士官',
    },
    '0314': {
        'en': 'Petty Officer 2nd Class(PO2)',
        'zh-cn': '二等士官',
    },
    '0315': {
        'en': 'Petty Officer 3rd Class(PO3)',
        'zh-cn': '三等士官',
    },
    '0316': {
        'en': 'Seaman(SN)',
        'zh-cn': '水手'
    },
    '0317': {
        'en': 'Seaman Apprentice(SA)',
        'zh-cn': '见习水手',
    },
    '0318': {
        'en': 'Seaman Recruit(SR)',
        'zh-cn': '新水手',
    },
    '03FF': {
        'en': 'Civilian Service',
        'zh-cn': '文职人员',
    },
    }

    @classmethod
    def get_by_id(self, id, locale):

        r = {}

        s = SERVICE.get_by_id(id[:2], locale)
        r['SERVICE'] = s
        r['SERVICE_id'] = id[:2]

        s = self.data[id][locale]

        r['TRNEE_RANK'] = s
        r['TRNEE_RANK_id'] = id

        return r


class RELATION(ConstantBase):
    data = {
        '0': {
            'en': 'Father',
            'zh-cn': '父亲',
        },
        '1': {
            'en': 'Mother',
            'zh-cn': '母亲',
        },
        '2': {
            'en': 'Wife',
            'zh-cn': '妻子',
        },
        '3': {
            'en': 'Husband',
            'zh-cn': '丈夫',
        },
        '4': {
            'en': 'Son',
            'zh-cn': '儿子',
        },
        '5': {
            'en': 'Daughter',
            'zh-cn': '女儿',
        },
        '6': {
            'en': 'Elder sister',
            'zh-cn': '姐姐',
        },
        '7': {
            'en': 'Younger sister',
            'zh-cn': '妹妹',
        },
        '8': {
            'en': 'Elder brother',
            'zh-cn': '哥哥',
        },
        '9': {
            'en': 'Younger brother',
            'zh-cn': '弟弟',
        },
    }


class EDU(ConstantBase):
    data = {
        '5': {
            'en': 'High school',
            'zh-cn': '高中',
        },
        '4': {
            'en': 'Junior College',
            'zh-cn': '大专',
        },
        '3': {
            'en': 'Bachelor degree',
            'zh-cn': '学士学位',
        },
        '2': {
            'en': 'Master degree',
            'zh-cn': '硕士学位',
        },
        '1': {
            'en': 'Doctor degree',
            'zh-cn': '博士学位',
        },
        '0': {
            'en': 'Post Ph. D',
            'zh-cn': '博士后',
        },
    }

class GENDER(ConstantBase):
    data = {
        '0': {
            'en': 'Female',
            'zh-cn': '女',
        },
        '1': {
            'en': 'Male',
            'zh-cn': '男',
        },
    }

class MARRIAGE(ConstantBase):
    data = {
        '0': {
            'en': 'Single',
            'zh-cn': '未婚',
        },
        '1': {
            'en': 'Married',
            'zh-cn': '已婚',
        },
    }

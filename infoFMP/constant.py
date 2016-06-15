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
            'en-us': 'News',
            'zh-cn': u'新闻',
        },
        '1': {
            'en-us': 'Notices',
            'zh-cn': u'通知',
        },
    }

class PRSN_CAT(ConstantBase):
    data = {
        '0': {
            'en-us': 'Chinese - Staff',
            'zh-cn': '中方人员 - 工作人员',
        },
        '1': {
            'en-us': 'Chinese - Staff Family',
            'zh-cn': '中方人员 - 员工家属',
        },
        '2': {
            'en-us': 'Chinese - Others',
            'zh-cn': '中方人员 - 外部人员',
        },
        '5': {
            'en-us': 'Foreigner - Trainee',
            'zh-cn': '外籍人员 - 学员',
        },
        '6': {
            'en-us': 'Foreigner - Trainee Family',
            'zh-cn': '外籍人员 - 学员家属',
        },
        '7': {
            'en-us': 'Foreigner - Others',
            'zh-cn': '外籍人员 - 外部人员',
        },

    }

class DEPARTMENT(ConstantBase):
    data = {
        '0': {
            'zh-cn': '机关',
            'en-us': 'Head Office',
        },
        '1': {
            'zh-cn': '管理处',
            'en-us': 'Administrative Office',
        },
        '2': {
            'zh-cn': '学员队',
            'en-us': 'Trainee\'s Affairs Office',
        },
        '3': {
            'zh-cn': '客房部',
            'en-us': 'Housekeeping Service',
        },
        '4': {
            'zh-cn': '餐厅',
            'en-us': 'Food Service',
        },
        '5': {
            'zh-cn': '工程部',
            'en-us': 'Engineering Service',
        },
        '6': {
            'zh-cn': '保安',
            'en-us': 'Security Service',
        },
        '7': {
            'zh-cn': '教研室',
            'en-us': 'Teaching and Research Office',
        },
        '8': {
            'zh-cn': '厨房',
            'en-us': 'Cooking Service',
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
            'en-us': 'Director',
        },
        '01': {
            'en-us': 'Political Commissar',
            'zh-cn': '政委',
        },
        '02': {
            'zh-cn': '副主任',
            'en-us': 'Vice Director',
        },
        '10': {
            'zh-cn': '管理处处长',
            'en-us': 'Head of the Administration Office',
        },
        '04': {
            'zh-cn': '干事',
            'en-us': 'Administrative Secretary',
        },
        '05': {
            'zh-cn': '参谋',
            'en-us': 'Staff Officer',
        },
        '06': {
            'zh-cn': '助理',
            'en-us': 'Aissistant',
        },
        '07': {
            'zh-cn': '客房部经理',
            'en-us': 'Housekeeping Manager',
        },
        '08': {
            'zh-cn': '会计',
            'en-us': 'Accountant',
        },
        '09': {
            'zh-cn': '食堂管理员',
            'en-us': 'Canteean Administrator',
        },
        '0F': {
            'zh-cn': '机关其他人员',
            'en-us': 'Other Office members',
        },
        '11': {
            'zh-cn': '管理处参谋',
            'en-us': 'Staff Officer of Administration Office'
        },
        '12': {
            'zh-cn': '管理处人员',
            'en-us': 'Personnel of Ad. Office',
        },
    '13': {
        'zh-cn': '司机',
        'en-us': 'Driver',
    },
    '20': {
        'zh-cn': '学员队队长',
        'en-us': 'Head of Trainee\'s Affairs Office',
    },
    '21': {
        'zh-cn': '学员队助理',
        'en-us': 'Aissistant of Trainee\'s Affairs Office',
    },
    '30': {
        'zh-cn': '客房部服务员主管',
        'en-us': 'Head of Housekeeping Service',
    },
    '31': {
        'zh-cn': '客房部服务员',
        'en-us': 'Housekeeping Service',
    },
    '40': {
        'zh-cn': '餐厅服务员主管',
        'en-us': 'Head of Food Service',
    },
    '41': {
        'zh-cn': '餐厅服务员',
        'en-us': 'Food Service',
    },
    '50': {
        'zh-cn': '工程部主管',
        'en-us': 'Head of Engineering Department',
    },
    '51': {
        'zh-cn': '工程部工作人员',
        'en-us': 'Engineering Service',
    },
    '60': {
        'zh-cn': '保安主管',
        'en-us': 'Head of Security Service',
    },
    '61': {
        'zh-cn': '保安',
        'en-us': 'Security Service'
    },
    '70': {
        'zh-cn': '教研室主任',
        'en-us': 'Head of Teaching and Research Office',
    },
    '71': {
        'zh-cn': '教研室副主任',
        'en-us': 'Excutive Head of T. R. Office',
    },
    '72': {
        'zh-cn': '教员',
        'en-us': 'Instructor',
    },
    '80': {
        'zh-cn': '厨房负责人',
        'en-us': 'Head of Cooking Service',
    },
    '81': {
        'zh-cn': '厨师',
        'en-us': 'Chef',
    },
    '82': {
        'zh-cn': '帮厨',
        'en-us': 'Kitchen workers',
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
            'en-us': 'Diplomatic',
            'zh-cn': '外交',
        },
        '1': {
            'en-us': 'Official',
            'zh-cn': '公务',
        },
        '2': {
            'en-us': 'Passport(tourist/regular)',
            'zh-cn': '普通',
        },
        'F': {
            'en-us': 'Other',
            'zh-cn': '其它',
        },
    }

class CERT_TYPE(ConstantBase):
    data = {
        '0': {
            'en-us': 'Residence visa',
            'zh-cn': '居留登记',
        },
        '1': {
            'en-us': 'R',
            'zh-cn': 'R',
        },
        '2': {
            'en-us': 'Official visas',
            'zh-cn': '公务',
        },
        '3': {
            'en-us': 'Visa-free',
            'zh-cn': '免',
        },
        '4': {
            'en-us': 'F',
            'zh-cn': 'F',
        },
        '5': {
            'en-us': 'X1',
            'zh-cn': 'X1',
        },
        '6': {
            'en-us': 'S1',
            'zh-cn': 'S1',
        },
        '7': {
            'en-us': 'L',
            'zh-cn': 'L',
        },
    }

class RELIGION(ConstantBase):
    data = {
        '00': {
            'en-us': 'None',
            'zh-cn': '无',
        },
        '01': {
            'en-us': 'Taoism',
            'zh-cn': '道教',
        },
        '02': {
            'en-us': 'Buddism',
            'zh-cn': '佛教',
        },
        '03': {
            'en-us': 'Christianity',
            'zh-cn': '基督教',
        },
        '04': {
            'en-us': 'Catholicism',
            'zh-cn': '天主教',
        },
        '05': {
            'en-us': 'Islam',
            'zh-cn': '伊斯兰教',
        },
        '06': {
            'en-us': 'Hinduism',
            'zh-cn': '印度教',
        },
        '07': {
            'en-us': 'Orthodox Christianity',
            'zh-cn': '东正教',
        },
        '08': {
            'en-us': 'Roman Catholicism',
            'zh-cn': '罗马天主教',
        },
        'FF': {
            'en-us': 'Other',
            'zh-cn': '其它',
        },
    }

class SERVICE(ConstantBase):
    data = {
        '00': {
            'en-us': 'Army',
            'zh-cn': '陆军',
        },
        '01': {
            'en-us': 'Marine Corps',
            'zh-cn': '海军陆战队',
        },
        '02': {
            'en-us': 'Air Force',
            'zh-cn': '空军',
        },
        '03': {
            'en-us': 'Navy',
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
            'en-us': 'General of the Army(GA)',
            'zh-cn': '元帅',
        },
        '0001': {
            'en-us': 'General(GEN)',
            'zh-cn': '上将',
        },
        '0002': {
            'en-us': 'Lieutenant General(LTG)',
            'zh-cn': '中将',
        },
        '0003': {
            'en-us': 'Major-general(MG)',
            'zh-cn': '少将',
        },
        '0004': {
            'en-us': 'Brigadier General(BG)',
            'zh-cn': '准将',
        },
        '0005': {
            'en-us': 'Senior Colonel(S. Col)',
            'zh-cn': '大校',
        },
        '0006': {
            'en-us': 'Colonel(COL)',
            'zh-cn': '上校',
        },
        '0007': {
            'en-us': 'Lieutenant Colonel(LTC)',
            'zh-cn': '中校',
        },
        '0008': {
            'en-us': 'Major(MAJ)',
            'zh-cn': '少校',
        },
        '0009': {
            'en-us': 'Captain(CPT)',
            'zh-cn': '上尉',
        },
        '000A': {
            'en-us': 'First Lieutenant(1LT)',
            'zh-cn': '中尉',
        },
        '000B': {
            'en-us': 'Second Lieutenant(2LT)',
            'zh-cn': '少尉',
        },
        '000C': {
            'en-us': 'Chief Warrant Officer 5(CW5)',
            'zh-cn': '五级准尉',
        },
    '000D': {
        'en-us': 'Chief Warrant Officer 4(CW4)',
        'zh-cn': '四级准尉',
    },
    '000E': {
        'en-us': 'Chief Warrant Officer 3(CW3)',
        'zh-cn': '三级准尉',
    },
    '000F': {
        'en-us': 'Chief Warrant Officer 2(CW2)',
        'zh-cn': '二级准尉',
    },
    '0010': {
        'en-us': 'Warrant Officer(WO1)',
        'zh-cn': '一级准尉',
    },
    '0011': {
        'en-us': 'Sergeant Major of the Army(SMA)',
        'zh-cn': '陆军总军士长',
    },
    '0012': {
        'en-us': 'Command Sergeant Major(CSM)',
        'zh-cn': '军士长',
    },
    '0013': {
        'en-us': 'Sergeant Major(SGM)',
        'zh-cn': '军士长',
    },
    '0014': {
        'en-us': 'First Sergeant(1SG)',
        'zh-cn': '军士长',
    },
    '0015': {
        'en-us': 'Master Sergeant(MSG)',
        'zh-cn': '军士长',
    },
    '0016': {
        'en-us': 'Sergeant First Class(SFC)',
        'zh-cn': '军士长',
    },
    '0017': {
        'en-us': 'Staff Sergeant(SSG)',
        'zh-cn': '上士',
    },
    '0018': {
        'en-us': 'Sergeant(SGT)',
        'zh-cn': '中士',
    },
    '0019': {
        'en-us': 'Corporal(CPL)',
        'zh-cn': '下士',
    },
    '001A': {
        'en-us': 'Specialist(SPC)',
        'zh-cn': '专业军士',
    },
    '001B': {
        'en-us': 'Private First Class(PFC)',
        'zh-cn': '一等兵',
    },
    '001C': {
        'en-us': 'Private 2(PV2)',
        'zh-cn': '二等兵',
    },
    '001D': {
        'en-us': 'Private(PV1)',
        'zh-cn': '新兵',
    },
    '00FF': {
        'en-us': 'Civilian Service',
        'zh-cn': '文职人员',
    },
    ##海军陆战队
    '0101': {
        'en-us': 'General(Gen)',
        'zh-cn': '上将',
    },
    '0102': {
        'en-us': 'Lieutenant General(LtGen)',
        'zh-cn': '中将',
    },
    '0103': {
        'en-us': 'Major-general(MajGen)',
        'zh-cn': '少将',
    },
    '0104': {
        'en-us': 'Brigadier General(BGen)',
        'zh-cn': '准将',
    },
    '0105': {
        'en-us': 'Senior Colonel(S. Col)',
        'zh-cn': '大校',
    },
    '0106': {
        'en-us': 'Colonel(Col)',
        'zh-cn': '上校',
    },
    '0107': {
        'en-us': 'Lieutenant Colonel(LtCol)',
        'zh-cn': '中校',
    },
    '0108': {
        'en-us': 'Major(Maj)',
        'zh-cn': '少校',
    },
    '0109': {
        'en-us': 'Captain(Capt)',
        'zh-cn': '上尉',
    },
    '010A': {
        'en-us': 'First Lieutenant(1stLt)',
        'zh-cn': '中尉',
    },
    '010B': {
        'en-us': 'Second Lieutenant(2ndLt)',
        'zh-cn': '少尉',
    },
    '010C': {
        'en-us': 'Chief Warrant Officer 5(CWO5)',
        'zh-cn': '五级准尉',
    },
    '010D': {
        'en-us': 'Chief Warrant Officer 4(CWO4)',
        'zh-cn': '四级准尉',
    },
    '010E': {
        'en-us': 'Chief Warrant Officer 3(CWO3)',
        'zh-cn': '三级准尉',
    },
    '010F': {
        'en-us': 'Chief Warrant Officer 2(CWO2)',
        'zh-cn': '二级准尉',
    },
    '0110': {
        'en-us': 'Warrant Officer(WO1)',
        'zh-cn': '一级准尉',
    },
    '0111': {
        'en-us': 'Sergeant Major of the Marine Corps(SgtMajMC)',
        'zh-cn': '军士长',
    },
    '0112': {
        'en-us': 'Master Gunnery Sergeant(MGySgt)',
        'zh-cn': '军士长',
    },
    '0113': {
        'en-us': 'First Sergeant(1stSgt)',
        'zh-cn': '军士长',
    },
    '0114': {
        'en-us': 'Master Sergeant(MSgt)',
        'zh-cn': '军士长',
    },
    '0115': {
        'en-us': 'Gunnery Sergeant(GySgt)',
        'zh-cn': '军士长',
    },
    '0116': {
        'en-us': 'Staff Sergeant(SSgt)',
        'zh-cn': '上士',
    },
    '0117': {
        'en-us': 'Sergeant(Sgt)',
        'zh-cn': '中士',
    },
    '0118': {
        'en-us': 'Corporal(Cpl)',
        'zh-cn': '下士',
    },
    '0119': {
        'en-us': 'Lance Corporal(LCpL)',
        'zh-cn': '准下士',
    },
    '011A': {
        'en-us': 'Private First Class(PFC)',
        'zh-cn': '一等兵',
    },
    '011B': {
        'en-us': 'Private(Pvt)',
        'zh-cn': '列兵',
    },
    '01FF': {
        'en-us': 'Civilian Service',
        'zh-cn': '文职人员',
    },
    ##空军
    '0200': {
        'en-us': 'General of the Air Force(GAF)',
        'zh-cn': '五星上将',
    },
    '0201': {
        'en-us': 'General(Gen)',
        'zh-cn': '上将',
    },
    '0202': {
        'en-us': 'Lieutenant General(Lt Ge)',
        'zh-cn': '中将',
    },
    '0203': {
        'en-us': 'Major General(Maj G)',
        'zh-cn': '少将',
    },
    '0204': {
        'en-us': 'Brigadier General(Brig)',
        'zh-cn': '准将',
    },
    '0206': {
        'en-us': 'Colonel(Col)',
        'zh-cn': '上校',
    },
    '0207': {
        'en-us': 'Lieutenant Colonel(Lt Co)',
        'zh-cn': '中校',
    },
    '0208': {
        'en-us': 'Major(Maj)',
        'zh-cn': '少校',
    },
    '0209': {
        'en-us': 'Captain(Capt)',
        'zh-cn': '上尉',
    },
    '020A': {
        'en-us': 'First Lieutenant(1st L)',
        'zh-cn': '中尉',
    },
    '020B': {
        'en-us': 'Second Lieutenant(2d Lt)',
        'zh-cn': '少尉',
    },
    '020C': {
        'en-us': 'Cadet',
        'zh-cn': '军校生',
    },
    '020D': {
        'en-us': 'Chief Master Sergeant of the Air Force(CMSAF)',
        'zh-cn': '空军总军士长',
    },
    '020E': {
        'en-us': 'Command Chief Master Sergeant(CCM)',
        'zh-cn': '指挥军士长',
    },
    '020F': {
        'en-us': 'Chief Master Sergeant(CMSgt)',
        'zh-cn': '一级军士长',
    },
    '0210': {
        'en-us': 'Senior Master Sergeant(SMSgt)',
        'zh-cn': '二级军士长',
    },
    '0211': {
        'en-us': 'Master Sergeant(MSgt)',
        'zh-cn': '三级军士长',
    },
    '0212': {
        'en-us': 'Technical Sergeant(Tsgt)',
        'zh-cn': '上士',
    },
    '0213': {
        'en-us': 'Staff Sergeant(SSgt)',
        'zh-cn': '中士',
    },
    '0214': {
        'en-us': 'Senior Airman(SrA)',
        'zh-cn': '下士',
    },
    '0215': {
        'en-us': 'Airman First Class(A1C)',
        'zh-cn': '一等兵',
    },
    '0216': {
        'en-us': 'Airman(Amn)',
        'zh-cn': '二等兵',
    },
    '0217': {
        'en-us': 'Airman Basic(AB)',
        'zh-cn': '三等兵',
    },
    '02FF': {
        'en-us': 'Civilian Service',
        'zh-cn': '文职人员',
    },
    ##海军
    '0300': {
        'en-us': 'Fleet Admiral(FADM)',
        'zh-cn': '五星上将',
    },
    '0301': {
        'en-us': 'Admiral(ADM)',
        'zh-cn': '上将',
    },
    '0302': {
        'en-us': 'Vice Admiral(VADM)',
        'zh-cn': '中奖',
    },
    '0303': {
        'en-us': 'Rear Admiral(Uper Half, RADM)',
        'zh-cn': '少将',
    },
    '0304': {
        'en-us': 'Rear Admiral(Lower Half, RADL)',
        'zh-cn': '准将',
    },
    '0305': {
        'en-us': 'Captain(CAPT)',
        'zh-cn': '上校',
    },
    '0306': {
        'en-us': 'Commander(CDR)',
        'zh-cn': '中校',
    },
    '0307': {
        'en-us': 'Lieutenant Commander(LCDR)',
        'zh-cn': '少校',
    },
    '0308': {
        'en-us': 'Lieutenant(LT)',
        'zh-cn': '上尉',
    },
    '0309': {
        'en-us': 'Lieutenant Junior Grade(LTJG)',
        'zh-cn': '中尉',
    },
    '030A': {
        'en-us': 'Ensign(ENS)',
        'zh-cn': '少尉',
    },
    '030B': {
        'en-us': 'Chief Warrant Officer(CWO5)',
        'zh-cn': '五级准尉',
    },
    '030C': {
        'en-us': 'Chief Warrant Officer(CWO4)',
        'zh-cn': '四级准尉',
    },
    '030D': {
        'en-us': 'Chief Warrant Officer(CWO3)',
        'zh-cn': '三级准尉',
    },
    '030E': {
        'en-us': 'Chief Warrant Officer(CWO2)',
        'zh-cn': '二级准尉',
    },
    '030F': {
        'en-us': 'Fleet/Commander Master Chief Petty Officer',
        'zh-cn': '总军士长',
    },
    '0310': {
        'en-us': 'Master Chief Petty Officer(MCPO)',
        'zh-cn': '副总军士长',
    },
    '0311': {
        'en-us': 'Second Chief Petty Officer(SCPO)',
        'zh-cn': '高级军士',
    },
    '0312': {
        'en-us': 'Chief Petty Officer(CPO)',
        'zh-cn': '上士',
    },
    '0313': {
        'en-us': 'Petty Officer 1st Class(PO1)',
        'zh-cn': '一等士官',
    },
    '0314': {
        'en-us': 'Petty Officer 2nd Class(PO2)',
        'zh-cn': '二等士官',
    },
    '0315': {
        'en-us': 'Petty Officer 3rd Class(PO3)',
        'zh-cn': '三等士官',
    },
    '0316': {
        'en-us': 'Seaman(SN)',
        'zh-cn': '水手'
    },
    '0317': {
        'en-us': 'Seaman Apprentice(SA)',
        'zh-cn': '见习水手',
    },
    '0318': {
        'en-us': 'Seaman Recruit(SR)',
        'zh-cn': '新水手',
    },
    '03FF': {
        'en-us': 'Civilian Service',
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
            'en-us': 'Father',
            'zh-cn': '父亲',
        },
        '1': {
            'en-us': 'Mother',
            'zh-cn': '母亲',
        },
        '2': {
            'en-us': 'Wife',
            'zh-cn': '妻子',
        },
        '3': {
            'en-us': 'Husband',
            'zh-cn': '丈夫',
        },
        '4': {
            'en-us': 'Son',
            'zh-cn': '儿子',
        },
        '5': {
            'en-us': 'Daughter',
            'zh-cn': '女儿',
        },
        '6': {
            'en-us': 'Elder sister',
            'zh-cn': '姐姐',
        },
        '7': {
            'en-us': 'Younger sister',
            'zh-cn': '妹妹',
        },
        '8': {
            'en-us': 'Elder brother',
            'zh-cn': '哥哥',
        },
        '9': {
            'en-us': 'Younger brother',
            'zh-cn': '弟弟',
        },
    }


class EDU(ConstantBase):
    data = {
        '5': {
            'en-us': 'High school',
            'zh-cn': '高中',
        },
        '4': {
            'en-us': 'Junior College',
            'zh-cn': '大专',
        },
        '3': {
            'en-us': 'Bachelor degree',
            'zh-cn': '学士学位',
        },
        '2': {
            'en-us': 'Master degree',
            'zh-cn': '硕士学位',
        },
        '1': {
            'en-us': 'Doctor degree',
            'zh-cn': '博士学位',
        },
        '0': {
            'en-us': 'Post Ph. D',
            'zh-cn': '博士后',
        },
    }

class GENDER(ConstantBase):
    data = {
        '0': {
            'en-us': 'Female',
            'zh-cn': '女',
        },
        '1': {
            'en-us': 'Male',
            'zh-cn': '男',
        },
    }

class MARRIAGE(ConstantBase):
    data = {
        '0': {
            'en-us': 'Single',
            'zh-cn': '未婚',
        },
        '1': {
            'en-us': 'Married',
            'zh-cn': '已婚',
        },
    }

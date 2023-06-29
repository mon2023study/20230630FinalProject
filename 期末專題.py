# 引入所需的模組
from flask import Flask, request, render_template, jsonify
#from flask_bootstrap import Bootstrap
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, IntegerField
#from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, NumberRange
#from wtforms.fields import FieldList, FormField
from wtforms.fields import DateField, FieldList, FormField


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from bs4 import BeautifulSoup
import datetime
import requests

# 建立 Flask 應用程式物件
app = Flask(__name__)
# 設定密鑰
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?' \
'driver=ODBC+Driver+17+for+SQL+Server&' \
'trusted_connection=yes&' \
'charset=utf8&' \
'server=LAPTOP-K92SIUII&' \
'database=2024vote'
#'charset=utf8mb4_unicode_ci&' \

# 初始化 Flask-Bootstrap
bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)

class Questionnaire(db.Model):
    __tablename__ = 'questionnaire'
    id_number = db.Column(db.String(10), primary_key=True)
    birthday = db.Column(db.Date)
    gender = db.Column(db.NVARCHAR(1))
    county = db.Column(db.NVARCHAR(10 ))
    district = db.Column(db.NVARCHAR(10 ))
    education = db.Column(db.NVARCHAR(10))
    party1 = db.Column(db.NVARCHAR(10))
    monthly_income = db.Column(db.Integer)
    annual_income = db.Column(db.Integer)
    reason1 = db.Column(db.NVARCHAR( ))
    video1 = db.Column(db.Boolean)
    video2 = db.Column(db.Boolean)
    video3 = db.Column(db.Boolean)
    party2 = db.Column(db.NVARCHAR(10))
    reason2 = db.Column(db.NVARCHAR( ))
    preference1 = db.Column(db.String(10))
    preference2 = db.Column(db.String(10))
    watch = db.Column(db.String(5))
    media_literacy = db.Column(db.String(5))
    fact_checking = db.Column(db.String(5))
    perspective_taking = db.Column(db.String(5))
    other_comments = db.Column(db.NVARCHAR( ))

with app.app_context():
    db.create_all()
    print("ca")

# 建立表單類別
class QuestionnaireForm(FlaskForm):
    candidates = ['柯文哲', '侯友宜', '賴清德']
    radio_yn = [(True, '是'), (False, '否')];
    # 身分證字號欄位
    id_number = StringField('身分證字號:', validators=[DataRequired(), Length(10,10)])
    # 生日欄位
    birthday = DateField('生日:', validators=[DataRequired()])
    # 性別欄位
    gender = RadioField('性別:', choices=[('男', '男'), ('女', '女')], validators=[DataRequired()])
    
    # 縣市調查
    county = SelectField('縣市', validate_choice=False, coerce=str, choices=[('default', '請選擇')])
    district = SelectField('區域', validate_choice=False, coerce=str, choices=[('default', '請選擇')])

    # 教育程度欄位
    education = RadioField('教育程度:', choices=[('國小以下', '國小以下'), ('國中', '國中'), ('高中/職', '高中/職'), ('大專院校', '大專院校'), ('碩士', '碩士'), ('博士', '博士')], validators=[DataRequired()])
    # 政黨傾向欄位
    party1 = RadioField('政黨傾向:', choices=[('民眾黨', '民眾黨'), ('國民黨', '國民黨'), ('民進黨', '民進黨'), ('其他', '其他')], validators=[DataRequired()])
    # 月收欄位
    monthly_income = IntegerField('月收:', validators=[DataRequired(),NumberRange(min=0)])
    # 年收欄位
    annual_income = IntegerField('年收:', validators=[DataRequired(),NumberRange(min=0)])
    # 選擇的原因欄位
    reason1 = TextAreaField('選擇的原因:', validators=[DataRequired()])
    # 是否看過候選人的相關影片欄位
    video1 = BooleanField('柯文哲')
    video2 = BooleanField('侯友宜')
    video3 = BooleanField('賴清德')
    # 看過之後政黨傾向欄位
    party2 = RadioField('看過之後政黨傾向:', choices=[('民眾黨', '民眾黨'), ('國民黨', '國民黨'), ('民進黨', '民進黨'), ('其他', '其他')], validators=[DataRequired()])
    # 選擇的原因欄位
    reason2 = TextAreaField('看完後選擇的原因:')
    # 偏好欄位（觀看政見前/後）
    preference1 = FieldList(RadioField('偏好:', choices=[(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')], validators=[DataRequired()]), min_entries=3)
    preference2 = FieldList(RadioField('偏好:', choices=[(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')], validators=[DataRequired()]), min_entries=3)
    
    # 選民素質調查
    watch = RadioField('您是否會主動查詢各候選人的政見', choices=radio_yn)
    media_literacy = RadioField('您是否有媒體識讀的能力', choices=radio_yn)
    fact_checking = RadioField('您是否會主動查證新聞內容', choices=radio_yn)
    perspective_taking = RadioField('平常看新聞有檢視各方看法並分析的習慣', choices=radio_yn)
    # 其他想說的欄位
    other_comments = TextAreaField('其他想說的:')
    submit = SubmitField('提交')

# 建立路由函式
@app.route('/', methods=['GET', 'POST'])
def index():
    # 建立表單物件
    form = QuestionnaireForm()
    # 如果表單驗證通過，則處理表單資料
    if form.validate_on_submit():
        if request.method == 'POST':
            # 獲取表單數據
            id_number = form.id_number.data
            birthday = form.birthday.data
            gender = form.gender.data
            county = form.county.data
            district = form.district.data
            education = form.education.data
            party1 = form.party1.data
            monthly_income = form.monthly_income.data
            annual_income = form.annual_income.data
            reason1 = form.reason1.data
            video1 = form.video1.data
            video2 = form.video2.data
            video3 = form.video3.data
            party2 = form.party2.data
            reason2 = form.reason2.data
            preference1_list = [field.data for field in form.preference1]
            preference1_str = ','.join(preference1_list)
            preference2_list = [field.data for field in form.preference2]
            preference2_str = ','.join(preference2_list)
            watch = form.watch.data
            media_literacy = form.media_literacy.data
            fact_checking = form.fact_checking.data
            perspective_taking = form.perspective_taking.data
            other_comments= form.other_comments.data

            # 創建數據模型對象，並賦值表單數據
            questionnaire= Questionnaire(
            id_number=id_number,
            birthday=birthday,
            gender=gender,
            county=county,
            district=district,
            education=education,
            party1=party1,
            monthly_income=monthly_income,
            annual_income=annual_income,
            reason1=reason1,
            video1=video1,
            video2=video2,
            video3=video3,
            party2=party2,
            reason2=reason2,
            preference1=preference1_str,
            preference2=preference2_str,
            watch=watch,
            media_literacy=media_literacy,
            fact_checking=fact_checking,
            perspective_taking=perspective_taking,
            other_comments=other_comments
            )
            try:
                # 將數據模型對象添加到數據庫會話中
                db.session.add(questionnaire)
                # 提交數據庫會話
                db.session.commit()
                return render_template('done.html', form=form)
                
            except IntegrityError:
                db.session.rollback()
                return render_template('vote.html', form=form,msg='該身份證字號已投票')
    # return redirect(url_for('success'))
    # 如果表單驗證失敗，則渲染模板來顯示表單和錯誤訊息
    return render_template('vote.html', form=form)

@app.route('/api/wiki',methods=['GET'])
def api_wiki():
    url = 'https://zh.wikipedia.org/wiki/2024年中華民國總統選舉民意調查'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    rows = table.findAll('tr')
    data = []
    for row in rows:
        cols = row.findAll('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    return jsonify(data)

@app.route('/api/result',methods=['GET'])
def api_result():
    qf = Questionnaire.query.all()
    def calculate_age(today,birthday):
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    # 計算年齡層
    def calculate_age_group(age):
        if age < 20:
            return '20以下'
        elif age < 30:
            return '20-29'
        elif age < 40:
            return '30-39'
        elif age < 50:
            return '40-49'
        elif age < 60:
            return '50-59'
        else:
            return '60以上'
    # 計算各年齡層人數
    group_dict = {
        '年齡':{'20以下': 0, '20-29': 0, '30-39': 0, '40-49': 0, '50-59': 0, '60以上': 0},
        '性別':{'男':0,'女':0},
        '縣市':{},
        '教育程度':{'國小以下': 0,'國中': 0, '高中/職': 0, '大專院校': 0, '碩士': 0, '博士': 0},
        '觀看政見前':{'民眾黨': 0, '國民黨': 0, '民進黨': 0, '其他': 0},
        '觀看政見後':{'民眾黨': 0, '國民黨': 0, '民進黨': 0, '其他': 0},
        '主動查詢各候選人的政見':{},
        '媒體識讀能力':{},
        '查證新聞內容':{},
        '檢視各方看法並分析':{},
        '候選人評分1':{'柯文哲':{'1':0,'2':0,'3':0,'4':0,'5':0},'侯友宜':{'1':0,'2':0,'3':0,'4':0,'5':0},'賴清德':{'1':0,'2':0,'3':0,'4':0,'5':0}},
        '候選人評分2':{'柯文哲':{'1':0,'2':0,'3':0,'4':0,'5':0},'侯友宜':{'1':0,'2':0,'3':0,'4':0,'5':0},'賴清德':{'1':0,'2':0,'3':0,'4':0,'5':0}}
    }

    today = datetime.date.today()
    for data in qf:
        group_dict['年齡'][calculate_age_group(calculate_age(today,data.birthday))] += 1
        group_dict['性別'][data.gender] += 1
        if data.county not in group_dict['縣市']:
            group_dict['縣市'][data.county] = 0
        group_dict['縣市'][data.county] += 1
        group_dict['教育程度'][data.education] += 1
        group_dict['觀看政見前'][data.party1] += 1
        group_dict['觀看政見後'][data.party2] += 1
        
        if data.watch not in group_dict['主動查詢各候選人的政見']:
            group_dict['主動查詢各候選人的政見'][data.watch] = 0
        group_dict['主動查詢各候選人的政見'][data.watch] += 1

        if data.media_literacy not in group_dict['媒體識讀能力']:
            group_dict['媒體識讀能力'][data.media_literacy] = 0
        group_dict['媒體識讀能力'][data.media_literacy] += 1

        if data.fact_checking not in group_dict['查證新聞內容']:
            group_dict['查證新聞內容'][data.fact_checking] = 0
        group_dict['查證新聞內容'][data.fact_checking] += 1

        if data.perspective_taking not in group_dict['檢視各方看法並分析']:
            group_dict['檢視各方看法並分析'][data.perspective_taking] = 0
        group_dict['檢視各方看法並分析'][data.perspective_taking] += 1

        preference1 = data.preference1.split(',')
        group_dict['候選人評分1']['柯文哲'][preference1[0]] += 1
        group_dict['候選人評分1']['侯友宜'][preference1[1]] += 1
        group_dict['候選人評分1']['賴清德'][preference1[2]] += 1

        preference2 = data.preference2.split(',')
        group_dict['候選人評分2']['柯文哲'][preference2[0]] += 1
        group_dict['候選人評分2']['侯友宜'][preference2[1]] += 1
        group_dict['候選人評分2']['賴清德'][preference2[2]] += 1
    
    # 回傳結果
    #{'20以下': age_group_dict['20以下'], '20-29': age_group_dict['20-29'], '30-39': age_group_dict['30-39'], '40-49': age_group_dict['40-49'], '50-59': age_group_dict['50-59'], '60以上': age_group_dict['60以上']}
    result_dict = group_dict
    
    return jsonify(result_dict)
@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html')
@app.route('/wiki', methods=['GET'])
def wiki():
    return render_template('wiki.html')
# 執行 Flask 應用程式
if __name__ == '__main__':
    app.run(debug=True)


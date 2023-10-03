from flask import Flask, request, redirect, jsonify, render_template, url_for, send_from_directory
from mail import My_Mail
from DB import DB
from create_json import My_Json
from flask_login import login_user, logout_user, LoginManager, UserMixin, login_required, current_user
from flask_httpauth import HTTPBasicAuth
import addrestoik as atik
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import pytz
from calc_distance import CalcDistance

class User(UserMixin):
    pass

app = Flask(__name__)
upload_folder = './static/map_display/img/safeguard/'
app.config['SECRET_KEY'] = 'machimori'
app.config['UPLOAD_FOLDER'] = upload_folder

email_parent = "parent@example.com"
email_house = "house@example.com"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"

allowed_extensions = set(['png', 'jpg', 'gif', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_extensions

@login_manager.user_loader
def load_user(sp_ID):
    db = DB()
    sql = 'select parent_ID from parent where parent_ID=%s;'
    data = db.select(sql, (sp_ID,))
    if data == []:
        sql = 'select safeguard_ID from safeguard where safeguard_ID=%s;'
        data = db.select(sql, (sp_ID,))
    db.end_DB()
    if sp_ID not in data[0]:
        return
    user = User()
    user.id = sp_ID
    return user

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        db = DB()
        sp_ID = request.form['ID']
        password = request.form['password']
        sql = 'select parent_password from parent where parent_ID=%s;'
        data = db.select(sql, (sp_ID,))
        if data == []:
            sql = 'select safeguard_password from safeguard where safeguard_ID=%s;'
            data = db.select(sql, (sp_ID,))
        db.end_DB()
        for pas in data:
            if pas[0] == password:
                user = User()
                user.id = sp_ID
                login_user(user)
                return redirect(url_for('map'))
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/select_type')
def select_type():
    return render_template('select_type.html')

@app.route('/registration_parent')
def registration_parent():
    return render_template('registration_parent.html')

@app.route('/registration_parent_data',methods=['POST'])
def registration_parent_data():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        mail_addres = request.form['mail_addres']
        password = request.form['password']
        addres_number = request.form['zip11']
        addres1 = request.form['addr11']
        addres2 = request.form['Address2']
        buzer_number = request.form['buzer_number']

        lat,lon = atik.address_to_latlon(addres1+addres2)
        db = DB()
        sql = 'select * from parent'
        ID_count = len(db.select(sql))
        data = ('P'+str(10000+ID_count),buzer_number,addres1+addres2,lat,lon,first_name+last_name,mail_addres,password)
        sql = 'insert into parent values (%s,%s,%s,%s,%s,%s,%s,%s)'
        db.insert_update(sql,data)
        db.end_DB()

        mail = My_Mail(app)
        mail.p_registration_mail([mail_addres], first_name+last_name, 'P'+str(10000+ID_count))

        return redirect(url_for('home'))
                
@app.route('/registration_safehouse')
def registration_safehouse():
    return render_template('registration_safehouse.html')

@app.route('/registration_safehouse_data',methods=['POST'])
def registration_safehouse_data():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        mail_addres = request.form['mail_address']
        password = request.form['password']
        addres_number = request.form['zip11']
        addres1 = request.form['addr11']
        addres2 = request.form['address']

        img_path = 'NULL'
        if 'uploadfile' in request.files:
            imgfile = request.files['uploadfile']
            # print('success file')
            if imgfile and allowed_file(imgfile.filename):
                filename = secure_filename(imgfile.filename)
                img_path = os.path.join(upload_folder,filename)
                imgfile.save(img_path)
                print(img_path)

        lat,lon = atik.address_to_latlon(addres1+addres2)
        db = DB()
        sql = 'select * from safeguard'
        ID_count = len(db.select(sql))
        data = ('S'+str(10000+ID_count),addres1+addres2,lat,lon,first_name+last_name,mail_addres,password, img_path)
        sql = 'insert into safeguard values (%s,%s,%s,%s,%s,%s,%s,%s)'
        db.insert_update(sql,data)
        db.end_DB()

        mail = My_Mail(app)
        mail.s_registration_mail([mail_addres], first_name+last_name, 'S'+str(10000+ID_count))

        return redirect(url_for('home'))
    
@app.route('/map')
@login_required
def map():
    user_flag = 0
    db = DB()
    sql = 'select * from occur;'
    occurdata = db.select(sql)
    sql = 'select * from safeguard;'
    safeguarddata = db.select(sql)
    sql = 'select buzzer_num,parent_lat,parent_lon,parent_name from parent where parent_ID=%s;'
    inuserdata = db.select(sql, (current_user.id,))
    if inuserdata == []:
        user_flag = 1
        sql = 'select safeguard_ID,safeguard_lat,safeguard_lon,safeguard_name from safeguard where safeguard_ID=%s;'
        inuserdata = db.select(sql, (current_user.id,))
    create_json = My_Json()
    data = create_json.data_molding(0, occurdata, 1, safeguarddata, inuserdata, user_flag)
    db.end_DB()
    return render_template('map_display.html', data=data, name=inuserdata[0][3])

@app.route('/add_occur_data', methods=['POST'])
def add_occur_data():
    if request.method == 'POST':
        casedata = request.form.getlist('case')
        latlon = request.form.getlist('latlon')
        db = DB()
        sql = 'update occur set occur_case=%s where occur_lat=%s and occur_lon=%s;'
        data = (','.join(casedata),latlon[0],latlon[1],)
        db.insert_update(sql,data)
        db.end_DB()
    return redirect(url_for('map'))

@app.route('/abnormal_mail')
def ab_send_mail():
    mail = My_Mail(app)
    mail.pab_send_mail([email_parent])
    return redirect(url_for('home'))

@app.route('/buzzer_mail')
def bz_send_mail():
    mail = My_Mail(app)
    mail.pbz_send_mail([email_parent])
    mail.sbz_send_mail([email_house])
    return redirect(url_for('home'))

@app.route('/wio_form')
def wio_form():
    return render_template('wio_form.html')

@app.route('/wio', methods=['GET','POST'])
def get_wio_data():
    mail = My_Mail(app)
    if request.method == 'POST':
        wio_lat = request.form['lat']
        wio_lon = request.form['lon']
        flag = int(request.form['flag'])
        parent_ID = request.form['parent_ID']
        buzzer_num = request.form['buzzer_num']
        if flag == 0:
            flag_text = '定期通信'
        elif flag == 1:
            flag_text = 'ボタンが押された'
            db = DB()
            sql = 'select parent_name,parent_mail_address from parent where parent_ID=%s'
            pdata = db.select(sql, (parent_ID,))
            mail.pbz_send_mail(pdata)
            sql = 'select safeguard_lat,safeguard_lon,safeguard_name,safeguard_mail_address from safeguard'
            sdata = db.select(sql)
            cd = CalcDistance(sdata)
            s_namail_list = cd.cal_rho(float(wio_lat),float(wio_lon))
            if s_namail_list != []:
                mail.sbz_send_mail(s_namail_list)
            nowtime = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H-%M-%S')
            sql = "insert into occur(occur_ID,parent_ID,buzzer_num,occur_lat,occur_lon,occur_time) value (%s,%s,%s,%s,%s,%s)"
            data = (0,parent_ID, buzzer_num, wio_lat, wio_lon, nowtime,)
            db.insert_update(sql, data)
            db.end_DB()
    else :
        print('GETで来た')
        print(request.args.get('lat'))
        print(request.args.get('lon'))
        mail.wio_get_mail([email_parent, email_house], 'GET', request.args.get('lat'), request.args.get('lon'))
    return str(1)

@app.route('/mistake')
def mistake():
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

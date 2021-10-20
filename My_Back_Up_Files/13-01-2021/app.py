from flask import Flask, render_template, request, session, redirect, url_for, flash, Response, Blueprint, jsonify
from functools import wraps,reduce
import gc
import requests
from werkzeug.utils import secure_filename
from azure_blob.database.dbconnect import connection
from azure_blob.security import login_encrypt, data_encryption
import flask
import flask_login
import datetime
from gevent.pywsgi import WSGIServer
from ldap3 import Server, Connection, ALL
from flask_restful import Resource, Api
from azure_blob.package.cloud_connection import downlaod_s3_unzip_upload
from azure_blob.package.api_config import get_part_data,get_sub_part_data,get_policy_details
from azure_blob.ICR_final import identifying_type_of_doc
from azure_blob.package.cloud_connection import upload_to_aws, image_presigned_url, image_sas_url
import ssl
#from OpenSSL import SSL
global view_permission, edit_table, gey_out_remove_button
from flask_talisman import Talisman
from flask_cookie_decode import CookieDecode
from flask_wtf.csrf import CSRFProtect
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import json
#from talisman import Talisman
from flask_cors import CORS
from azure_blob.ICR_final import identifying_type_of_doc
import pandas as pd
import json
import threading
from collections import defaultdict
import os
csp = {
        'default-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
	'https://il-s3--cldillodgeclaim-du.s3.amazonaws.com',
    ],
        'img-src': ['\'self\'','https://il-s3--cldillodgeclaim-du.s3.amazonaws.com',],
        'media-src': [
            'https://il-s3--cldillodgeclaim-du.s3.amazonaws.com',
        ],
        'style-src': ['\'unsafe-inline\'' ,'\'self\'',],
        'script-src': ['\'unsafe-inline\'' ,'\'self\'','https://cdn.jsdelivr.net',]
    }
blue_print = Blueprint("for_demo", __name__, url_prefix='/ICICI_MICRA', template_folder='templates', static_folder='static')
app = Flask(__name__)
#app.url_map.strict_slashes = False
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#cors = CORS(app)
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
api = Api(app, prefix="/api/processing")
Talisman(app,content_security_policy=csp)
cookie = CookieDecode()
cookie.init_app(app)
csrf = CSRFProtect(app)
SESSION_COOKIE_SECURE = True
app.config.update(
    SESSION_COOKIE_SAMESITE='strict',
SESSION_COOKIE_PATH = '/ICICI_MICRA',
)
#app.config['CORS_METHODS'] = ['GET', 'POST']
def encrypt_plain(plain_text):
    data = b64decode(plain_text)
    with open('static/keyfile/my_enc.json') as f:
        data_json = json.load(f)
    bytes = PBKDF2(str(data_json.get('my_key')).encode("utf-8"), str(data_json.get('my_salt')).encode("utf-8"), 48, 128)
    iv = bytes[0:16]
    key = bytes[16:48]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    text = cipher.decrypt(data)
    text = text[:-text[-1]].decode("utf-8")
    return text

def get_dropdownjsondata():
    LOOKUP_ID = []
    LOOKUP_NAME = []
    excel_file = 'lov_config/Lookup LOV VALUES.xlsx'
    MANUFACTURER = pd.read_excel(excel_file,sheet_name='MANUFACTURER')
    json_str = MANUFACTURER.to_json(orient='records')
    jsondata=json.loads(json_str)
    for i in range(len(jsondata)):
        LOOKUP_ID.append(jsondata[i]['LOOKUP_ID'])
        LOOKUP_NAME.append(jsondata[i]['LOOKUP_NAME'])

    return LOOKUP_ID,LOOKUP_NAME
    
    
def all_DropDowndata():
    excel_file = 'lov_config/All_DropDowndata.xlsx'
    # Insured_type/basic_Insured_Type
    Insured_type_LOOKUP_ID = []
    Insured_type_LOOKUP_NAME = []
    Insured_type = pd.read_excel(excel_file, sheet_name='Insured Type')
    json_str = Insured_type.to_json(orient='records')
    jsondata = json.loads(json_str)
    for i in range(len(jsondata)):
        Insured_type_LOOKUP_ID.append(jsondata[i]['LOOKUP_ID'])
        Insured_type_LOOKUP_NAME.append(jsondata[i]['LOOKUP_NAME'])
    # permit
    permit_LOOKUP_ID = []
    permit_LOOKUP_NAME = []
    permit = pd.read_excel(excel_file, sheet_name='Insured Type')
    json_str = permit.to_json(orient='records')
    jsondata = json.loads(json_str)
    for i in range(len(jsondata)):
        permit_LOOKUP_ID.append(jsondata[i]['LOOKUP_ID'])
        permit_LOOKUP_NAME.append(jsondata[i]['LOOKUP_NAME'])
    #Type of Licence

    Type_of_Licence_LOOKUP_ID = []
    Type_of_Licence_LOOKUP_NAME = []
    Type_of_Licence = pd.read_excel(excel_file, sheet_name='Type of Licence')
    json_str = Type_of_Licence.to_json(orient='records')
    jsondata = json.loads(json_str)
    for i in range(len(jsondata)):
        Type_of_Licence_LOOKUP_ID.append(jsondata[i]['LOOKUP_ID'])
        Type_of_Licence_LOOKUP_NAME.append(jsondata[i]['LOOKUP_NAME'])
    #RTO Locations
    RTO_Locations_LOOKUP_ID = []
    RTO_Locations_LOOKUP_NAME = []
    RTO_Locations = pd.read_excel(excel_file, sheet_name='RTO Locations')
    json_str = RTO_Locations.to_json(orient='records')
    jsondata = json.loads(json_str)
    for i in range(len(jsondata)):
        RTO_Locations_LOOKUP_ID.append(jsondata[i]['LOOKUP_ID'])
        RTO_Locations_LOOKUP_NAME.append(jsondata[i]['LOOKUP_NAME'])
    #Road Type

    Road_Type_LOOKUP_ID = []
    Road_Type_LOOKUP_NAME = []
    Road_Type = pd.read_excel(excel_file, sheet_name='Road Type')
    json_str = Road_Type.to_json(orient='records')
    jsondata = json.loads(json_str)
    for i in range(len(jsondata)):
        Road_Type_LOOKUP_ID.append(jsondata[i]['LOOKUP_ID'])
        Road_Type_LOOKUP_NAME.append(jsondata[i]['LOOKUP_NAME'])

    #Nature of Goods

    NatureofGoods_LOOKUP_ID = []
    NatureofGoods_LOOKUP_NAME = []
    NatureofGoods = pd.read_excel(excel_file, sheet_name='Nature of Goods')
    json_str = NatureofGoods.to_json(orient='records')
    jsondata = json.loads(json_str)
    for i in range(len(jsondata)):
        NatureofGoods_LOOKUP_ID.append(jsondata[i]['LOOKUP_ID'])
        NatureofGoods_LOOKUP_NAME.append(jsondata[i]['LOOKUP_NAME'])
    #Driver Qualification
    Driver_Qualification_LOOKUP_ID = []
    Driver_Qualification_LOOKUP_NAME = []
    Driver_Qualification = pd.read_excel(excel_file, sheet_name='Driver Qualification')
    json_str = Driver_Qualification.to_json(orient='records')
    jsondata = json.loads(json_str)
    for i in range(len(jsondata)):
        Driver_Qualification_LOOKUP_ID.append(jsondata[i]['LOOKUP_ID'])
        Driver_Qualification_LOOKUP_NAME.append(jsondata[i]['LOOKUP_NAME'])

    #Vehicle driven by
    Vehicledrivenby_LOOKUP_ID = []
    Vehicledrivenby_LOOKUP_NAME = []
    Vehicledrivenby = pd.read_excel(excel_file, sheet_name='Vehicle driven by')
    json_str = Vehicledrivenby.to_json(orient='records')
    jsondata = json.loads(json_str)
    for i in range(len(jsondata)):
        Vehicledrivenby_LOOKUP_ID.append(jsondata[i]['LOOKUP_ID'])
        Vehicledrivenby_LOOKUP_NAME.append(jsondata[i]['LOOKUP_NAME'])

    #Cause of loss

    Causeofloss_LOOKUP_ID = []
    Causeofloss_LOOKUP_NAME = []
    Causeofloss = pd.read_excel(excel_file, sheet_name='Cause of loss')
    json_str = Causeofloss.to_json(orient='records')
    jsondata = json.loads(json_str)
    for i in range(len(jsondata)):
        Causeofloss_LOOKUP_ID.append(jsondata[i]['LOOKUP_ID'])
        Causeofloss_LOOKUP_NAME.append(jsondata[i]['LOOKUP_NAME'])

    return Insured_type_LOOKUP_ID, Insured_type_LOOKUP_NAME,permit_LOOKUP_ID,permit_LOOKUP_NAME,Type_of_Licence_LOOKUP_ID,Type_of_Licence_LOOKUP_NAME,RTO_Locations_LOOKUP_ID,RTO_Locations_LOOKUP_NAME,Road_Type_LOOKUP_ID,Road_Type_LOOKUP_NAME,NatureofGoods_LOOKUP_ID,NatureofGoods_LOOKUP_NAME,Driver_Qualification_LOOKUP_ID,Driver_Qualification_LOOKUP_NAME,Vehicledrivenby_LOOKUP_ID,Vehicledrivenby_LOOKUP_NAME,Causeofloss_LOOKUP_ID,Causeofloss_LOOKUP_NAME


def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items()
                            if len(locs)>1)

def sorting_summary_invoice(part_name,sub_part_name,type_of_charges,taxable_value):
	duplicate_value_part = []
	print("main",sub_part_name)
	duplicate_index_part = []
	inv_lab_subpart_dropdown_buffer = []
	for dup in sorted(list_duplicates(part_name)):
		# print(dup[0],dup[1])
		duplicate_value_part.append(dup[0])
		duplicate_index_part.append(dup[1])

	my_buffer = []
	for i in range(len(duplicate_value_part)):
		for j in range(len(duplicate_index_part[i])):
			my_buffer.append(sub_part_name[duplicate_index_part[i][j]])
		inv_lab_subpart_dropdown_buffer.append(my_buffer)
		my_buffer = []
	# print(duplicate_index_part)
	sub_part_index = []
	# print(inv_lab_subpart_dropdown_buffer)
	for i in range(len(inv_lab_subpart_dropdown_buffer)):
		for dup in sorted(list_duplicates(inv_lab_subpart_dropdown_buffer[i])):
			sub_part_index.append(dup[1])
	print("sub partr",sub_part_index)

	final_duplicate_index_buffer = []

	my_buffer = []
	for i in range(len(sub_part_index)):
		for j in range(len(sub_part_index[i])):
			my_buffer.append(duplicate_index_part[i][sub_part_index[i][j]])
		final_duplicate_index_buffer.append(my_buffer)
		my_buffer = []
	final_list = []
	final_list_buffer = ['','','Metal','1',0.00,'18%',0.00,0.00,0.00,'18%','Repair',0.00,0.00,0.00]
	for i in range(len(final_duplicate_index_buffer)):
		for j in range(len(final_duplicate_index_buffer[i])):
			# print(final_duplicate_index_buffer[i][j])
			final_list_buffer[0] = part_name[final_duplicate_index_buffer[i][j]]
			final_list_buffer[1] = sub_part_name[final_duplicate_index_buffer[i][j]]
			if type_of_charges[final_duplicate_index_buffer[i][j]] == "painting_charges":
				final_list_buffer[8] = final_list_buffer[8] + float(taxable_value[final_duplicate_index_buffer[i][j]].replace(",","").replace(" ",""))
			if type_of_charges[final_duplicate_index_buffer[i][j]] == "part_charges":
				final_list_buffer[4] = final_list_buffer[4] + float(taxable_value[final_duplicate_index_buffer[i][j]].replace(",","").replace(" ",""))
			if type_of_charges[final_duplicate_index_buffer[i][j]] == "denting_charges":
				final_list_buffer[7] = final_list_buffer[7] + float(taxable_value[final_duplicate_index_buffer[i][j]].replace(",","").replace(" ",""))
			if type_of_charges[final_duplicate_index_buffer[i][j]] == "of_charges":
				final_list_buffer[6] = final_list_buffer[6] + float(taxable_value[final_duplicate_index_buffer[i][j]].replace(",","").replace(" ",""))
		final_list.append(final_list_buffer)
		final_list_buffer = ['','','','',0.00,'',0.00,0.00,0.00,'','',0.00,0.00,0.00]

	final_duplicate_index = []
	print(final_duplicate_index_buffer)
	final_duplicate_index = reduce(lambda x,y :(x[0]+y[0],x[1]+y[1]) ,final_duplicate_index_buffer)
	final_list_buffer = ['','','Metal','1',0.00,'18%',0.00,0.00,0.00,'18%','Repair',0.00,0.00,0.00]
	count = 0
	for i in range(len(part_name)):
		# print(final_duplicate_index[count])
		if i == final_duplicate_index[count]:
			if count < len(final_duplicate_index) - 1:
				count = count + 1
		else:

			final_list_buffer[0] = part_name[i]
			final_list_buffer[1] = sub_part_name[i]
			if type_of_charges[i] == "painting_charges":
				final_list_buffer[8] = final_list_buffer[8] + float(taxable_value[i].replace(",","").replace(" ",""))
			if type_of_charges[i] == "part_charges":
				final_list_buffer[4] = final_list_buffer[4] + float(taxable_value[i].replace(",","").replace(" ",""))
			if type_of_charges[i] == "denting_charges":
				final_list_buffer[7] = final_list_buffer[7] + float(taxable_value[i].replace(",","").replace(" ",""))
			if type_of_charges[i] == "of_charges":
				final_list_buffer[6] = final_list_buffer[6] + float(taxable_value[i].replace(",","").replace(" ",""))
			final_list.append(final_list_buffer)
			final_list_buffer = ['','','Metal','1',0.00,'18%',0.00,0.00,0.00,'18%','Repair',0.00,0.00,0.00]


	return final_list



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        #print(session)
        #print("login check")
        if 'logged_in' in session:

            return f(*args, **kwargs)
        else:
            #flash("You need to login first")
            return redirect(url_for('for_demo.login'))

    return wrap

@blue_print.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    r.headers["server"] = ""
    return r

@blue_print.before_request
def before_request():

    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=10)
    flask.session.modified = True
    flask.g.user = flask_login.current_user
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@blue_print.route('/',methods=["GET", "POST"])
def login():
    if request.method == "OPTIONS":
        return 403
    else:
        session.clear()
        gc.collect()
        #print("login")
        password_msg = "hidden"
        already_logged_msg = "hidden"
        return render_template("login.html", password_msg=password_msg, already_logged_msg=already_logged_msg)


@blue_print.route('/ICICI', methods=["GET", "POST"])
@csrf.exempt
# @login_required
def home():
    # if request.method == "POST":
    #print("starting application ....")
    #print(session)

    where_email_id = ""
    where_row_id = ""
    session_flag_login = 0
    login_session_id = 0
    password_msg = "hidden"
    already_logged_msg = "hidden"
    ui_last_login = ""
    if request.method == "POST":
        #username_form = request.form["username"]
        username_form = encrypt_plain(str(request.form["username"]))
        #password_form = request.form["pass"]
        password_form = encrypt_plain(str(request.form["pass"]))
        session['username_form'] = username_form
        session['password_form'] = password_form
        #print("username",session)
        try:
            s = Server('cldilACTds04.ilgicltd.com', get_info=ALL)
            c = Connection(s, user=username_form, password=password_form)
            #print(c.bind())
            if str(c.bind()) == "True":
                #print("in true")
                session['logged_in'] = True
                # session['set_expiry'] = 240
                c, conn, status = connection()
                c.execute("SELECT user_name,login_verified,user_id,last_login FROM icici_user_management;")
                row = c.fetchall()
                c.close()
                conn.close()
                #print("my data row",row)
                for my_count_for in range(len(row)):
                    today_1 = datetime.datetime.today()
                    dt_string_new = str(today_1.strftime("%d/%m/%Y %H:%M:%S"))
                    datetime_object_1 = datetime.datetime.strptime(dt_string_new, '%d/%m/%Y %H:%M:%S')
                    datetime_object_2 = datetime.datetime.strptime(str(row[my_count_for][3]), '%d/%m/%Y %H:%M:%S')
                    if str(login_encrypt(str(row[my_count_for][0]))) == session.get('username_form') and (str(
                            row[my_count_for][1]) == "no_login" or (datetime_object_1 - datetime_object_2).total_seconds()/60 > 10):
                        login_session_id = row[my_count_for][2]
                        session['login_session_id'] = login_session_id
                        session_flag_login = 1
                        break
                # login_status = 1
                # session['login_status'] = 1
                if session_flag_login == 1:
                    login_status = 1
                    today_1 = datetime.datetime.today()
                    dt_string = str(today_1.strftime("%d/%m/%Y %H:%M:%S"))
                    c, conn, status = connection()
                    c.execute("SELECT last_login FROM icici_user_management WHERE user_id = %s"%(str(session.get('login_session_id'))))
                    ui_last_login = c.fetchall()[0][0]
                    session['ui_last_login'] = ui_last_login
                    c.execute("UPDATE icici_user_management SET login_verified = %s,last_login = %s WHERE user_id = %s",
                              ("yes_login", dt_string, session.get('login_session_id')))
                    conn.commit()
                    c.close()
                    conn.close()
                    session['login_status'] = 1
                else:
                    password_msg = "hidden"
                    already_logged_msg = ""
                    return render_template("login.html", password_msg=password_msg,
                                           already_logged_msg=already_logged_msg)
            else:
                login_status = 0
                session['login_status'] = 0
        except ValueError as err:
            return "login connection failed"

    view_permission = ""
    edit_table = ""
    gey_out_remove_button = ""
    gey_out_remove_button_index_page = ""
    last_logged_in_at = ""
    if session.get('login_status') == 1:
        #print("in login")

        c, conn, status = connection()
        c.execute("SELECT icici_login_username,attribute_1,attribute_2 FROM icici_login_details;")
        row = c.fetchall()
        c.close()
        conn.close()

        for i in range(len(row)):
            #print(login_encrypt(str(row[i][1])))
            if str(login_encrypt(str(row[i][1]))) == session.get('username_form'):
                where_email_id = str(login_encrypt(str(row[i][0])))
                where_row_id = str(login_encrypt(str(row[i][2])))
                #print(where_email_id)
                #print(where_row_id)
        claim_number = []
        process_status = []
        process_time = []
        process_doc = []
        claims_with_partial_document = 0
        claim_recieved_my_days_count = 0
        claim_processed_by_agent = 0
        claim_processed_by_agent_today = 0
        total_claim_rejected = 0
        total_no_claims = 0
        #print("before db")
        c, conn, status = connection()
        #print(status)
        # c.execute("SELECT icici_claim_number,icici_dl_frt,icici_rc_frt,icici_aadhar_frt,icici_pan,icici_policy_form,icici_intimation_sheet,icici_estimation_sheet,icici_invoice,icici_claim_form_pg1,icici_status,icici_time FROM icici_email_recieved_document WHERE icici_email_id = '%s';")
        # row = c.fetchall()
        if where_row_id == "csm":
            gey_out_remove_button_index_page = "disabled"
            c.execute(
                "SELECT icici_claim_number,icici_dl_frt,icici_rc_frt,icici_aadhar_frt,icici_pan,icici_policy_form,icici_intimation_sheet,icici_estimation_sheet,icici_invoice,icici_claim_form_pg1,icici_status,icici_time,icici_email_id FROM icici_email_recieved_document ;")
            row_temp = c.fetchall()
            row = []
            for i in range(len(row_temp)):
                #print(row_temp[i][12],str(session.get('username_form').split('\\')[1]))
                if str(row_temp[i][12]) == where_email_id or str(row_temp[i][12]).upper().__contains__(str(session.get('username_form').split('\\')[1]).upper()):
                    row.append(row_temp[i])


            session['view_permission'] = ""
            session['edit_table'] = ""
            session['gey_out_remove_button'] = ""
            session['gey_out_remove_button_index_page'] = ""
        elif where_row_id == "read":
            c.execute(
                "SELECT icici_claim_number,icici_dl_frt,icici_rc_frt,icici_aadhar_frt,icici_pan,icici_policy_form,icici_intimation_sheet,icici_estimation_sheet,icici_invoice,icici_claim_form_pg1,icici_status,icici_time,icici_email_id FROM icici_email_recieved_document ;")

            row = c.fetchall()
            session['view_permission'] = "readonly"
            session['edit_table'] = "false"
            session['gey_out_remove_button'] = "disabled"
            session['gey_out_remove_button_index_page'] = ""

        elif where_row_id == "admin":
            gey_out_remove_button_index_page = ""
            c.execute(
                "SELECT icici_claim_number,icici_dl_frt,icici_rc_frt,icici_aadhar_frt,icici_pan,icici_policy_form,icici_intimation_sheet,icici_estimation_sheet,icici_invoice,icici_claim_form_pg1,icici_status,icici_time,icici_email_id FROM icici_email_recieved_document ;")

            row = c.fetchall()
            session['view_permission'] = ""
            session['edit_table'] = ""
            session['gey_out_remove_button'] = ""
            session['gey_out_remove_button_index_page'] = ""
        else:
            c.close()
            conn.close()
            return ("User Not Allowed")

        c.close()
        conn.close()
        #print("view", view_permission)
        today_date = datetime.datetime.strptime(datetime.date.today().strftime("%Y-%m-%d"), '%Y-%m-%d').date()
        total_no_claims = len(row)
        for i_count in range(len(row)):
            date_time_obj = datetime.datetime.strptime(row[i_count][11], '%Y-%m-%d %H:%M:%S')
            if (today_date - date_time_obj.date()).days == 0:
                claim_recieved_my_days_count = claim_recieved_my_days_count + 1

        for i_count in range(len(row)):
            date_time_obj = datetime.datetime.strptime(row[i_count][11], '%Y-%m-%d %H:%M:%S')
            if (today_date - date_time_obj.date()).days == 0 and str(row[i_count][10]) == 'Complete':
                claim_processed_by_agent_today = claim_processed_by_agent_today + 1
            if str(row[i_count][10]) == 'Complete':
                claim_processed_by_agent = claim_processed_by_agent + 1
            if str(row[i_count][10]) == 'Rejected':
                total_claim_rejected = total_claim_rejected + 1

        for i_count in range(len(row)):
            if str(row[i_count][8]) != 'Yes':
                claims_with_partial_document = claims_with_partial_document + 1
        for i in range(len(row)):
            inner_list = ["", "", "", "", "", "", "", "", ""]
            claim_number.append(row[i][0])
            process_status.append(row[i][10])
            process_time.append(row[i][11])
            if row[i][1] != "Yes":
                inner_list[0] = str("<i class='fa fa-times' style='color:#f00505;font-size:24px;'></i>")
            else:
                inner_list[0] = str("<i class='fa fa-check' style='color:#00c700;font-size:24px;'></i>")
            if row[i][2] != "Yes":
                inner_list[1] = str("<i class='fa fa-times ' style='color:#f00505;font-size:24px;'></i>")
            else:
                inner_list[1] = str("<i class='fa fa-check' style='color:#00c700;font-size:24px;'></i>")
            if row[i][5] != "Yes":
                inner_list[2] = str("<i class='fa fa-times ' style='color:#f00505;font-size:24px;'></i>")
            else:
                inner_list[2] = str("<i class='fa fa-check' style='color:#00c700;font-size:24px;'></i>")
            if row[i][9] != "Yes":
                inner_list[3] = str("<i class='fa fa-times ' style='color:#f00505;font-size:24px;'></i>")
            else:
                inner_list[3] = str("<i class='fa fa-check' style='color:#00c700;font-size:24px;'></i>")
            if row[i][6] != "Yes":
                inner_list[4] = str("<i class='fa fa-times ' style='color:#f00505;font-size:24px;'></i>")
            else:
                inner_list[4] = str("<i class='fa fa-check' style='color:#00c700;font-size:24px;'></i>")
            if row[i][4] != "Yes":
                inner_list[5] = str("<i class='fa fa-times ' style='color:#f00505;font-size:24px;'></i>")
            else:
                inner_list[5] = str("<i class='fa fa-check' style='color:#00c700;font-size:24px;'></i>")
            if row[i][8] != "Yes":
                inner_list[6] = str("<i class='fa fa-times ' style='color:#f00505;font-size:24px;'></i>")
            else:
                inner_list[6] = str("<i class='fa fa-check' style='color:#00c700;font-size:24px;'></i>")
            if row[i][3] != "Yes":
                inner_list[7] = str("<i class='fa fa-times ' style='color:#f00505;font-size:24px;'></i>")
            else:
                inner_list[7] = str("<i class='fa fa-check' style='color:#00c700;font-size:24px;'></i>")
            if row[i][7] != "Yes":
                inner_list[8] = str("<i class='fa fa-times ' style='color:#f00505;font-size:24px;'></i>")
            else:
                inner_list[8] = str("<i class='fa fa-check' style='color:#00c700;font-size:24px;'></i>")
            process_doc.append(inner_list)
        claim_count = len(claim_number)
        username_form = session.get('username_form')

        return render_template("index.html",total_no_claims = total_no_claims,claim_recieved_my_days_count = claim_recieved_my_days_count,claim_processed_by_agent = claim_processed_by_agent,claim_processed_by_agent_today = claim_processed_by_agent_today,total_claim_rejected = total_claim_rejected,claims_with_partial_document = claims_with_partial_document,login_session_id = login_session_id,ui_last_login = session.get('ui_last_login'), username=username_form, process_doc=process_doc, claim_number=claim_number,
                               claim_count=claim_count, process_status=process_status, process_time=process_time)
    else:
        # return "Invalid cred"
        password_msg = ""
        already_logged_msg = "hidden"
        return render_template('login.html', password_msg=password_msg, already_logged_msg=already_logged_msg)

@blue_print.route('/model/<string:PARENTID>',methods=["GET", "POST"])
@login_required
@csrf.exempt
def model(PARENTID):
    excel_file = 'lov_config/Lookup LOV VALUES.xlsx'
    modesl=pd.read_excel(excel_file,sheet_name='MODEL',)
    json_str=modesl.to_json(orient='records')
    json_data = json.loads(json_str)
    MODEL=[]
    for i in range(len(json_data)):
        if str(PARENTID) in str(json_data[i]['PARENT_ID']):
            modelobj={}
            modelobj['LOOKUP_ID']=str(json_data[i]['LOOKUP_ID'])
            modelobj['LOOKUP_NAME']=str(json_data[i]['LOOKUP_NAME'])
            MODEL.append(modelobj)
    print(MODEL)
    return jsonify({'MODEL':MODEL})

@blue_print.route('/ICICI/CLAIM/<string:myid>', methods=["GET", "POST"])
@login_required
def claim(myid):
    invoice_url_pdf = ""
    #print("in claim",session.get('view_permission'))
    view_permission = session.get('view_permission')
    edit_table = session.get('edit_table')
    gey_out_remove_button = session.get('gey_out_remove_button')
    gey_out_remove_button_index_page = session.get('gey_out_remove_button_index_page')
    #print("view", view_permission)
    # time.sleep(5)
    dl_icon_img = ""
    dl_bck_icon_img = ""
    rc_icon_img = ""
    cf_icon_img = ""
    cf_icon_img_2 = ""
    cf_icon_img_3 = ""
    cf_icon_img_4 = ""
    is_icon_img = ""
    pf_icon_img = ""
    rc_bck_icon_img = ""
    pan_icon_img = ""
    aadhar_icon_img = ""
    dl_stat = ""
    rc_stat = ""
    cf_stat = ""
    cf_stat_2 = ""
    cf_stat_3 = ""
    cf_stat_4 = ""
    is_stat = ""
    pf_stat = ""
    in_stat = ""
    es_stat = ""
    pan_stat = ""
    aadhar_stat = ""
    aadhar_stat_bck = ""
    dl_url = ""
    dl_bck_url = ""
    rc_url = ""
    rc_bck_url = ""
    rc_bck_stat = ""
    rc_stat_row_bck = ""
    pan_url = ""
    aadhar_url = ""
    aadhar_url_bck = ""
    dl_stat_row = ""
    dl_stat_row_bck = ""
    dl_bck_stat = ""
    rc_stat_row = ""
    cf_stat_row = ""
    cf_stat_row_2 = ""
    cf_stat_row_3 = ""
    cf_stat_row_4 = ""
    is_stat_row = ""
    pf_stat_row = ""
    pan_stat_row = ""
    aadhar_stat_row = ""
    aadhar_stat_row_bck = ""
    es_data_count = 0
    claim_form_url = ""
    claim_form_url_2 = ""
    claim_form_url_3 = ""
    claim_form_url_4 = ""
    intimation_sheet_page1_url = ""
    policy_form_1_url = ""
    invoice_post_check = ""

    username = session.get('username_form')
    #print("Second Page")
    # #print(myid)
    claim_number = myid
    check_claim_number_flag = 0
    row_number_claim_number = 0
    row = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    doc_sas_url = []
    doc_sas_url = image_sas_url(myid)
    for image_sas_index in range(len(doc_sas_url)):
        img_url_with_sas_token = doc_sas_url[image_sas_index]
        if (str(img_url_with_sas_token).upper().__contains__("PAN.PNG") or str(
                img_url_with_sas_token).upper().__contains__("PAN.JPG")):
            row[4] = img_url_with_sas_token
        elif (str(img_url_with_sas_token).upper().__contains__("DL.JPG") or str(
                img_url_with_sas_token).upper().__contains__("DL.PNG")):
            row[0] = img_url_with_sas_token
        elif (str(img_url_with_sas_token).upper().__contains__("DL_BCK.JPG") or str(
                img_url_with_sas_token).upper().__contains__("DL_BCK.PNG")):
            row[1] = img_url_with_sas_token
        elif (str(img_url_with_sas_token).upper().__contains__("RC_BCK.PNG") or str(
                img_url_with_sas_token).upper().__contains__("RC_BCK.JPG")):
            row[3] = img_url_with_sas_token
        elif (str(img_url_with_sas_token).upper().__contains__("RC.PNG") or str(
                img_url_with_sas_token).upper().__contains__("RC.JPG")):
            row[2] = img_url_with_sas_token
        elif (str(img_url_with_sas_token).upper().__contains__("AADHAR.PNG") or str(
                img_url_with_sas_token).upper().__contains__("AADHAR.JPG")):
            row[5] = img_url_with_sas_token
        elif (str(img_url_with_sas_token).upper().__contains__("AADHAR_BCK.PNG") or str(
                img_url_with_sas_token).upper().__contains__("AADHAR_BCK.JPG")):
            row[6] = img_url_with_sas_token
        elif str(img_url_with_sas_token).upper().__contains__("CLAIM_PG1"):
            row[9] = img_url_with_sas_token
        elif str(img_url_with_sas_token).upper().__contains__("CLAIM_PG2"):
            row[10] = img_url_with_sas_token
        elif str(img_url_with_sas_token).upper().__contains__("CLAIM_PG3"):
            row[11] = img_url_with_sas_token
        elif str(img_url_with_sas_token).upper().__contains__("CLAIM_PG4"):
            row[12] = img_url_with_sas_token
        elif str(img_url_with_sas_token).upper().__contains__("POLICY") and (
                str(img_url_with_sas_token).upper().__contains__("JPG") or str(
                img_url_with_sas_token).upper().__contains__("PNG")):
            row[8] = img_url_with_sas_token
        elif str(img_url_with_sas_token).upper().__contains__("/INTIMATION_IMAGES/"):
            row[7] = img_url_with_sas_token
        elif str(img_url_with_sas_token).upper().__contains__("ESTIMATION") and str(
                img_url_with_sas_token).upper().__contains__(".PDF"):
            row[14] = img_url_with_sas_token
        elif str(img_url_with_sas_token).upper().__contains__("INVOICE") and str(
                img_url_with_sas_token).upper().__contains__(".PDF"):
            row[13] = img_url_with_sas_token

    # c, conn, status = connection()
    # c.execute("SELECT icici_url_dl_frt,icici_url_dl_bck,icici_url_rc_frt,icici_url_rc_bck,icici_url_pan,icici_url_aadhar_frt,icici_url_aadhar_bck,icici_url_intimation,icici_url_policy_form,icici_url_claim_form_pg1,icici_url_claim_form_pg2,icici_url_claim_form_pg3,icici_url_claim_form_pg4,icici_url_invoice,icici_url_estimation FROM icici_document_url WHERE icici_claim_number = '%s';"%(myid))
    # row = c.fetchone()
    # c.close()
    # conn.close()
    # my_text_url = image_sas_url(claim_number)
    if str(row[0]).__contains__("http"):
        #print("IN dl if")
        dl_url = row[0]
        dl_icon_img = "/static/ImgSource/icons/Driving-license-512x512.png"
    else:
        #print("in dl else")
        dl_url = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        dl_stat = "disabled"
        dl_stat_row = "hidden"
        dl_icon_img = "/static/ImgSource/icons/Driving-license-512x512-Cross.png"
    #print("dl stat ", dl_stat)

    # if icr_complete_sheet.cell(row=row_number_claim_number, column=3).value != "":
    if str(row[2]).__contains__("http"):
        rc_url = row[2]
        rc_icon_img = "/static/ImgSource/icons/Registration-Certificate-512x512.png"
    else:
        rc_url = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        rc_stat = "disabled"
        rc_stat_row = "hidden"
        rc_icon_img = "/static/ImgSource/icons/Registration-Certificate-512x512-Cross.png"

    # if icr_complete_sheet.cell(row=row_number_claim_number, column=5).value != "":
    if str(row[9]).__contains__("http"):
        claim_form_url = row[9]
        cf_icon_img = "/static/ImgSource/icons/Claim-Form-512x512.png"
    else:
        claim_form_url = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        cf_stat = "disabled"
        cf_stat_row = "hidden"
        cf_icon_img = "/static/ImgSource/icons/Claim-Form-512x512-Cross.png"

    # if icr_complete_sheet.cell(row=row_number_claim_number, column=6).value != "":
    if str(row[7]).__contains__("http"):
        intimation_sheet_page1_url = row[7]
        is_icon_img = "/static/ImgSource/icons/Intimation Sheet-512x512.png"
    else:
        intimation_sheet_page1_url = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        is_stat = "disabled"
        is_stat_row = "hidden"
        is_icon_img = "/static/ImgSource/icons/Intimation Sheet-512x512-Cross.png"
    # if icr_complete_sheet.cell(row=row_number_claim_number, column=4).value != "":
    if str(row[8]).__contains__("http"):
        policy_form_1_url = row[8]
        pf_icon_img = "/static/ImgSource/icons/Policy-Form-512x512.png"
    else:
        policy_form_1_url = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        pf_stat = "disabled"
        pf_stat_row = "hidden"
        pf_icon_img = "/static/ImgSource/icons/Policy-Form-512x512-Cross.png"

    # if icr_complete_sheet.cell(row=row_number_claim_number, column=7).value != "":
    if str(row[4]).__contains__("http"):
        pan_url = row[4]
        pan_icon_img = "/static/ImgSource/icons/Policy-Form-512x512.png"
    else:
        pan_url = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        pan_stat = "disabled"
        pan_stat_row = "hidden"
        pan_icon_img = "/static/ImgSource/icons/Policy-Form-512x512-Cross.png"

    # if icr_complete_sheet.cell(row=row_number_claim_number, column=9).value != "":
    if str(row[5]).__contains__("http"):
        aadhar_url = row[5]
        aadhar_icon_img = "/static/ImgSource/icons/Policy-Form-512x512.png"
    else:
        aadhar_url = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        aadhar_stat = "disabled"
        aadhar_stat_row = "hidden"
        aadhar_icon_img = "/static/ImgSource/icons/Policy-Form-512x512-Cross.png"
    if str(row[3]).__contains__("http"):
        rc_bck_url = row[3]
        dl_bck_icon_img = "/static/ImgSource/icons/Policy-Form-512x512.png"
        rc_stat_row_bck = ""
    else:
        rc_bck_url = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        rc_bck_stat = "disabled"
        rc_stat_row_bck = "hidden"
        rc_bck_icon_img = "/static/ImgSource/icons/Policy-Form-512x512-Cross.png"

    # if icr_complete_sheet.cell(row=row_number_claim_number, column=14).value != "":
    if str(row[1]).__contains__("http"):
        dl_bck_url = row[1]
        dl_bck_icon_img = "/static/ImgSource/icons/Policy-Form-512x512.png"
        dl_stat_row_bck = ""
    else:
        dl_bck_url = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        dl_bck_stat = "disabled"
        dl_stat_row_bck = "hidden"
        dl_bck_icon_img = "/static/ImgSource/icons/Policy-Form-512x512-Cross.png"
    if str(row[10]).__contains__("http"):
        claim_form_url_2 = row[10]
        cf_icon_img_2 = "/static/ImgSource/icons/Policy-Form-512x512.png"
        cf_stat_row_2 = ""
    else:
        claim_form_url_2 = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        cf_stat_2 = "disabled"
        cf_stat_row_2 = "hidden"
        cf_icon_img_2 = "/static/ImgSource/icons/Policy-Form-512x512-Cross.png"

    if str(row[11]).__contains__("http"):
        claim_form_url_3 = row[11]
        cf_icon_img_3 = "/static/ImgSource/icons/Policy-Form-512x512.png"
        cf_stat_row_3 = ""
    else:
        claim_form_url_3 = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        cf_stat_3 = "disabled"
        cf_stat_row_3 = "hidden"
        cf_icon_img_3 = "/static/ImgSource/icons/Policy-Form-512x512-Cross.png"

    if str(row[12]).__contains__("http"):
        claim_form_url_4 = row[12]
        cf_icon_img_4 = "/static/ImgSource/icons/Policy-Form-512x512.png"
        cf_stat_row_4 = ""
    else:
        claim_form_url_4 = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        cf_stat_4 = "disabled"
        cf_stat_row_4 = "hidden"
        cf_icon_img_4 = "/static/ImgSource/icons/Policy-Form-512x512-Cross.png"

    if str(row[6]).__contains__("http"):
        aadhar_url_bck = row[6]

        aadhar_icon_img = "/static/ImgSource/icons/Policy-Form-512x512.png"
        aadhar_stat_row_bck = ""
    else:
        aadhar_url_bck = "https://firebasestorage.googleapis.com/v0/b/iail-icr.appspot.com/o/iail_icici%2Fno_document_found.png?alt=media&token=21c5f795-3bd4-4882-b5e6-a9a55d4baa3d"
        aadhar_stat_bck = "disabled"
        aadhar_stat_row_bck = "hidden"
        aadhar_icon_img = "/static/ImgSource/icons/Policy-Form-512x512-Cross.png"
    if str(row[13]).__contains__("http"):
        in_stat = ""
        invoice_post_check = "Yes"
        invoice_url_pdf = row[13]
    else:
        in_stat = "hidden"
    if str(row[14]).__contains__("http") and str(row[14]).__contains__(".pdf"):
        es_stat = ""
    else:
        es_stat = "hidden"

    c, conn, status = connection()
    c.execute(
        "SELECT icici_ib_invoice_number,icici_ib_garage_name,icici_ib_model,icici_ib_gst_number,icici_ib_reg_number,icici_ib_policy_number,icici_ib_policy_name,icici_ib_chasiss_number,icici_ib_engine_number,attribute_1	FROM icici_invoice_basic_data WHERE icici_claim_number = '%s';" %
        (claim_number))
    row = c.fetchone()
    c.close()
    conn.close()
    invoice_basic_invoice_number = ""
    invoice_basic_garage_name = ""
    invoice_basic_model = ""
    invoice_basic_gstn_number = ""
    invoice_reg_no_post_process = ""
    invoice_policy_number_post_process = ""
    invoice_name_post_process = ""
    invoice_chassis_number_post_process = ""
    invoice_engine_number_post_process = ""
    invoice_version = ""
    # wb_in_basic = load_workbook("azure_blob/database/local_database.xlsx")
    # wb_in_basic_sheet = wb_in_basic['invoice_data_basic']
    # wb_in_basic_max_row = wb_in_basic_sheet.max_row
    # for i in range(1, wb_in_basic_max_row + 1):
    #     cell_obj = wb_in_basic_sheet.cell(row=i, column=1)
    #     if cell_obj.value == claim_number:
    if row is not None:
        invoice_basic_invoice_number = row[0]
        invoice_basic_garage_name = row[1]
        invoice_basic_model = row[2]
        invoice_basic_gstn_number = row[3]
        invoice_reg_no_post_process = row[4]
        invoice_policy_number_post_process = row[5]
        invoice_name_post_process = row[6]
        invoice_chassis_number_post_process = row[7]
        invoice_engine_number_post_process = row[8]
        invoice_version = row[9]
    #         break
    #     else:
    #         continue
    # wb_in_basic.save("azure_blob/database/local_database.xlsx")
    # wb_in_basic.close()

    my_status_check = 0

    ui_part_name = []
    lab_part_name = []
    part_part_name = []
    lab_part_number = []
    part_part_number = []
    ui_hsn = []
    lab_hsn = []
    part_hsn = []
    lab_qty = []
    ui_qty = []
    part_qty = []
    lab_unit_price = []
    ui_unit_price = []
    part_unit_price = []
    lab_discount_amount = []
    ui_discount_amount = []
    part_discount_amount = []
    lab_taxable_value = []
    ui_taxable_value = []
    part_taxable_value = []
    lab_cgst_per = []
    ui_cgst_per = []
    part_cgst_per = []
    es_part_name = []
    part_es_part_name = []
    lab_es_part_name = []
    part_es_hsn = []
    lab_es_hsn = []
    es_hsn = []
    es_unit_price = []
    part_es_unit_price = []
    lab_es_unit_price = []
    c, conn, status = connection()
    c.execute(
        "SELECT icici_ipd_part_number,icici_ipd_part_name,icici_ipd_hsn,icici_ipd_qty,icici_ipd_unity_price,icici_ipd_discount_amount,icici_ipd_tax_value,icici_ipd_cgst,icici_ipd_sgst,icici_ipd_type_charges	FROM icici_part_details WHERE icici_claim_number_ref = '%s' and attribute_1 = '%s';" % (
        "ref_" + str(claim_number), invoice_version))
    row = c.fetchall()
    c.close()
    conn.close()
    for i in range(len(row)):
        if row[i][9] == "Labour":
            lab_part_number.append(row[i][0])
            lab_part_name.append(row[i][1])
            lab_hsn.append(row[i][2])
            lab_qty.append(row[i][3])
            lab_unit_price.append(row[i][4])
            lab_discount_amount.append(row[i][5])
            lab_taxable_value.append(row[i][6])
            lab_cgst_per.append(row[i][7])
        elif row[i][9] == "Part":
            part_part_number.append(row[i][0])
            part_part_name.append(row[i][1])
            part_hsn.append(row[i][2])
            part_qty.append(row[i][3])
            part_unit_price.append(row[i][4])
            part_discount_amount.append(row[i][5])
            part_taxable_value.append(row[i][6])
            part_cgst_per.append(row[i][7])
    lab_data_count = len(lab_part_name)
    part_data_count = len(part_part_name)

    c, conn, status = connection()
    c.execute(
        "SELECT icici_rc_reg_number,icici_rc_reg_date,icici_rc_engine_number,icici_rc_chassis_number,icici_rc_mfg_name,icici_rc_cust_name,icici_rc_model,icici_rc_mfg_date,icici_rc_exp_date,icici_rc_rto_location,attribute_1,attribute_2,attribute_3,attribute_4 FROM icici_rc_data WHERE icici_claim_number = '%s';" %
        (claim_number))
    row = c.fetchone()
    c.close()
    conn.close()

    # wb_rc = load_workbook("azure_blob/database/local_database.xlsx")
    # rc_sheet = wb_rc['RC_data']
    # rc_max_row = rc_sheet.max_row
    rc_reg_number = ""
    rc_reg_date = ""
    rc_engine_number = ""
    rc_chassis_number = ""
    rc_mfg_name = ""
    rc_cust_name = ""
    rc_model = ""
    rc_mfg_date = ""
    rc_exp_date = ""
    rc_rto_loc = ""
    rc_veichle_class = ""
    rc_image_quality = ""
    rc_veh_colour = ""
    rc_veh_capacity = ""
    # for i in range(2,rc_max_row + 1):
    #     cell_obj = rc_sheet.cell(row=i, column=1)
    #     # #print(cell_obj.value)
    #     # #print(claim_number)
    #     if cell_obj.value == claim_number:
    if row is not None:
        rc_reg_number = row[0]
        rc_reg_date = row[1]
        rc_engine_number = row[2]
        rc_chassis_number = row[3]
        rc_mfg_name = row[4]
        rc_cust_name = row[5]
        rc_model = row[6]
        rc_mfg_date = row[7]
        rc_exp_date = row[8]
        rc_rto_loc = row[9]
        rc_image_quality = row[10]
        rc_veichle_class = row[11]
        rc_veh_colour = row[12]
        rc_veh_capacity = row[13]
        #print("rc_veh_capacity :", rc_veh_capacity)
    #         break
    #     else:
    #         continue
    # wb_rc.save("azure_blob/database/local_database.xlsx")
    # wb_rc.close()

    c, conn, status = connection()
    c.execute(
        "SELECT icici_dl_number,icici_dl_exp_date,icici_dl_cust_name,icici_dl_father_name,icici_dl_issued_on,icici_dl_dob,icici_dl_type_of_vehicle,icici_dl_permit,attribute_1 FROM icici_dl_data WHERE icici_claim_number = '%s';" %
        (claim_number))
    row = c.fetchone()
    c.close()
    conn.close()

    # wb_rc = load_workbook("azure_blob/database/local_database.xlsx")
    # rc_sheet = wb_rc['DL_data']
    # rc_max_row = rc_sheet.max_row
    dl_number = ""
    dl_exp_date = ""
    dl_cust_name = ""
    dl_father_name = ""
    dl_doi_name = ""
    dl_dob_name = ""
    dl_veh_type = ""
    dl_permit = ""
    dl_image_quality = ""
    # for i in range(1, rc_max_row + 1):
    #     cell_obj = rc_sheet.cell(row=i, column=1)
    #     if cell_obj.value == claim_number:
    if row is not None:
        dl_number = row[0]
        dl_exp_date = row[1]
        dl_cust_name = row[2]
        dl_father_name = row[3]
        dl_doi_name = row[4]
        dl_dob_name = row[5]
        dl_veh_type = row[6]
        dl_permit = row[7]
        dl_image_quality = row[8]
    #         break
    #     else:
    #         continue
    #
    # wb_rc.save("azure_blob/database/local_database.xlsx")
    # wb_rc.close()

    c, conn, status = connection()
    c.execute(
        "SELECT icici_pd_full_name,icici_pd_father_name,icici_pd_dob,icici_pd_pan_number,attribute1 FROM icici_pan_data WHERE icici_claim_number = '%s'" %
        (claim_number))
    row = c.fetchone()
    c.close()
    conn.close()

    pan_number = ""
    pan_full_name = ""
    pan_father_name = ""
    pan_dob = ""
    pan_image_quality = ""
    if row is not None:
        pan_full_name = row[0]
        pan_father_name = row[1]
        pan_dob = row[2]
        pan_number = row[3]
        pan_image_quality = row[4]

    c, conn, status = connection()
    c.execute(
        "SELECT icic_ad_aadhar_number,icici_ad_dob,icici_ad_aadhar_name,icici_ad_aadhar_address_line1,icici_ad_aadhar_address_line2,icici_ad_city,icici_ad_state,icici_ad_pincode,attribute_1 FROM icici_aadhar_data WHERE icici_claim_number = '%s'" %
        (claim_number))
    row = c.fetchone()
    #print(row)
    c.close()
    conn.close()

    aadhar_number = ""
    aadhar_dob = ""
    aadhar_name = ""
    address_line_1 = ""
    address_line_2 = ""
    city = ""
    state = ""
    pincode = ""
    aadhar_image_quality = ""
    if row is not None:
        aadhar_number = row[0]
        aadhar_dob = row[1]
        aadhar_name = row[2]
        address_line_1 = row[3]
        address_line_2 = row[4]
        city = row[5]
        state = row[6]
        pincode = row[7]
        aadhar_image_quality = row[8]

    c, conn, status = connection()
    c.execute(
        "SELECT icici_is_claim_number,icici_is_policy_number,icici_is_intimation_date,icici_is_reg_number,icici_is_engine_number,icici_is_chassis_number,icici_is_make,icici_is_date_of_loss,icici_is_driver_name,attribute_1 FROM icici_intimation_data WHERE icici_claim_number = '%s';" %
        (claim_number))
    row = c.fetchone()
    c.close()
    conn.close()

    is_intimation_date = ""
    is_intimation_rec = ""
    is_reg_no = ""
    is_engine_no = ""
    is_chassis_no = ""
    is_make = ""
    is_model = ""
    is_year_of_mfg = ""
    is_date_of_loss = ""
    is_claim_no = ""
    is_policy_no = ""
    is_driver_name = ""
    is_confidence_level = ""
    if row is not None:
        is_claim_no = row[0]
        is_policy_no = row[1]
        is_intimation_date = row[2]
        is_reg_no = row[3]
        is_engine_no = row[4]
        is_chassis_no = row[5]
        is_make = row[6]
        # is_model = rc_sheet.cell(row=i, column=9).value
        # is_year_of_mfg = rc_sheet.cell(row=i, column=9).value
        is_date_of_loss = row[7]
        is_driver_name = row[8]
        is_confidence_level = row[9]

    c, conn, status = connection()
    c.execute(
        "SELECT icici_pf_insured_name,icici_pf_insured_type,icici_pf_policy_number,icici_pf_pre_policy_number,icici_pf_period_of_insurance,icici_pf_dob,icici_vechile_cost,icici_pf_add_on,icici_pf_basic_third_party,icici_pf_chassis_number,icici_pf_engine_number,icici_pf_make,icici_pf_model,icici_pf_year_mfg,icici_pf_reg_number,attribute_1	FROM icici_policy_form_data WHERE icici_claim_number = '%s';" %
        (claim_number))
    row = c.fetchone()
    c.close()
    conn.close()

    pf_insured_name = ""
    pf_insured_type = ""
    pf_policy_no = ""
    pf_pre_policy_no = ""
    pf_period_of_insurance = ""
    pf_dob = ""
    pf_veh_cost = ""
    pf_add_on = ""
    pf_basic_third_party = ""
    pf_chassis_no = ""
    pf_engine_no = ""
    pf_make = ""
    pf_model = ""
    pf_year_of_mfg = ""
    pf_reg_no = ""
    pf_image_quality = ""
    # for i in range(1, rc_max_row + 1):
    #     cell_obj = rc_sheet.cell(row=i, column=1)
    #     if cell_obj.value == claim_number:
    if row is not None:
        pf_insured_name = row[0]
        pf_insured_type = row[1]
        pf_policy_no = row[2]
        pf_pre_policy_no = row[3]
        pf_period_of_insurance = row[4]
        pf_dob = row[5]
        pf_veh_cost = row[6]
        pf_add_on = row[7]
        pf_basic_third_party = row[8]
        pf_chassis_no = row[9]
        pf_engine_no = row[10]
        pf_make = row[11]
        pf_model = row[12]
        pf_year_of_mfg = row[13]
        pf_reg_no = row[14]
        pf_image_quality = row[15]
    #         break
    #     else:
    #         continue
    # # #print("pf indual",pf_insured_type)
    # wb_rc.save("azure_blob/database/local_database.xlsx")
    # wb_rc.close()

    c, conn, status = connection()
    c.execute(
        "SELECT icici_cf_covernote_number,icici_cf_policy_number,icici_cf_insured_name,icici_cf_driver_name,icici_cf_driving_licence_number,icici_cf_date_of_exp,icici_cf_engine_number,icici_cf_reg_number,icici_cf_make,icici_cf_model,icici_cf_chassis_number,icici_cf_date_time,icici_cf_accident_details,icici_cf_signature_pg2,icici_cf_signature_pg3,icici_cf_signature_pg4,attribute_1 FROM icici_claim_form_data WHERE icici_claim_number = '%s';" %
        (claim_number))
    row = c.fetchone()
    c.close()
    conn.close()
    # wb_rc = load_workbook("azure_blob/database/local_database.xlsx")
    # rc_sheet = wb_rc['claim_form_data']
    # rc_max_row = rc_sheet.max_row
    cf_cover_note_number = ""
    cf_policy_number = ""
    cf_insured_name = ""
    cf_driver_name = ""
    cf_driving_licence_number = ""
    cf_date_of_expiry = ""
    cf_engine_number = ""
    cf_reg_no = ""
    cf_make = ""
    cf_model = ""
    cf_chassis_no = ""
    cf_date = ""
    cf_time = ""
    cf_accident_details = ""
    cf_signature_pg2 = ""
    cf_signature_pg3 = ""
    cf_signature_pg4 = ""
    cf_image_quality = ""
    # for i in range(1, rc_max_row + 1):
    #     cell_obj = rc_sheet.cell(row=i, column=1)
    #     if cell_obj.value == claim_number:
    if row is not None:
        cf_cover_note_number = row[0]
        cf_policy_number = row[1]
        cf_insured_name = row[2]
        cf_driver_name = row[3]
        cf_driving_licence_number = row[4]
        cf_date_of_expiry = row[5]
        cf_engine_number = row[6]
        cf_reg_no = row[7]
        cf_make = row[8]
        cf_model = row[9]
        cf_chassis_no = row[10]
        cf_date = row[11]
        # cf_time = rc_sheet.cell(row=i, column=14).value
        cf_accident_details = row[12]
        cf_signature_pg2 = row[13]
        cf_signature_pg3 = row[14]
        cf_signature_pg4 = row[15]
        cf_image_quality = row[16]
    #         break
    #     else:
    #         continue
    # wb_rc.save("azure_blob/database/local_database.xlsx")
    # wb_rc.close()

    c, conn, status = connection()
    c.execute(
        "SELECT icici_eb_estimation_number,icici_eb_reg_number,icici_eb_policy_number,attribute_1 FROM icici_estimation_basics_data WHERE icici_claim_number = '%s';" %
        (claim_number))
    row = c.fetchone()
    c.close()
    conn.close()

    es_estimation_number = ""
    es_reg_no = ""
    es_policy_number = ""
    estimation_version = ""
    # wb_es_basic = load_workbook("azure_blob/database/local_database.xlsx")
    # wb_es_basic_sheet = wb_es_basic['estimation_sheet_basic']
    # wb_es_basic_max_row = wb_es_basic_sheet.max_row
    # for i in range(1, wb_es_basic_max_row + 1):
    #     cell_obj = wb_es_basic_sheet.cell(row=i, column=1)
    #     # #print(cell_obj.value)
    #     if cell_obj.value == claim_number:
    if row is not None:
        es_estimation_number = row[0]
        es_reg_no = row[1]
        es_policy_number = row[2]
        estimation_version = row[3]
    #         break
    #     else:
    #         continue
    # wb_es_basic.save("azure_blob/database/local_database.xlsx")
    #print("inversion", invoice_version)
    c, conn, status = connection()
    c.execute(
        "SELECT icici_epd_part_number,icici_epd_part_name,icici_epd_hsn,icici_epd_qty,icici_epd_unit_price,icici_epd_type_charges FROM icici_estimation_part_details WHERE icici_claim_number_ref = '%s' and attribute_1 = '%s';" %
        ("ref_" + str(claim_number), estimation_version))
    row = c.fetchall()
    c.close()
    conn.close()
    lab_es_part_number = []
    part_es_part_number = []
    lab_es_qty = []
    part_es_qty = []
    for i in range(len(row)):
        if row[i][5] == "Labour":
            lab_es_part_number.append(row[i][0])
            lab_es_part_name.append(row[i][1])
            lab_es_hsn.append(row[i][2])
            lab_es_qty.append(row[i][3])
            lab_es_unit_price.append(row[i][4])
        elif row[i][5] == "Part":
            part_es_part_number.append(row[i][0])
            part_es_part_name.append(row[i][1])
            part_es_hsn.append(row[i][2])
            part_es_qty.append(row[i][3])
            part_es_unit_price.append(row[i][4])
    es_data_count = len(es_part_name)
    lab_es_data_count = len(lab_es_part_name)
    part_es_data_count = len(part_es_part_name)

    if invoice_post_check == "Yes":
        rc_invoice_reg_no_post_process = ""
        pf_invoice_reg_no_post_process = ""
        is_invoice_reg_no_post_process = ""
        cf_invoice_reg_no_post_process = ""
        pf_invoice_policy_number_post_process = ""
        cf_invoice_policy_number_post_process = ""
        rc_invoice_name_post_process = ""
        pf_invoice_name_post_process = ""
        cf_invoice_name_post_process = ""
        rc_invoice_chassis_number_post_process = ""
        pf_invoice_chassis_number_post_process = ""
        is_invoice_chassis_number_post_process = ""
        cf_invoice_chassis_number_post_process = ""
        rc_invoice_engine_number_post_process = ""
        pf_invoice_engine_number_post_process = ""
        is_invoice_engine_number_post_process = ""
        cf_invoice_engine_number_post_process = ""
        c, conn, status = connection()
        c.execute(
            "SELECT icici_ib_reg_number,icici_ib_policy_number,icici_ib_policy_name,icici_ib_chasiss_number,icici_ib_engine_number FROM icici_invoice_basic_data WHERE icici_claim_number = '%s';" %
            (claim_number))
        row = c.fetchone()
        c.close()
        conn.close()
        # wb_in_basic = load_workbook("azure_blob/database/local_database.xlsx")
        # wb_in_basic_sheet = wb_in_basic['invoice_data_basic']
        # wb_in_basic_max_row = wb_in_basic_sheet.max_row
        # for i in range(1, wb_in_basic_max_row + 1):
        #     cell_obj = wb_in_basic_sheet.cell(row=i, column=1)
        #     if cell_obj.value == claim_number:
        if row is not None:
            rc_invoice_reg_no_post_process = row[0]
            pf_invoice_reg_no_post_process = row[0]
            is_invoice_reg_no_post_process = row[0]
            cf_invoice_reg_no_post_process = row[0]
            pf_invoice_policy_number_post_process = row[1]
            cf_invoice_policy_number_post_process = row[1]
            rc_invoice_name_post_process = row[2]
            pf_invoice_name_post_process = row[2]
            cf_invoice_name_post_process = row[2]
            rc_invoice_chassis_number_post_process = row[3]
            pf_invoice_chassis_number_post_process = row[3]
            is_invoice_chassis_number_post_process = row[3]
            cf_invoice_chassis_number_post_process = row[3]
            rc_invoice_engine_number_post_process = row[4]
            pf_invoice_engine_number_post_process = row[4]
            is_invoice_engine_number_post_process = row[4]
            cf_invoice_engine_number_post_process = row[4]
        #         break
        #     else:
        #         continue
        # wb_in_basic.save("azure_blob/database/local_database.xlsx")
        # wb_in_basic.close()



    else:
        rc_invoice_reg_no_post_process = rc_reg_number
        pf_invoice_reg_no_post_process = pf_reg_no
        is_invoice_reg_no_post_process = is_reg_no
        cf_invoice_reg_no_post_process = cf_reg_no
        pf_invoice_policy_number_post_process = pf_policy_no
        cf_invoice_policy_number_post_process = cf_policy_number
        rc_invoice_name_post_process = rc_cust_name
        pf_invoice_name_post_process = pf_insured_name
        cf_invoice_name_post_process = cf_insured_name
        rc_invoice_chassis_number_post_process = rc_chassis_number
        pf_invoice_chassis_number_post_process = pf_chassis_no
        is_invoice_chassis_number_post_process = is_chassis_no
        cf_invoice_chassis_number_post_process = cf_chassis_no
        rc_invoice_engine_number_post_process = rc_engine_number
        pf_invoice_engine_number_post_process = pf_engine_no
        is_invoice_engine_number_post_process = is_engine_no
        cf_invoice_engine_number_post_process = cf_engine_number

    my_stat = ""
    if in_stat == "hidden" and es_stat == "hidden":
        my_stat = ""
    else:
        my_stat = "hidden"
    part_name = []
    part_name_id = []
    try:
        my_json = get_part_data()
        
        for i in range(len(my_json)):

            part_name.append(my_json[i].get('Name'))
            part_name_id.append(my_json[i].get('ID'))
    except:
        pass
    lab_data_count = len(lab_part_name)
    part_data_count = len(part_part_name)
    number_of_rows = lab_data_count + part_data_count
    labour_part_break = lab_data_count
    javascript_part_name = []
    javascript_part_demo = []
    for i in range(number_of_rows):
        javascript_part_name.append("part_name"+str(i))
        javascript_part_demo.append("demo_subpart"+str(i))

    Lookup_id,lookup_name=get_dropdownjsondata()
    Insured_type_LOOKUP_ID, Insured_type_LOOKUP_NAME,permit_LOOKUP_ID,permit_LOOKUP_NAME,Type_of_Licence_LOOKUP_ID,Type_of_Licence_LOOKUP_NAME,RTO_Locations_LOOKUP_ID,RTO_Locations_LOOKUP_NAME,Road_Type_LOOKUP_ID,Road_Type_LOOKUP_NAME,NatureofGoods_LOOKUP_ID,NatureofGoods_LOOKUP_NAME,Driver_Qualification_LOOKUP_ID,Driver_Qualification_LOOKUP_NAME,Vehicledrivenby_LOOKUP_ID,Vehicledrivenby_LOOKUP_NAME,Causeofloss_LOOKUP_ID,Causeofloss_LOOKUP_NAME=all_DropDowndata()
    
    print(invoice_url_pdf)
    
    if os.path.exists('static/invoice_pdf_temp/'+str(myid)+'_invoice.pdf'):
        print("file exist")
    else:
        r = requests.get(invoice_url_pdf, allow_redirects=True)
        open('static/invoice_pdf_temp/'+str(myid)+'_invoice.pdf', 'wb').write(r.content)
    
    invoice_url_pdf = ""
    invoice_url_pdf = 'static/invoice_pdf_temp/'+str(myid)+'_invoice.pdf'
    api_policy_data = get_policy_details(myid)
    return render_template("claim.html",Insured_type_LOOKUP_ID=Insured_type_LOOKUP_ID,Insured_type_LOOKUP_NAME=Insured_type_LOOKUP_NAME,
                           permit_LOOKUP_ID=permit_LOOKUP_ID,permit_LOOKUP_NAME=permit_LOOKUP_NAME,Type_of_Licence_LOOKUP_ID=Type_of_Licence_LOOKUP_ID,Type_of_Licence_LOOKUP_NAME=Type_of_Licence_LOOKUP_NAME,
                           RTO_Locations_LOOKUP_ID=RTO_Locations_LOOKUP_ID,RTO_Locations_LOOKUP_NAME=RTO_Locations_LOOKUP_NAME,Road_Type_LOOKUP_ID=Road_Type_LOOKUP_ID,Road_Type_LOOKUP_NAME=Road_Type_LOOKUP_NAME,
                           NatureofGoods_LOOKUP_ID=NatureofGoods_LOOKUP_ID,NatureofGoods_LOOKUP_NAME=NatureofGoods_LOOKUP_NAME,Driver_Qualification_LOOKUP_ID=Driver_Qualification_LOOKUP_ID,Driver_Qualification_LOOKUP_NAME=Driver_Qualification_LOOKUP_NAME,
                           Vehicledrivenby_LOOKUP_ID=Vehicledrivenby_LOOKUP_ID,Vehicledrivenby_LOOKUP_NAME=Vehicledrivenby_LOOKUP_NAME,Causeofloss_LOOKUP_ID=Causeofloss_LOOKUP_ID,Causeofloss_LOOKUP_NAME=Causeofloss_LOOKUP_NAME,
                           api_policy_data = api_policy_data,Lookup_id=Lookup_id,lookup_name=lookup_name,labour_part_break = labour_part_break,javascript_part_demo = javascript_part_demo,javascript_part_name = javascript_part_name,part_name = part_name,part_name_id = part_name_id,ui_last_login = session.get('ui_last_login'), username=username, lab_es_part_number=lab_es_part_number,
                           part_es_part_number=part_es_part_number, lab_es_qty=lab_es_qty, part_es_qty=part_es_qty,
                           lab_es_data_count=lab_es_data_count, part_es_data_count=part_es_data_count,
                           part_es_hsn=part_es_hsn, part_es_unit_price=part_es_unit_price,
                           lab_es_part_name=lab_es_part_name, lab_es_hsn=lab_es_hsn,
                           lab_es_unit_price=lab_es_unit_price, part_es_part_name=part_es_part_name,
                           lab_part_number=lab_part_number, part_part_number=part_part_number,
                           lab_data_count=lab_data_count, part_data_count=part_data_count, lab_part_name=lab_part_name,
                           part_part_name=part_part_name, lab_hsn=lab_hsn, part_hsn=part_hsn, lab_qty=lab_qty,
                           part_qty=part_qty, lab_unit_price=lab_unit_price, part_unit_price=part_unit_price,
                           lab_discount_amount=lab_discount_amount, part_discount_amount=part_discount_amount
                           , lab_taxable_value=lab_taxable_value, part_taxable_value=part_taxable_value,
                           lab_cgst_per=lab_cgst_per, part_cgst_per=part_cgst_per, address_line_1=address_line_1,
                           address_line_2=address_line_2, city=city, state=state, pincode=pincode,
                           dl_veh_type=dl_veh_type, dl_permit=dl_permit, dl_dob_name=dl_dob_name,
                           dl_doi_name=dl_doi_name, dl_father_name=dl_father_name, dl_bck_url=dl_bck_url,
                           is_policy_no=is_policy_no, is_claim_no=is_claim_no, aadhar_name=aadhar_name,
                           aadhar_dob=aadhar_dob, aadhar_number=aadhar_number, pan_dob=pan_dob,
                           pan_father_name=pan_father_name, pan_full_name=pan_full_name, pan_number=pan_number,
                           pan_url=pan_url, aadhar_url=aadhar_url, dl_bck_stat=dl_bck_stat,
                           dl_stat_row_bck=dl_stat_row_bck, pan_stat=pan_stat, aadhar_stat=aadhar_stat,
                           pan_stat_row=pan_stat_row, aadhar_stat_row=aadhar_stat_row,
                           cf_invoice_engine_number_post_process=cf_invoice_engine_number_post_process,
                           is_invoice_engine_number_post_process=is_invoice_engine_number_post_process,
                           pf_invoice_engine_number_post_process=pf_invoice_engine_number_post_process,
                           rc_invoice_engine_number_post_process=rc_invoice_engine_number_post_process,
                           cf_invoice_chassis_number_post_process=cf_invoice_chassis_number_post_process,
                           is_invoice_chassis_number_post_process=is_invoice_chassis_number_post_process,
                           pf_invoice_chassis_number_post_process=pf_invoice_chassis_number_post_process,
                           rc_invoice_chassis_number_post_process=rc_invoice_chassis_number_post_process,
                           cf_invoice_name_post_process=cf_invoice_name_post_process,
                           pf_invoice_name_post_process=pf_invoice_name_post_process,
                           rc_invoice_name_post_process=rc_invoice_name_post_process,
                           cf_invoice_policy_number_post_process=cf_invoice_policy_number_post_process,
                           pf_invoice_policy_number_post_process=pf_invoice_policy_number_post_process,
                           cf_invoice_reg_no_post_process=cf_invoice_reg_no_post_process,
                           is_invoice_reg_no_post_process=is_invoice_reg_no_post_process,
                           rc_invoice_reg_no_post_process=rc_invoice_reg_no_post_process,
                           pf_invoice_reg_no_post_process=pf_invoice_reg_no_post_process, dl_stat_row=dl_stat_row,
                           rc_stat_row=rc_stat_row, cf_stat_row=cf_stat_row,
                           is_stat_row=is_stat_row, pf_stat_row=pf_stat_row, my_stat=my_stat, es_stat=es_stat,
                           es_data_count=es_data_count, es_part_name=es_part_name, es_hsn=es_hsn,
                           es_unit_price=es_unit_price, dl_url=dl_url, es_estimation_number=es_estimation_number,
                           es_reg_no=es_reg_no,
                           es_policy_number=es_policy_number, rc_url=rc_url, policy_form_1_url=policy_form_1_url,
                           intimation_sheet_page1_url=intimation_sheet_page1_url, claim_form_url=claim_form_url,
                           ui_part_name=ui_part_name, ui_hsn=ui_hsn, ui_qty=ui_qty, ui_unit_price=ui_unit_price,
                           ui_discount_amount=ui_discount_amount, ui_taxable_value=ui_taxable_value,
                           ui_cgst_per=ui_cgst_per, rc_reg_number=rc_reg_number, rc_veichle_class=rc_veichle_class,
                           rc_reg_date=rc_reg_date, rc_engine_number=rc_engine_number,
                           rc_chassis_number=rc_chassis_number,
                           rc_mfg_name=rc_mfg_name, rc_cust_name=rc_cust_name, rc_model=rc_model,
                           rc_mfg_date=rc_mfg_date, rc_exp_date=rc_exp_date, rc_rto_loc=rc_rto_loc, dl_number=dl_number,
                           dl_exp_date=dl_exp_date, dl_cust_name=dl_cust_name, is_intimation_date=is_intimation_date,
                           is_intimation_rec=is_intimation_rec, is_reg_no=is_reg_no,
                           is_engine_no=is_engine_no, is_chassis_no=is_chassis_no, is_make=is_make, is_model=is_model,
                           is_year_of_mfg=is_year_of_mfg, is_date_of_loss=is_date_of_loss,
                           pf_insured_name=pf_insured_name, pf_insured_type=pf_insured_type, pf_policy_no=pf_policy_no,
                           pf_pre_policy_no=pf_pre_policy_no, pf_period_of_insurance=pf_period_of_insurance,
                           pf_dob=pf_dob,
                           pf_veh_cost=pf_veh_cost, pf_add_on=pf_add_on, pf_basic_third_party=pf_basic_third_party,
                           pf_chassis_no=pf_chassis_no, pf_engine_no=pf_engine_no, pf_make=pf_make,
                           pf_model=pf_model, pf_year_of_mfg=pf_year_of_mfg, pf_reg_no=pf_reg_no,
                           cf_cover_note_number=cf_cover_note_number, cf_policy_number=cf_policy_number,
                           cf_insured_name=cf_insured_name, cf_driver_name=cf_driver_name,
                           cf_driving_licence_number=cf_driving_licence_number, cf_date_of_expiry=cf_date_of_expiry,
                           cf_engine_number=cf_engine_number, cf_reg_no=cf_reg_no, cf_make=cf_make, cf_model=cf_model,
                           cf_chassis_no=cf_chassis_no, claim_number_flask=myid,
                           dl_stat=dl_stat, rc_stat=rc_stat, cf_stat=cf_stat, is_stat=is_stat, pf_stat=pf_stat,
                           in_stat=in_stat, dl_icon_img=dl_icon_img, rc_icon_img=rc_icon_img, cf_icon_img=cf_icon_img,
                           is_icon_img=is_icon_img, pf_icon_img=pf_icon_img,
                           invoice_basic_invoice_number=invoice_basic_invoice_number,
                           invoice_basic_garage_name=invoice_basic_garage_name, invoice_basic_model=invoice_basic_model,
                           invoice_policy_number_post_process=invoice_policy_number_post_process,
                           claim_number=claim_number,
                           invoice_basic_gstn_number=invoice_basic_gstn_number,invoice_url_pdf = invoice_url_pdf, aadhar_url_bck=aadhar_url_bck,
                           aadhar_stat_row_bck=aadhar_stat_row_bck, aadhar_stat_bck=aadhar_stat_bck,
                           rc_bck_url=rc_bck_url, rc_bck_stat=rc_bck_stat, rc_stat_row_bck=rc_stat_row_bck,
                           claim_form_url_2=claim_form_url_2, claim_form_url_3=claim_form_url_3,
                           claim_form_url_4=claim_form_url_4,
                           cf_stat_row_4=cf_stat_row_4, cf_stat_row_2=cf_stat_row_2, cf_stat_row_3=cf_stat_row_3,
                           cf_date=cf_date, cf_time=cf_time, cf_accident_details=cf_accident_details,
                           cf_signature_pg2=cf_signature_pg2, cf_signature_pg3=cf_signature_pg3,
                           cf_signature_pg4=cf_signature_pg4, view_permission=view_permission, edit_table=edit_table,
                           gey_out_remove_button=gey_out_remove_button, dl_image_quality=dl_image_quality,
                           rc_image_quality=rc_image_quality, pan_image_quality=pan_image_quality,
                           aadhar_image_quality=aadhar_image_quality, rc_veh_colour=rc_veh_colour,
                           rc_veh_capacity=rc_veh_capacity,
                           is_driver_name=is_driver_name, is_confidence_level=is_confidence_level,
                           pf_image_quality=pf_image_quality, cf_image_quality=cf_image_quality)


@blue_print.route('/final_proceed/<string:myid_proc>', methods=["GET", "POST"])
@login_required
@csrf.exempt
def final_proceed(myid_proc):
    print("in final")
    c, conn, status = connection()
    c.execute("UPDATE icici_email_recieved_document SET icici_status = %s WHERE icici_claim_number = %s",
              ("Complete", myid_proc))
    conn.commit()
    c.close()
    conn.close()
    c, conn, status = connection()
    c.execute(
        "SELECT icici_url_dl_frt,icici_url_dl_bck,icici_url_rc_frt,icici_url_rc_bck,icici_url_pan,icici_url_aadhar_frt,icici_url_aadhar_bck,icici_url_intimation,icici_url_policy_form,icici_url_claim_form_pg1,icici_url_claim_form_pg2,icici_url_claim_form_pg3,icici_url_claim_form_pg4,icici_url_invoice,icici_url_estimation FROM icici_document_url WHERE icici_claim_number = '%s';" % (
            myid_proc))
    row = c.fetchone()
    c.close()
    conn.close()
    #print(row[14])
    c, conn, status = connection()
    if str(row[0]).__contains__("http"):
        # dl
        dl_number_changed = str(request.form['dl_number_changed'])
        dl_exp_changed = str(request.form['dl_exp_changed'])
        dl_name_changed = str(request.form['dl_name_changed'])
        dl_father_name_changed = str(request.form['dl_father_name_changed'])
        dl_doi_changed = str(request.form['dl_doi_changed'])
        dl_dob_changed = str(request.form['dl_dob_changed'])
        dl_veh_type_changed = str(request.form['dl_veh_type_changed'])
        dl_permit_type_changed = str(request.form['dl_permit_type_changed'])
        c.execute(
            "UPDATE icici_dl_data SET icici_dl_number = %s,icici_dl_cust_name = %s,icici_dl_father_name = %s,icici_dl_issued_on = %s,icici_dl_dob = %s,icici_dl_exp_date = %s,icici_dl_type_of_vehicle = %s,icici_dl_permit = %s WHERE icici_claim_number = %s",
            (dl_number_changed, dl_name_changed, dl_father_name_changed, dl_doi_changed, dl_dob_changed, dl_exp_changed,
             dl_veh_type_changed, dl_permit_type_changed, myid_proc))
        conn.commit()
    if str(row[2]).__contains__("http"):
        # rc
        rc_reg_no_changed = str(request.form['rc_reg_no_changed'])
        rc_reg_date_changed = str(request.form['rc_reg_date_changed'])
        rc_engine_no_changed = str(request.form['rc_engine_no_changed'])
        rc_chassis_no_changed = str(request.form['rc_chassis_no_changed'])
        rc_mfg_name_changed = str(request.form['rc_mfg_name_changed'])
        rc_name_changed = str(request.form['rc_name_changed'])
        rc_model_changed = str(request.form['rc_model_changed'])
        rc_mfg_date_changed = str(request.form['rc_mfg_date_changed'])
        rc_valid_date_changed = str(request.form['rc_valid_date_changed'])
        rc_rto_loc_changed = str(request.form['rc_rto_loc_changed'])
        rc_veichle_class_changed = str(request.form['rc_veichle_class_changed'])
        rc_veichle_color_changed = str(request.form['rc_veichle_color_changed'])
        rc_veichle_Capacity_changed = str(request.form['rc_veichle_Capacity_changed'])
        c.execute(
            "UPDATE icici_rc_data SET icici_rc_reg_number = %s,icici_rc_reg_date = %s,icici_rc_exp_date = %s,icici_rc_chassis_number = %s,icici_rc_engine_number = %s,icici_rc_cust_name = %s,icici_rc_mfg_date = %s,icici_rc_model = %s,icici_rc_rto_location = %s,icici_rc_mfg_name = %s ,attribute_2 = %s,attribute_3 = %s,attribute_4 = %s WHERE icici_claim_number = %s",
            (rc_reg_no_changed, rc_reg_date_changed, rc_valid_date_changed, rc_chassis_no_changed, rc_engine_no_changed,
             rc_name_changed, rc_mfg_date_changed, rc_model_changed, rc_rto_loc_changed, rc_mfg_name_changed,
             rc_veichle_class_changed, rc_veichle_color_changed, rc_veichle_Capacity_changed, myid_proc))
        conn.commit()
    if str(row[4]).__contains__("http"):
        # pan
        pan_number_changed = str(request.form['pan_number_changed'])
        pan_full_name_changed = str(request.form['pan_full_name_changed'])
        pan_father_name_changed = str(request.form['pan_father_name_changed'])
        pan_dob_changed = str(request.form['pan_dob_changed'])
        c.execute(
            "UPDATE icici_pan_data SET icici_pd_full_name = %s,icici_pd_father_name = %s,icici_pd_dob = %s,icici_pd_pan_number = %s WHERE icici_claim_number = %s",
            (pan_full_name_changed, pan_father_name_changed, pan_dob_changed, pan_number_changed, myid_proc))
        conn.commit()
    if str(row[5]).__contains__("http"):
        # aadhar
        aadhar_number_changed = str(request.form['aadhar_number_changed'])
        aadhar_name_changed = str(request.form['aadhar_name_changed'])
        aadhar_dob_changed = str(request.form['aadhar_dob_changed'])
        address_line_one_changed = str(request.form['address_line_one_changed'])
        address_line_two_changed = str(request.form['address_line_two_changed'])
        city_changed = str(request.form['city_changed'])
        state_changed = str(request.form['state_changed'])
        pincode_changed = str(request.form['pincode_changed'])
        c.execute(
            "UPDATE icici_aadhar_data SET icic_ad_aadhar_number = %s,icici_ad_dob = %s,icici_ad_aadhar_name = %s,icici_ad_aadhar_address_line1 = %s,icici_ad_aadhar_address_line2 = %s,icici_ad_city = %s,icici_ad_state = %s, icici_ad_pincode = %s WHERE icici_claim_number = %s",
            (aadhar_number_changed, aadhar_dob_changed, aadhar_name_changed, address_line_one_changed,
             address_line_two_changed, city_changed, state_changed,
             pincode_changed, myid_proc))
        conn.commit()
    if str(row[7]).__contains__("http"):
        # intimation
        is_intimation_date_changed = str(request.form['is_intimation_date_changed'])
        is_reg_no_changed = str(request.form['is_reg_no_changed'])
        is_engine_no_changed = str(request.form['is_engine_no_changed'])
        is_chassis_no_changed = str(request.form['is_chassis_no_changed'])
        is_make_changed = str(request.form['is_make_changed'])
        is_model_changed = str(request.form['is_model_changed'])
        is_driver_name_changed = str(request.form['is_driver_name_changed'])
        is_date_of_loss_changed = str(request.form['is_date_of_loss_changed'])
        c.execute(
            "UPDATE icici_intimation_data SET icici_is_date_of_loss = %s ,icici_is_intimation_date = %s ,icici_is_make = %s ,icici_is_chassis_number = %s,icici_is_engine_number = %s ,icici_is_reg_number = %s,icici_is_driver_name = %s WHERE icici_claim_number = %s;",
            (is_date_of_loss_changed, is_intimation_date_changed, is_make_changed, is_chassis_no_changed,
             is_engine_no_changed, is_reg_no_changed, is_driver_name_changed, myid_proc))
        conn.commit()
    if str(row[8]).__contains__("http"):
        # pf
        pf_insured_name_changed = str(request.form['pf_insured_name_changed'])
        insured_type_changed = str(request.form['insured_type_changed'])
        policy_no_changed = str(request.form['policy_no_changed'])
        pre_policy_no_changed = str(request.form['pre_policy_no_changed'])
        period_of_insurance_changed = str(request.form['period_of_insurance_changed'])
        dob_changed = str(request.form['dob_changed'])
        veh_cost_changed = str(request.form['veh_cost_changed'])
        add_on_changed = str(request.form['add_on_changed'])
        basic_third_party_changed = str(request.form['basic_third_party_changed'])
        chassis_no_changed = str(request.form['chassis_no_changed'])
        engine_no_changed = str(request.form['engine_no_changed'])
        pf_make_changed = str(request.form['pf_make_changed'])
        year_of_mfg_changed = str(request.form['year_of_mfg_changed'])
        pf_reg_no_changed = str(request.form['pf_reg_no_changed'])
        pf_cubic_changed = str(request.form['pf_cubic_changed'])
        c.execute(
            "UPDATE icici_policy_form_data SET icici_pf_insured_name = %s,icici_pf_insured_type = %s,icici_pf_policy_number = %s,icici_pf_pre_policy_number = %s,icici_pf_period_of_insurance = %s,icici_pf_dob = %s,icici_vechile_cost	 = %s,icici_pf_add_on = %s,icici_pf_basic_third_party = %s,icici_pf_chassis_number = %s,icici_pf_engine_number = %s,icici_pf_make = %s,icici_pf_year_mfg = %s,icici_pf_reg_number = %s WHERE icici_claim_number = %s",
            (pf_insured_name_changed, insured_type_changed, policy_no_changed, pre_policy_no_changed,
             period_of_insurance_changed, dob_changed, veh_cost_changed, add_on_changed,
             basic_third_party_changed, chassis_no_changed, engine_no_changed, pf_make_changed, year_of_mfg_changed,
             pf_reg_no_changed, myid_proc))
        conn.commit()
    if str(row[9]).__contains__("http"):
        cover_note_number_changed = str(request.form['cover_note_number_changed'])
        policy_number_changed = str(request.form['policy_number_changed'])
        cf_insured_name_changed = str(request.form['cf_insured_name_changed'])
        driver_name_changed = str(request.form['driver_name_changed'])
        driving_licence_number_changed = str(request.form['driving_licence_number_changed'])
        date_of_expiry_changed = str(request.form['date_of_expiry_changed'])
        cf_reg_no_changed = str(request.form['cf_reg_no_changed'])
        engine_number_changed = str(request.form['engine_number_changed'])
        chassis_number_changed = str(request.form['chassis_number_changed'])
        cf_make_changed = str(request.form['cf_make_changed'])
        cf_model_changed = str(request.form['cf_model_changed'])
        cf_date_changed = str(request.form['cf_date_changed'])
        cf_doa_changed = str(request.form['cf_doa_changed'])
        cf_sig2_changed = str(request.form['cf_sig2_changed'])
        cf_sig3_changed = str(request.form['cf_sig3_changed'])
        cf_sig4_changed = str(request.form['cf_sig4_changed'])
        c.execute(
            "UPDATE icici_claim_form_data SET icici_cf_covernote_number = %s,icici_cf_policy_number = %s,icici_cf_insured_name =%s,icici_cf_driver_name = %s,icici_cf_driving_licence_number = %s,	icici_cf_date_of_exp = %s,icici_cf_engine_number=%s,icici_cf_reg_number =%s,icici_cf_make =%s,icici_cf_model=%s,icici_cf_chassis_number=%s,icici_cf_date_time=%s,icici_cf_accident_details =%s,icici_cf_signature_pg2=%s,icici_cf_signature_pg3=%s,icici_cf_signature_pg4=%s WHERE icici_claim_number = %s",
            (cover_note_number_changed, policy_number_changed, cf_insured_name_changed, driver_name_changed,
             driving_licence_number_changed, date_of_expiry_changed,
             engine_number_changed, cf_reg_no_changed, cf_make_changed, cf_model_changed, chassis_number_changed,
             cf_date_changed, cf_doa_changed, cf_sig2_changed, cf_sig3_changed, cf_sig4_changed, myid_proc))

        conn.commit()

    if str(row[13]).__contains__("http"):
        inv_part_part_number = request.form.getlist("inv_part_part_number")
        inv_part_part_name = request.form.getlist("inv_part_part_name")
        inv_part_part_hsn = request.form.getlist("inv_part_part_hsn")
        inv_part_part_qty = request.form.getlist("inv_part_part_qty")
        inv_part_part_unity_price = request.form.getlist("inv_part_part_unity_price")
        inv_part_part_discount_amount = request.form.getlist("inv_part_part_discount_amount")
        inv_part_part_taxable_value = request.form.getlist("inv_part_part_taxable_value")
        inv_part_part_sgst = request.form.getlist("inv_part_part_sgst")
        inv_part_part_scgst = request.form.getlist("inv_part_part_scgst")
        inv_lab_part_number = request.form.getlist("inv_lab_part_number")
        inv_lab_part_name = request.form.getlist("inv_lab_part_name")
        inv_lab_part_hsn = request.form.getlist("inv_lab_part_hsn")
        inv_lab_part_qty = request.form.getlist("inv_lab_part_qty")
        inv_lab_part_unity_price = request.form.getlist("inv_lab_part_unity_price")
        inv_lab_part_discount_amount = request.form.getlist("inv_lab_part_discount_amount")
        inv_lab_part_taxable_value = request.form.getlist("inv_lab_part_taxable_value")
        inv_lab_part_sgst = request.form.getlist("inv_lab_part_sgst")
        inv_lab_part_scgst = request.form.getlist("inv_lab_part_scgst")
        c.execute("SELECT attribute_1 FROM icici_invoice_basic_data WHERE icici_claim_number = '%s';" % (myid_proc))
        row_new = c.fetchone()
        version_control = int(row_new[0]) + 1
        c.execute(
            "UPDATE icici_invoice_basic_data SET attribute_1 = %s WHERE icici_claim_number = %s",
            (version_control, myid_proc))
        conn.commit()
        for i in range(len(inv_part_part_number)):
            c.execute(
                "INSERT INTO icici_part_details(icici_claim_number_ref,attribute_1,icici_ipd_part_number,icici_ipd_part_name,icici_ipd_hsn,icici_ipd_qty,icici_ipd_unity_price,icici_ipd_discount_amount,icici_ipd_tax_value,icici_ipd_cgst,icici_ipd_sgst,icici_ipd_type_charges) VALUES ( %s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                ("ref_" + str(myid_proc), str(version_control), str(inv_part_part_number[i]).strip(),
                 inv_part_part_name[i], inv_part_part_hsn[i],
                 inv_part_part_qty[i], inv_part_part_unity_price[i], inv_part_part_discount_amount[i],
                 inv_part_part_taxable_value[i],
                 inv_part_part_sgst[i], inv_part_part_scgst[i], "Part"))
            conn.commit()

        for i in range(len(inv_lab_part_number)):
            c.execute(
                "INSERT INTO icici_part_details(icici_claim_number_ref,attribute_1,icici_ipd_part_number,icici_ipd_part_name,icici_ipd_hsn,icici_ipd_unity_price,icici_ipd_discount_amount,icici_ipd_tax_value,icici_ipd_cgst,icici_ipd_sgst,icici_ipd_type_charges) VALUES ( %s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)",
                ("ref_" + str(myid_proc), str(version_control), str(inv_lab_part_number[i]).strip(),
                 inv_lab_part_name[i], inv_lab_part_hsn[i],
                 inv_lab_part_unity_price[i], inv_lab_part_discount_amount[i], inv_lab_part_taxable_value[i],
                 inv_lab_part_sgst[i], inv_lab_part_scgst[i], "Labour"))
            conn.commit()
    if str(row[14]).__contains__("http"):
        es_lab_part_number = request.form.getlist("es_lab_part_number")
        es_lab_part_name = request.form.getlist("es_lab_part_name")
        es_lab_part_hsn = request.form.getlist("es_lab_part_hsn")
        es_lab_part_unity_price = request.form.getlist("es_lab_part_unity_price")
        es_part_part_number = request.form.getlist("es_part_part_number")
        es_part_part_name = request.form.getlist("es_part_part_name")
        es_part_part_hsn = request.form.getlist("es_part_part_hsn")
        es_part_part_qty = request.form.getlist("es_part_part_qty")
        es_part_part_unity_price = request.form.getlist("es_part_part_unity_price")
        c.execute("SELECT attribute_1 FROM icici_estimation_basics_data WHERE icici_claim_number = '%s';" % (myid_proc))
        row = c.fetchone()
        version_control = int(row[0]) + 1
        c.execute(
            "UPDATE icici_estimation_basics_data SET attribute_1 = %s WHERE icici_claim_number = %s",
            (version_control, myid_proc))
        conn.commit()
        for i in range(len(es_lab_part_number)):
            c.execute(
                "INSERT INTO icici_estimation_part_details(icici_claim_number_ref,attribute_1,icici_epd_part_number,icici_epd_part_name,icici_epd_hsn,icici_epd_unit_price,icici_epd_type_charges) VALUES (%s, %s, %s,%s, %s, %s, %s)",
                ("ref_" + str(myid_proc), str(version_control), str(es_lab_part_number[i]).strip(),
                 es_lab_part_name[i], es_lab_part_hsn[i], es_lab_part_unity_price[i], "Labour"))
            conn.commit()

        for i in range(len(es_part_part_number)):
            c.execute(
                "INSERT INTO icici_estimation_part_details(icici_claim_number_ref,attribute_1,icici_epd_part_number,icici_epd_part_name,icici_epd_hsn,icici_epd_qty,icici_epd_unit_price,icici_epd_type_charges) VALUES ( %s, %s, %s, %s,%s, %s, %s, %s)",
                ("ref_" + str(myid_proc), str(version_control), str(es_part_part_number[i]).strip(),
                 es_part_part_name[i], es_part_part_hsn[i], es_part_part_qty[i], es_part_part_unity_price[i], "Part"))
            conn.commit()

    c.close()
    conn.close()
    return ('', 204)


@blue_print.route('/final_proceed_rejected/<string:myid_proc>', methods=["GET", "POST"])
@login_required
@csrf.exempt
def final_proceed_rejected(myid_proc):
    print("in final rejected")
    c, conn, status = connection()
    c.execute("UPDATE icici_email_recieved_document SET icici_status = %s WHERE icici_claim_number = %s",
              ("Rejected", myid_proc))
    conn.commit()
    c.close()
    conn.close()
    return ('', 204)

@blue_print.route("/logout")
@login_required
def logout():
    if session.get('login_session_id') is not None:
        c, conn, status = connection()
        c.execute("UPDATE icici_user_management SET login_verified = %s WHERE user_id = %s",
                  ("no_login", session.get('login_session_id')))
        conn.commit()
        c.close()
        conn.close()
    session.clear()
    gc.collect()
    password_msg = "hidden"
    already_logged_msg = "hidden"
    return render_template('login.html', password_msg=password_msg, already_logged_msg=already_logged_msg)

@blue_print.route('/sub_part_data',methods=['POST','GET'])
@csrf.exempt
def sub_part_data():
    if request.method == 'POST':
        part_id=request.json
        final_data_sub_part = get_sub_part_data(part_id)
        return jsonify(final_data_sub_part)

@blue_print.route('/iail_upload_auto_buddy',methods=["GET", "POST"])
@csrf.exempt
def iail_upload():
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    email_id = request.form['email_id']


    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    else:
        filename = secure_filename(file.filename)
        file.save('uploads/' + str(filename))
        downlaod_s3_unzip_upload('uploads/' + str(filename))
        new_claim_url = image_sas_url(str(filename).replace(".zip",""))
        threading.Thread(target=identifying_type_of_doc, args=([str(filename).replace(".zip","")],[email_id],)).start()
        resp = jsonify({'result' : 'successfull'})
        resp.status_code = 200
        return resp


@blue_print.route('/assesment_summary', methods=["GET", "POST"])
@login_required
@csrf.exempt
def assesment_summary():
    myid_proc = request.form['claim_number_new']
    c, conn, status = connection()
    c.execute(
        "SELECT icici_url_dl_frt,icici_url_dl_bck,icici_url_rc_frt,icici_url_rc_bck,icici_url_pan,icici_url_aadhar_frt,icici_url_aadhar_bck,icici_url_intimation,icici_url_policy_form,icici_url_claim_form_pg1,icici_url_claim_form_pg2,icici_url_claim_form_pg3,icici_url_claim_form_pg4,icici_url_invoice,icici_url_estimation FROM icici_document_url WHERE icici_claim_number = '%s';" % (
            myid_proc))
    row = c.fetchone()
    c.close()
    conn.close()
    print("hiiiii111")
    if str(row[13]).__contains__("http"):
        print("hiiiii")
        # invoice
        #inv_part_part_number = request.form.getlist("inv_part_part_number")
        #inv_part_part_name = request.form.getlist("inv_part_part_name")
        #inv_part_part_dropdown = request.form.getlist("part_dropdown_invoice_part")
        #inv_part_subpart_dropdown = request.form.getlist("part_dropdown_invoice_subpart")
        #inv_part_type_charges = request.form.getlist("part_type_charges")
        #inv_part_part_hsn = request.form.getlist("inv_part_part_hsn")
        #inv_part_part_qty = request.form.getlist("inv_part_part_qty")
        #inv_part_part_unity_price = request.form.getlist("inv_part_part_unity_price")
        #inv_part_part_discount_amount = request.form.getlist("inv_part_part_discount_amount")
        #inv_part_part_taxable_value = request.form.getlist("inv_part_part_taxable_value")
        #inv_part_part_sgst = request.form.getlist("inv_part_part_sgst")
        #inv_part_part_scgst = request.form.getlist("inv_part_part_scgst")
        #inv_lab_part_number = request.form.getlist("inv_lab_part_number")
        #inv_lab_part_name = request.form.getlist("inv_lab_part_name")
        #inv_lab_part_dropdown = request.form.getlist("lab_dropdown_invoice_part")
        #inv_lab_subpart_dropdown = request.form.getlist("lab_dropdown_invoice_subpart")
        #inv_lab_type_charges = request.form.getlist("lab_type_charges")
        #inv_lab_part_hsn = request.form.getlist("inv_lab_part_hsn")
        #inv_lab_part_qty = request.form.getlist("inv_lab_part_qty")
        #inv_lab_part_unity_price = request.form.getlist("inv_lab_part_unity_price")
        #inv_lab_part_discount_amount = request.form.getlist("inv_lab_part_discount_amount")
        #inv_lab_part_taxable_value = request.form.getlist("inv_lab_part_taxable_value")
        #inv_lab_part_sgst = request.form.getlist("inv_lab_part_sgst")
        #inv_lab_part_scgst = request.form.getlist("inv_lab_part_scgst")
        #final_part_ui = request.form("part_name_new")
        
        final_part_ui = []
        final_sub_part_ui = []
        final_type_charges_ui = []
        final_taxable_value_ui = []
        final_part_ui = request.form.get('part_name_new').split("@~@")
        final_part_ui.pop(0)
        final_sub_part_ui = request.form.get('subpart_name_new').split("@~@")
        final_sub_part_ui.pop(0)
        final_type_charges_ui = request.form.get('type_of_charges_new').split("@~@")
        final_type_charges_ui.pop(0)
        final_taxable_value_ui = request.form.get('taxable_value_new').replace(" ","").replace(",","").split("@~@")
        final_taxable_value_ui.pop(0)
        print(final_part_ui)
        print(len(final_part_ui))
        print(final_sub_part_ui)
        print(final_type_charges_ui)
        print(final_taxable_value_ui)
        final_list_table = []
        final_list_table = sorting_summary_invoice(final_part_ui,final_sub_part_ui,final_type_charges_ui,final_taxable_value_ui)
        #final_list_table = [['502232', 'AIR CLEANER ASSY', 'Metal', '1', 471.0, '18%', 0.0, 16423.0, 0.0, '18%', 'Repair', 0.0, 0.0, 0.0], ['502237', 'AIR CLEANER ASSY', 'Metal', '1', 0.0, '18%', 0.0, 0.0, 218.0, '18%', 'Repair', 0.0, 0.0, 0.0], ['510196', 'ANTENA', 'Metal', '1', 0.0, '18%', 222.0, 0.0, 0.0, '18%', 'Repair', 0.0, 0.0, 0.0], ['502255', 'ADJUSTER BRAKE', 'Metal', '1', 22893.0, '18%', 0.0, 0.0, 0.0, '18%', 'Repair', 0.0, 0.0, 0.0], ['503318', 'ACE', 'Metal', '1', 0.0, '18%', 2692.23, 0.0, 0.0, '18%', 'Repair', 0.0, 0.0, 0.0], ['503319', 'API LAMBRETTA', 'Metal', '1', 0.0, '18%', 0.0, 0.0, 4860.0, '18%', 'Repair', 0.0, 0.0, 0.0], ['503321', 'BIJLI AUTO', 'Metal', '1', 670.0, '18%', 0.0, 0.0, 0.0, '18%', 'Repair', 0.0, 0.0, 0.0]]
        final_part = get_part_data()
        #print(final_part)
        list_id = []
        list_name = []
        for i in range(len(final_part)):
            list_id.append(final_part[i].get("ID"))
            list_name.append(final_part[i].get("Name"))
        for i in range(len(final_list_table)):
            if final_list_table[i][0] in list_id:
                final_list_table[i][0] = list_name[list_id.index(final_list_table[i][0])]
                
        return jsonify(final_list_table)

class PrivateResource(Resource):
    # @auth.login_required
    def get(self, dir):
        #print("dir", dir)
        temp_dir = str(dir).replace("/" + str(dir).split("/")[len(str(dir).split("/")) - 1], "")
        temp_email = str(dir).split("/")[len(str(dir).split("/")) - 1]
        claim_number = str(dir).split("/")[1]
        #print(temp_dir)
        #print(temp_email)
        #print(claim_number)
        downlaod_s3_unzip_upload(temp_dir)
        # identifying_type_of_doc([claim_number])
        return "processed successfull"


#api.add_resource(PrivateResource, '/auto_buddy/<path:dir>', methods=['GET', 'POST'])
app.register_blueprint(blue_print)
if __name__ == '__main__':

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    #context = ('Cert/ins_PUBLIC.crt', 'Cert/DecryPrivate.key')
    context.load_cert_chain('Cert/ins_PUBLIC.pem', 'Cert/DecryPrivate.key')
    #app.run(debug=False,host='172.30.48.115',port= 80)
    app.run(debug=False,threaded = True,port= 8000, ssl_context=context)
    #http_server = WSGIServer(('0.0.0.0', 443), app,log=None, ssl_context=context)
    #http_server.serve_forever()

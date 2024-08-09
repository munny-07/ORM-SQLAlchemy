import os
from flask import Blueprint
from flask import request
from flask import jsonify
import traceback
import time
from flask import send_file
from sqlalchemy.orm import sessionmaker

from src.services.validations.validate import validate_for_view_details
from src.services.validations.validate import validate_for_create_pdf_details
from src.services.validations.validate import validate_for_edit_details
from src.services.validations.validate import validate_for_create_cols_pdf_details
from src.services.database.db_service import get_conn
from src.services.database.db_service import sales_view_details
from src.services.database.db_service import cpn_view_details
from src.services.database.db_service import sales_add_details
from src.services.database.db_service import cpn_add_details
from src.services.database.db_service import sales_edit_details
from src.services.database.db_service import cpn_edit_details
from src.services.pdf.download import create_sales_pdf,create_sales_cols_pdf
from src.services.pdf.download import create_cpn_pdf,create_cpn_cols_pdf

from src.services.logger.logger import configure_loggers
from src.services.logger.logger import log_mesg


routes_blueprint = Blueprint('routes', __name__)
configure_loggers()

start_time = time.time()
conn = get_conn()
Session = sessionmaker(bind=conn)
session = Session()
log_mesg(mesg="Time Taken for Connection: "+ str(time.time()-start_time))

@routes_blueprint.route('/Sales_view_api', methods=['GET'])
def salesviewdetails():
    if request.method == "GET":
        try:
            start_time = time.time()
            startpage = int(request.args.get("startpage"))
            limit = int(request.args.get("limit"))
            per_page = int(request.args.get("per_page"))
            validate_for_view_details(
                startpage=startpage,
                limit=limit,
                per_page=per_page
                )
            log_mesg(mesg="Validating the parameters for getting the stored details is complted")
            response = sales_view_details(
                session=session,
                startpage=startpage,
                limit=limit,
                per_page=per_page
                )
            log_mesg(mesg="Getting the stored details is completed")
            log_mesg(mesg="Time Taken for viewdetails API: "+ str(time.time()-start_time))
            return response
        except ValueError as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"message": str(e), "formated_error": fe}), 400
        except Exception as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"message": str(e), "formated_error": fe}), 400

@routes_blueprint.route('/CPN_view_api', methods=['GET'])
def cpnviewdetails():
    if request.method == "GET":
        try:
            start_time = time.time()
            startpage = int(request.args.get("startpage"))
            limit = int(request.args.get("limit"))
            per_page = int(request.args.get("per_page"))
            validate_for_view_details(
                startpage=startpage,
                limit=limit,
                per_page=per_page
                )
            log_mesg(mesg="Validating the parameters for getting the stored details is completed")
            response = cpn_view_details(
                session = session,
                startpage=startpage,
                limit=limit,
                per_page=per_page
                )
            log_mesg(mesg="Getting the stored details is completed")
            log_mesg(mesg="Time Taken for viewdetails API: "+ str(time.time()-start_time))
            return response
        except ValueError as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"message": str(e), "formated_error": fe}), 400
        except Exception as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"message": str(e), "formated_error": fe}), 400
     
@routes_blueprint.route('/Sales_add_api', methods=['POST'])
def salesadddetails():
    if request.method == "POST":
        try:
            start_time = time.time()
            json_data = request.json
           
            start_time = time.time()
            response = sales_add_details(session, data=json_data)
            log_mesg(mesg="Time Taken for salesadddetails API is: "+ str(time.time() - start_time))
            return response
        except ValueError as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"error": str(e), "formated_error": fe}), 400
        except Exception as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"error": str(e), "formated_error": fe}), 400

@routes_blueprint.route('/CPN_add_api', methods=['POST'])
def cpnadddetails():
    if request.method == "POST":
        try:
            start_time = time.time()
            json_data = request.json
            
            start_time = time.time()
            response = cpn_add_details(session, data=json_data)
            log_mesg(mesg="Time Taken for cpnadddetails API is: "+ str(time.time() - start_time))
            return response
        except ValueError as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"error": str(e), "formated_error": fe}), 400
        except Exception as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"error": str(e), "formated_error": fe}), 400

@routes_blueprint.route('/Sales_edit_api', methods=['POST'])
def saleseditdetails():
    if request.method == "POST":
        try:
            start_time = time.time()
            json_data = request.json
            
            validate_for_edit_details(data=json_data)
            log_mesg(mesg="Validating the parameters for getting the stored details is completed")
            
            start_time = time.time()
            response = sales_edit_details(session, data=json_data)
            log_mesg(mesg="Time Taken for updateiddetails API is: "+ str(time.time() - start_time))
            return response
        except ValueError as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"error": str(e), "formated_error": fe}), 400
        except Exception as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"error": str(e), "formated_error": fe}), 400
        
@routes_blueprint.route('/CPN_edit_api', methods=['POST'])
def cpneditdetails():
    if request.method == "POST":
        try:
            start_time = time.time()
            json_data = request.json
            
            validate_for_edit_details(data=json_data)
            log_mesg(mesg="Validating the parameters for getting the stored details is completed")

            start_time = time.time()
            response = cpn_edit_details(session, data=json_data)
            log_mesg(mesg="Time Taken for updateiddetails API is: "+ str(time.time() - start_time))
            return response
        except ValueError as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"error": str(e), "formated_error": fe}), 400
        except Exception as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"error": str(e), "formated_error": fe}), 400

@routes_blueprint.route('/create_sales_cols_pdf_api', methods=['POST'])
def createsalescolspdf():
    if request.method == "POST":
        try:
            start_time = time.time()
            json_data = request.json
            validate_for_create_cols_pdf_details(data=json_data)
            log_mesg(mesg="Validating the input parameters for creating cpn pdf is completed")
            log_mesg(mesg="Time Taken for validating the parameters of creating cpn pdf API is: "+ str(time.time() - start_time))
            start_time = time.time()
            x, status_code = create_sales_cols_pdf(session, data=json_data)
            log_mesg(mesg="Time Taken for creating cpn pdf API is: "+ str(time.time() - start_time))
            if status_code == 200:
                return send_file("output.pdf", as_attachment=True)
            else:
                return jsonify({"message": "Record not found"}), status_code
        except ValueError as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"error": str(e), "formated_error": fe}), 400
        except Exception as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"error": str(e), "formated_error": fe}), 400
        finally:
            session.close()

@routes_blueprint.route('/create_cpn_cols_pdf_api', methods=['POST'])
def createcpncolspdf():
    if request.method == "POST":
        try:
            start_time = time.time()
            json_data = request.json
            validate_for_create_cols_pdf_details(data=json_data)
            log_mesg(mesg="Validating the input parameters for creating cpn pdf is completed")
            log_mesg(mesg="Time Taken for validating the parameters of creating cpn pdf API is: "+ str(time.time() - start_time))
            start_time = time.time()
            
            x, status_code = create_cpn_cols_pdf(session, data=json_data)
            log_mesg(mesg="Time Taken for creating cpn pdf API is: "+ str(time.time() - start_time))
            if status_code == 200:
                return send_file("output.pdf", as_attachment=True)
            else:
                return jsonify({"message": "Record not found"}), status_code
            
        except ValueError as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"error": str(e), "formated_error": fe}), 400
        except Exception as e:
            fe = traceback.format_exc()
            log_mesg(mesg=str(fe), type="error")
            return jsonify({"error": str(e), "formated_error": fe}), 400
        finally:
            session.close()

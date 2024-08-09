from config import config
from src.services.logger.logger import log_mesg

def validate_for_view_details(startpage, limit, per_page):
    if startpage != None:
        if type(startpage) is int:
            if startpage <= 0:
                log_mesg(mesg="startpage is lesser or equal to 0", type="error")
                raise ValueError("startpage can't be lesser or equal to 0")
        else:
            log_mesg(mesg="startpage is not Int type", type="error")
            raise ValueError("startpage should be a number")
    else:
        log_mesg(mesg="startpage Field is Missing", type="error")
        raise ValueError("startpage Field is Missing")
    
    if limit != None:
        if type(limit) is int:
            if limit <= 0:
                log_mesg(mesg="limit is lesser or equal to 0", type="error")
                raise ValueError("limit can't be lesser or equal to 0")
        else:
            log_mesg(mesg="limit is not Int type", type="error")
            raise ValueError("limit should be a number")
    else:
        log_mesg(mesg="limit Field is Missing", type="error")
        raise ValueError("limit Field is Missing")    

    if per_page != None:
        if type(per_page) is int:
            if per_page <= 0:
                log_mesg(mesg="per_page is lesser or equal to 0", type="error")
                raise ValueError("per_page can't be lesser or equal to 0")
        else:
            log_mesg(mesg="per_page is not number", type="error")
            raise ValueError("per_page should be a number")
    else:
        log_mesg(mesg="per_page Field is Missing", type="error")
        raise ValueError("per_page Field is Missing")
    
def validate_for_create_pdf_details(data):
    if "Id" not in data.keys():
        log_mesg(mesg="Id Field is Missing", type="error")
        raise ValueError("Id Field is Missing")
    elif data["Id"] is None or data["Id"] == "":
        log_mesg("Value for Id Field is Missing", type="error")
        raise ValueError("Value for Id Field is Missing")
    elif type(data["Id"]) is int:
        if data["Id"] <= 0:
            log_mesg(mesg="Id is lesser than 0", type="error")
            raise ValueError("Id can't be lesser or equal to 0")
    else:
        log_mesg(mesg="Id is not Int type", type="error")
        raise ValueError("Id should be a number")

def validate_for_create_cols_pdf_details(data):
    if "Columns" not in data.keys():
        log_mesg(mesg="Columns Field is Missing", type="error")
        raise ValueError("Columns Field is Missing")
    if "Id" not in data.keys():
        log_mesg(mesg="Id Field is Missing", type="error")
        raise ValueError("Id Field is Missing")
    elif data["Id"] is None or data["Id"] == "":
        log_mesg("Value for Id Field is Missing", type="error")
        raise ValueError("Value for Id Field is Missing")
    elif type(data["Id"]) is int:
        if data["Id"] <= 0:
            log_mesg(mesg="Id is lesser than 0", type="error")
            raise ValueError("Id can't be lesser or equal to 0")
    else:
        log_mesg(mesg="Id is not Int type", type="error")
        raise ValueError("Id should be a number")

def validate_for_edit_details(data):
    if "Id" not in data.keys():
        log_mesg(mesg="Id Field is Missing", type="error")
        raise ValueError("Id Field is Missing")
    elif data["Id"] is None or data["Id"] == "":
        log_mesg("Value for Id Field is Missing", type="error")
        raise ValueError("Value for Id Field is Missing")
    elif type(data["Id"]) is int:
        if data["Id"] <= 0:
            log_mesg(mesg="Id is lesser than 0", type="error")
            raise ValueError("Id can't be lesser or equal to 0")
    else:
        log_mesg(mesg="Id is not Int type", type="error")
        raise ValueError("Id should be a number")

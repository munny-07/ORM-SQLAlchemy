from distutils.errors import CompileError
import mysql.connector
import pymysql
from config import config
from src.services.logger.logger import log_mesg
import time
import datetime
import math
from flask import jsonify
from sqlalchemy import case, create_engine, exists, select, update
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()

class Sales(Base):
 
    __tablename__ = 'Sales_Order_List'
 
    Id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    Sales_Order_Number = db.Column(db.Integer)
    Sales_Order_Unit_Price = db.Column(db.String(50))
    Sales_Order_Quantity = db.Column(db.Integer)
    Sales_Order_Price = db.Column(db.String(50))
    Sales_Order_Address = db.Column(db.String(255))
    Sales_Order_Country = db.Column(db.String(100))
    Sales_Order_Warehouse = db.Column(db.String(100))

class CPN(Base):
 
    __tablename__ = 'CPN_List'
 
    Id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    CPN_Order_Number = db.Column(db.Integer)
    CPN_Order_Unit_Price = db.Column(db.String(50))
    CPN_Order_Quantity = db.Column(db.Integer)
    CPN_Order_Price = db.Column(db.String(50))
    CPN_Order_Address = db.Column(db.String(255))
    CPN_Order_Country = db.Column(db.String(100))
    CPN_Order_Warehouse = db.Column(db.String(100))

def get_conn():
    try:
        host = config["host"]
        user = config["user"]
        password = config["password"]
        database = config["database"]
        port = config["port"]

        return create_engine(
            url="mysql+pymysql://{0}:{1}@{2}/{3}".format(user, password, host, database),
            pool_size=10,  # The number of connections to keep in the pool
            max_overflow=5,  # The number of connections to allow in addition to pool_size
            pool_timeout=30,  # The number of seconds to wait for a connection before throwing an error
            pool_recycle=3600,  # The number of seconds after which a connection is automatically recycled
            pool_pre_ping=True )
    except Exception as e:
        log_mesg(mesg=str(e), type="error")
        return e

def sales_view_details(session, startpage, limit, per_page):
    try:
        pages_needed = [i for i in range(startpage, startpage+limit)]
        sales_pages = []
        for page in pages_needed:
            offset = (page - 1) * per_page
            start_time = time.time()

            results = (session.query(Sales.Id, Sales.Sales_Order_Address,Sales.Sales_Order_Country,
                                     Sales.Sales_Order_Number,Sales.Sales_Order_Price,Sales.Sales_Order_Quantity,
                                     Sales.Sales_Order_Unit_Price,Sales.Sales_Order_Warehouse) \
                         .order_by(Sales.Id.desc()) \
                         .limit(per_page) \
                         .offset(offset))\
                         .all()
                         
            for row in results:
                sales_pages.append({
                    "Id": row.Id,
                    "Sales_Order_Address": row.Sales_Order_Address,
                    "Sales_Order_Country": row.Sales_Order_Country,
                    "Sales_Order_Number": row.Sales_Order_Number,
                    "Sales_Order_Price": row.Sales_Order_Price,
                    "Sales_Order_Quantity": row.Sales_Order_Quantity,
                    "Sales_Order_Unit_Price": row.Sales_Order_Unit_Price,
                    "Sales_Order_Warehouse": row.Sales_Order_Warehouse,
                })
            print(f"Page {page} fetched.")
            print(results)
            print("Query1: ", time.time() - start_time)
            
        start_time = time.time()
        
        print("Query2: ", time.time() - start_time)
        total_records = session.query(Sales).count()
        print(total_records,per_page)
        total_pages = math.ceil(total_records/per_page)
        response_data = {"total_pages":total_pages,
                "sales_data": {"pages": sales_pages}}
        return jsonify(response_data)
    except Exception as e:
        log_mesg(mesg=str(e), type="error")
        return jsonify({
            "success": False,
            "message": "An error occurred",
            "error": str(e)
        }), 500

def cpn_view_details(session, startpage, limit, per_page):
    try:
        pages_needed = [i for i in range(startpage, startpage+limit)]
        start_time = time.time()
        cpn_pages = []
        for page in pages_needed:
            offset = (page - 1) * per_page
            start_time = time.time()
            
            results = session.query(CPN) \
                         .order_by(CPN.Id.desc()) \
                         .limit(per_page) \
                         .offset(offset) \
                         .all()
        
            for row in results:
                cpn_pages.append({
                    "Id": row.Id,
                    "CPN_Order_Address": row.CPN_Order_Address,
                    "CPN_Order_Country": row.CPN_Order_Country,
                    "CPN_Order_Number": row.CPN_Order_Number,
                    "CPN_Order_Price": row.CPN_Order_Price,
                    "CPN_Order_Quantity": row.CPN_Order_Quantity,
                    "CPN_Order_Unit_Price": row.CPN_Order_Unit_Price,
                    "CPN_Order_Warehouse": row.CPN_Order_Warehouse,
                })
            print(f"Page {page} fetched.")
            print(results)
            
            print("Query1: ", time.time() - start_time)
            
        start_time = time.time()
        
        print("Query2: ", time.time() - start_time)
        total_records = session.query(CPN).count()
        print(total_records,per_page)
        total_pages = math.ceil(total_records/per_page)
        return {"total_pages":total_pages,
                "cpn_data":{"pages": cpn_pages}}
    except Exception as e:
        log_mesg(mesg=str(e), type="error")
        return e

def sales_add_details(session, data):
    try:
        new_record = Sales(**data)
        start_time = time.time()
        
        session.add(new_record)
        session.commit()
        log_mesg(mesg="Time taken to insert into table: " + str(time.time()-start_time))
        log_mesg(mesg="Data added to the table")
        data = jsonify({
                        "success": True,
                        "message": "Details are added Successfully"
                    })
        return data
    except Exception as e:
        log_mesg(mesg=str(e), type="error")
        return e

def cpn_add_details(session, data):
    try:
        
        new_record = CPN(**data)
        start_time = time.time()
        session.add(new_record)
        session.commit()
        
        log_mesg(mesg="Time taken to insert into table: " + str(time.time()-start_time))
        log_mesg(mesg="Data added to the table")
        data = jsonify({
                        "success": True,
                        "message": "Details are added Successfully"
                    })
        return data
    except Exception as e:
        log_mesg(mesg=str(e), type="error")
        return e

def sales_edit_details(session, data):
    try:
        
        start_time = time.time()
        subquery = session.query(exists().where(Sales.Id == data["Id"])).scalar()
        
        log_mesg(mesg="Time Taken for Query1: "+ str(time.time()-start_time))
        
        if (subquery):
            start_time = time.time()
            for i,j in data.items():
                if(i!="Id"):
                    stmt = (
                        update(Sales)
                        .where(Sales.Id == data["Id"])
                        .values(
                            {i:j}
                        )
                    )
                    session.execute(stmt)
                    session.commit()
            
            log_mesg(mesg="Time taken to insert details: " + str(time.time()-start_time))
            log_mesg(mesg="Data added to the Sales_Order_List")
            data = jsonify({
                            "success": True,
                            "message": "Details are Updated Successfully"
                        })
        else:
            data = jsonify({
                            "message": "Record not found in table with given id"
                        })
        return data
    except Exception as e:
        log_mesg(mesg=str(e), type="error")
        return e

def cpn_edit_details(session, data):
    try:
        
        start_time = time.time()
        subquery = session.query(exists().where(CPN.Id == data["Id"])).scalar()
        
        log_mesg(mesg="Time Taken for Query1: "+ str(time.time()-start_time))
        
        if (subquery):
            start_time = time.time()
            for i,j in data.items():
                if(i!="Id"):
                    stmt = (
                        update(CPN)
                        .where(CPN.Id == data["Id"])
                        .values(
                            {i:j}
                        )
                    )
                    session.execute(stmt)
                    session.commit()
            
            log_mesg(mesg="Time taken to insert details: " + str(time.time()-start_time))
            log_mesg(mesg="Data added to the Sales_Order_List")
            data = jsonify({
                            "success": True,
                            "message": "Details are Updated Successfully"
                        })
        else:
            data = jsonify({
                            "message": "Record not found in table with given id"
                        })
        return data
    except Exception as e:
        log_mesg(mesg=str(e), type="error")
        return e
    
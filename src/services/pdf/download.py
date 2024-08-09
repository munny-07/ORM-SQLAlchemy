from flask import jsonify
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import exists
from src.services.database.db_service import Sales, CPN

   
def create_sales_cols_pdf(session,data):
    Id = data["Id"]
    columns = data["Columns"]
    subquery = session.query(exists().where(Sales.Id == Id)).scalar()
    pdf_file = "output.pdf"
    
    if (subquery):
        if(len(columns)==0):
            columns = ["Id","Sales_Order_Number","Sales_Order_Unit_Price",
                   "Sales_Order_Quantity","Sales_Order_Price",
                   "Sales_Order_Address","Sales_Order_Country",
                   "Sales_Order_Warehouse"]
            column_dict = {col: getattr(Sales, col) for col in columns}
            column_objects = [value for key, value in column_dict.items()]
            sales_details = session.query(*column_objects).filter(Sales.Id == Id).all()
            
            if not sales_details:
                return jsonify({"message":"Sales details not found"}), 404
            
            for sales_detail in sales_details:
                data = {key: getattr(sales_detail, key) for key in column_dict.keys()}

            # Create a canvas
            c = canvas.Canvas(pdf_file, pagesize=letter)
            
            # Set up the font
            c.setFont("Helvetica", 12)
            
            # Define starting position for text
            y_position = 750
            
            # Iterate over data and write each item as a paragraph
            for key,value in data.items():
                #label = item['label']
                #value = item['value']
                text = f"{key}: {value}"
                
                # Write the text on the canvas
                c.drawString(100, y_position, text)
                
                # Adjust y_position for the next item
                y_position -= 20  # Move down 20 units for the next line
            
            # Save the PDF file
            c.save()
            # return jsonify({"message": "PDF created successfully"}), 200
            return pdf_file,200
        
        else:
            columns.insert(0,"Id")
            column_dict = {col: getattr(Sales, col) for col in columns}
            
            column_objects = [value for key, value in column_dict.items()]
            sales_details = session.query(*column_objects).filter(Sales.Id == Id).all()
            
            if not sales_details:
                return jsonify({"message":"Sales details not found"}), 404
            
            for sales_detail in sales_details:
                data = {key: getattr(sales_detail, key) for key in column_dict.keys()}

            # Create a canvas
            c = canvas.Canvas(pdf_file, pagesize=letter)
            
            # Set up the font
            c.setFont("Helvetica", 12)
            
            # Define starting position for text
            y_position = 750
            
            # Iterate over data and write each item as a paragraph
            for key,value in data.items():
                #label = item['label']
                #value = item['value']
                text = f"{key}: {value}"
                
                # Write the text on the canvas
                c.drawString(100, y_position, text)
                
                # Adjust y_position for the next item
                y_position -= 20  # Move down 20 units for the next line
            
            # Save the PDF file
            c.save()
            # return jsonify({"message": "PDF created successfully"}), 200
            return pdf_file,200
    else:
        # return jsonify({"message": "Record not found"}), 404
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(100,750,text="{Status:Record not found}")
        c.save()
        return pdf_file, 404

def create_cpn_cols_pdf(session,data):
    Id = data["Id"]
    columns = data["Columns"]
    subquery = session.query(exists().where(CPN.Id == Id)).scalar()
    pdf_file = "output.pdf"
    
    if (subquery):
        if(len(columns)==0):
            c = ["Id","CPN_Order_Number","CPN_Order_Unit_Price","CPN_Order_Quantity","CPN_Order_Price","CPN_Order_Address","CPN_Order_Country","CPN_Order_Warehouse"]
            column_dict = {col: getattr(CPN, col) for col in c}
            column_objects = [value for key, value in column_dict.items()]
            cpn_details = session.query(*column_objects).filter(CPN.Id == Id).all()
            
            if not cpn_details:
                return jsonify({"message":"CPN details not found"}), 404
            
            for cpn_detail in cpn_details:
                data = {key: getattr(cpn_detail, key) for key in column_dict.keys()}

            # Create a canvas
            c = canvas.Canvas(pdf_file, pagesize=letter)
                    
            # Set up the font
            c.setFont("Helvetica", 12)
            
            # Define starting position for text
            y_position = 750
            
            # Iterate over data and write each item as a paragraph
            for key,value in data.items():
                #label = item['label']
                #value = item['value']
                text = f"{key}: {value}"
                
                # Write the text on the canvas
                c.drawString(100, y_position, text)
                
                # Adjust y_position for the next item
                y_position -= 20  # Move down 20 units for the next line
            
            # Save the PDF file
            c.save()
            # return jsonify({"message": "PDF created successfully"}), 200
            return pdf_file,200
    
        else:
            columns.insert(0,"Id")
            column_dict = {col: getattr(CPN, col) for col in columns}
        
            column_objects = [value for key, value in column_dict.items()]
            cpn_details = session.query(*column_objects).filter(CPN.Id == Id).all()
            
            if not cpn_details:
                return jsonify({"message":"CPN details not found"}), 404
            
            for cpn_detail in cpn_details:
                data = {key: getattr(cpn_detail, key) for key in column_dict.keys()}

            # Create a canvas
            c = canvas.Canvas(pdf_file, pagesize=letter)
                    
            # Set up the font
            c.setFont("Helvetica", 12)
            
            # Define starting position for text
            y_position = 750
            
            # Iterate over data and write each item as a paragraph
            for key,value in data.items():
                #label = item['label']
                #value = item['value']
                text = f"{key}: {value}"
                
                # Write the text on the canvas
                c.drawString(100, y_position, text)
                
                # Adjust y_position for the next item
                y_position -= 20  # Move down 20 units for the next line
            
            # Save the PDF file
            c.save()
            # return jsonify({"message": "PDF created successfully"}), 200
            return pdf_file,200
    else:
        # return jsonify({"message": "Record not found"}), 404
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(100,750,text="{Status:Record not found}")
        return pdf_file, 404

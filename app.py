from flask import Flask, jsonify, send_from_directory, request
import openpyxl
import pandas as pd

app = Flask(__name__)

def extract_links_from_excel(file_path, sheet_name, column_name):
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheet = wb[sheet_name]
    links = []
    
    col_idx = None
    for col in sheet.iter_cols(1, sheet.max_column):
        if col[0].value == column_name:
            col_idx = col[0].column
            break

    if col_idx is None:
        raise ValueError(f"Column '{column_name}' not found in sheet '{sheet_name}'")
    
    for cell in sheet.iter_cols(min_col=col_idx, max_col=col_idx, min_row=2, values_only=False):
        for c in cell:
            if c.hyperlink:
                links.append(c.hyperlink.target)

    return links

def extract_names_from_excel(file_path, sheet_name, columns):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    if not all(col in df.columns for col in columns):
        raise ValueError("One or more specified columns are missing in the Excel sheet.")
    
    combined_names = df[columns[0]].astype(str).str[:30] + " " + \
                     df[columns[1]].astype(str).str[:30] + " - " + \
                     df[columns[2]].astype(str).str[:30]
    full_names = df[columns[0]].astype(str) + " " + df[columns[1]].astype(str) + " - " + df[columns[2]].astype(str)
    
    return combined_names.tolist(), full_names.tolist()

@app.route('/playlist')
def get_playlist():
    # file_path = r'C:\Users\Tolli\Music\AMQ\Browserplayer\AMQDB.xlsx'
    file_path = './AMQDB.xlsx'
    sheet_name = request.args.get('sheet', 'GaleHail')
    column_name = 'Song Info'  # Column containing the links

    try:
        links = extract_links_from_excel(file_path, sheet_name, column_name)
        combined_names, full_names = extract_names_from_excel(file_path, sheet_name, ['Anime Name', 'Song Type', 'Song Info'])
        combined_playlist = list(zip(links, combined_names, full_names))
        return jsonify(combined_playlist)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)

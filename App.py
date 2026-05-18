from flask import Flask ,request, render_template, jsonify
from PIL import Image
import algorithm
import io
import base64
import time


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods = ['POST'])
def processing():
    file = request.files['image']
    filter_type = request.form['filter']

    img = Image.open(file.stream).convert('L')
    width , height = img.size

    img_data = list(img.getdata())

    matrix = [img_data[i * width : (i+1) * width] for i in range(height)]
    gamma = 2.0
    start_time = time.time()
    if filter_type == 'log':
        processed_matrix = algorithm.apply_log(matrix)


    elif filter_type == 'gamma':
        processed_matrix = algorithm.apply_gamma(matrix, gamma)

    
    elif filter_type == 'negative':
        processed_matrix = algorithm.apply_negative(matrix)

    elif filter_type == 'blur':
        processed_matrix = algorithm.apply_smoothing(matrix)

    elif filter_type == 'median':
        processed_matrix = algorithm.apply_median(matrix)
    elif filter_type == 'edge':
        processed_matrix = algorithm.apply_edge_detection(matrix)
    
    else:
        return jsonify({
            "success": True,
            "message": f"Applied {filter_type} filter successfully!"
        })
    end_time = time.time()
    exec_time =round(end_time - start_time, 4)

    flat_processed_data = [pixel for row in processed_matrix for pixel in row]

    processed_img = Image.new('L', (width, height))
    processed_img.putdata(flat_processed_data)


    img_io = io.BytesIO()
    processed_img.save(img_io, "PNG")
    img_io.seek(0)

    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    img_url = f"data:image/png;base64,{img_base64}"

    return jsonify({
        "success": True,
        "message": f"Applied {filter_type} filter successfully!",
        "image": img_url,
        "execution_time": exec_time,
        "complexity": "Time: O(N*M) | Space: O(N*M)"
    })
    




if __name__ == '__main__':
    app.run(debug=True)
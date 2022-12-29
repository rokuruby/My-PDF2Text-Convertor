from flask import Flask, request, render_template, send_file
import PyPDF2
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def convert_pdf():
    if request.method == 'GET':
        # Render the upload template
        return render_template('upload.html')
    else:
        # Process the uploaded PDF file
        print(request.files)
        try:
            pdf_file = request.files['pdf']
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            print(pdf_reader.getNumPages()) 
            text = ""
            for page in range(pdf_reader.getNumPages()):
                text += pdf_reader.getPage(page).extractText()

            # Save the extracted text to a file
            output_file_path = os.path.join(app.root_path, 'output.txt')
            with open(output_file_path, 'w') as f:
                f.write(text)
                print(f)

            # Render the download template
            return render_template('download.html')
        except Exception as e:
            # Render an error template
            return render_template('error.html', error=str(e))

@app.route('/download')
def download():
    # Send the output.txt file as a download
    return send_file('output.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


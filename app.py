from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask import send_from_directory
import pandas as pd
from cleansing_function import cleansing

from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

bad_words = pd.read_csv("full-list-of-bad-words_text-file_2022_05_05.txt", sep="\t", engine="python", names=["word"])
bad_words['word'] = bad_words["word"].apply(cleansing)

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def filter_words():
    if request.method == 'POST':
        user_text = request.form['text']
        input_text_df = pd.DataFrame({'Input User' : [user_text]})
        input_text_df['Input User'] = input_text_df['Input User'].apply(cleansing)
        input_text_df['Input User'] = input_text_df['Input User'].to_list()
        input_text_df['Token Text'] = input_text_df['Input User'].apply(lambda x : x.split())

        result = []
        for tokens in input_text_df['Token Text']:
            for token in tokens:
                if token in bad_words.values:
                    result.append("Sorry the word is not allowed")
                    break
                else:
                    continue
            result.append("Thank you for being polite")
        return jsonify(result[0])
    
    return render_template("input_text.html")

## SWAGGER UI ##

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info={
        'title': LazyString(lambda: "API Documentation for Word Filtering"),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: "API made using Flask"),
    },
    host=LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)


@swag_from("./templates/word_filters.yaml", methods=['POST'])
@app.route("/filter_bad_words", methods=["POST"])
def filter_words_swgr():
    if request.method == 'POST':
        user_text = request.form['text']
        input_text_df = pd.DataFrame({'Input User' : [user_text]})
        input_text_df['Input User'] = input_text_df['Input User'].apply(cleansing)
        input_text_df['Input User'] = input_text_df['Input User'].to_list()
        input_text_df['Token Text'] = input_text_df['Input User'].apply(lambda x : x.split())

        result = []
        for tokens in input_text_df['Token Text']:
            for token in tokens:
                if token in bad_words.values:
                    result.append("Sorry the word is not allowed")
                    break
                else:
                    continue
            result.append("Thank you for being polite")
        return jsonify(result[0])

if __name__ == '__main__':
    app.run(debug=True)


        
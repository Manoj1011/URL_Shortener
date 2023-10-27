from flask import Flask, render_template, request, jsonify
import shortuuid

app = Flask(__name__)
url_mapping = {}
titles = {} 

@app.route('/shorten', methods=['POST'])
def shorten_url():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        if 'url' in data and 'title' in data:
            long_url = data['url']
            title = data['title']
            short_url = generate_short_url()
            url_mapping[short_url] = long_url
            titles[long_url] = title
            return jsonify({'short_url': short_url}), 201
        else:
            return jsonify({'error': 'Missing "url" or "title" parameter'}), 400
    else:
        return "Content type is not supported."

@app.route('/search/<term>', methods=['GET'])
def search_urls(term):
    matching_urls = []
    for long_url, title in titles.items():
        if title.count(term) > 0:
            short_url = next((k for k, v in url_mapping.items() if v == long_url), None)
            matching_urls.append({'title': title, 'url': long_url, 'short_url': short_url})
    return jsonify(matching_urls=matching_urls), 200

def generate_short_url():
    return shortuuid.ShortUUID().random(length=7)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', results=[])

# if __name__ == '__main__':
#     app.run()

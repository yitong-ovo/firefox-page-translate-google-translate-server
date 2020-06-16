# 先用几天看看有没有 bug。
from flask import Flask, request, jsonify
from googletrans import Translator
app = Flask(__name__)
translator = Translator(
    service_urls=[
        # 'translate.google.cn', # CN 域是不行的
        'translate.google.com',
    ],
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:77.0) Gecko/20100101 Firefox/77.0',
    # proxies={
    #     'http': '127.0.0.1:1087' # 代理我设置了是没用的，可以使用 proxychains 来运行。
    # }
)

# 统计，不需要的话可以关掉。
enable_statistics = True
statistics_count = {
    "query_character": 0,
    "translated_character": 0,
    "request_count": 0,
}


def statistics(srcQuery, translations):
    if not enable_statistics:
        return
    statistics_count['request_count'] = statistics_count['request_count'] + 1
    for query_text in srcQuery:
        statistics_count['query_character'] = statistics_count['query_character'] + len(str(query_text))
    for translation in translations:
        statistics_count['translated_character'] = statistics_count['translated_character'] + len(str(translation.text))
    print(f"\n==== statistocs ====\n{str(statistics_count)}\nAverage characters per request: {str((statistics_count['query_character'] / statistics_count['request_count']))}\n")

@app.route('/api/translate', methods=['GET', 'POST'])
def get_data():
    translationResultList = []
    try:
        print(f'==== HEADER: ==== \n{request.headers}')
        sourceLANG = request.form.get('source')
        targetLANG = request.form.get('target')
        allQuery = request.form.getlist('q')

        print(f"sourceLANG: {sourceLANG}")
        print(f"targetLANG: {targetLANG}")
        print(f"all query: {allQuery}")

        # firefox 会把目标的中文提交为 'zh' 但这个库没法处理。替换一下。
        if targetLANG == 'zh':
            targetLANG = 'zh-cn'

        translations = translator.translate(
            allQuery, src=sourceLANG, dest=targetLANG)
        translationResultList = [
            {"translatedText": translation.text} for translation in translations]

        statistics(allQuery, translations)

    except Exception as e:
        print(e)

    return jsonify(
        {
            "data": {
                "translations": translationResultList
            }
        }
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

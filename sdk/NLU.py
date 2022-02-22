import requests,json



class NLU:
    def __init__(self):
        self.host = 'https://static.bosonnlp.com'
        
    def sentiment(self,text):
        data = {'data': text}
        response = requests.post(url = f'{self.host}/analysis/sentiment?analysisType=', data = data)
        json_obj = json.loads(response.text)
        return {'data':float(round(json_obj[0][0], 2)*100)}
    
    def wordsAnalysis(self,text):
        data = {'data': text}
        response = requests.post(url = f'{self.host}/analysis/tag', data = data)
        json_obj = json.loads(response.text)[0]
        res = dict(zip(json_obj['word'],json_obj['tag']))
        verb_index = 0
        noun_index = 0
        cmd = {}
        for word in res:
            if res[word] == 'v':
                cmd[str(verb_index)+'v'] = word
                verb_index += 1
            elif res[word] == 'n':
                cmd[str(noun_index)+'n'] = word
                noun_index += 1
        return {'data':cmd}
    
nlu = NLU()
if __name__ == '__main__':
    nlu_res = nlu.wordsAnalysis('打开电视关闭')['data']
    nlu_res_len = len(nlu_res)
    if 1 == nlu_res_len%2:
        nlu_res.popitem()
    res = ''.join([nlu_res[x] for x in nlu_res])
    print(res)

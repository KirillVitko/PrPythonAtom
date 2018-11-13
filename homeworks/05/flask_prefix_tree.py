from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

class PrefixTree:
    #TODO реализация класса prefix tree, методы как на лекции + метод дать топ 10 продолжений. Скажем на строку кросс выдаем кроссовки, кроссовочки итп. Как хранить топ? 
    #Решать вам. Можно, конечно, обходить все ноды, но это долго. Дешевле чуток проиграть по памяти, зато отдавать быстро (скажем можно взять кучу)
    #В терминальных (конечных) нодах может лежать json с топ актерами.
    
    def __init__(self):
        self.root = [{}]
        
    def add(self, string, rating, json):
        if self.check(string):
            return
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                wrk_dict[0][i] = [{}]
                wrk_dict = wrk_dict[0][i]
                wrk_dict.append({1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], "min": 0})
        wrk_dict.append(rating)
        wrk_dict.append(json)
        self.recount(string, rating, json)
        
    def check(self, string):
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                return False
        if len(wrk_dict) == 4:
            return True
        return False
    
    def check_part(self, string):
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                return False
        return True
        
    def sort(self,wrk,p):
        k = 1
        while k == 1:
            k = 0
            for i in range(9):
                if wrk[0][p][1][i+1] < wrk[0][p][1][i+2]:
                    wrk[0][p][1][i+1], wrk[0][p][1][i+2] = wrk[0][p][1][i+2], wrk[0][p][1][i+1]
                    k = 1
        return wrk
        
    def recount(self, string, rating, json):
        wrk_dict = self.root
        for i in string:
            if wrk_dict[0][i][1][10] == []:
                for j in range(10):
                    if wrk_dict[0][i][1][j+1] == []:
                        wrk_dict[0][i][1][j+1].append(rating)
                        wrk_dict[0][i][1][j+1].append(string)
                        wrk_dict[0][i][1][j+1].append(json)
                        wrk_dict = self.sort(wrk_dict, i)
                        wrk_dict[0][i][1]["min"] = wrk_dict[0][i][1][j+1][0]
                        break
            elif rating <= wrk_dict[0][i][1]["min"]:
                wrk_dict = wrk_dict[0][i]
                continue
            else:
                for j in range(10):
                    if wrk_dict[0][i][1][j+1][0] == wrk_dict[0][i][1]["min"]:
                        wrk_dict[0][i][1][j+1][0] = rating
                        wrk_dict[0][i][1][j+1][1] = string
                        wrk_dict[0][i][1][j+1][2] = json
                        wrk_dict = self.sort(wrk_dict, i)
                        wrk_dict[0][i][1]["min"] = wrk_dict[0][i][1][10][0]
                        break
            wrk_dict = wrk_dict[0][i]
            
    def tops(self,string):
        if self.check_part(string) == False:
            return "в базе нет подходящих слов"
        wrk_dict = self.root
        for i in string:
            wrk_dict = wrk_dict[0][i]
        result = []
        for i in range(10):
            if wrk_dict[1][i+1] != []:
                result.append(wrk_dict[1][i+1])
        return result
    
def init_prefix_tree(filename):
    #TODO в данном методе загружаем данные из файла. Предположим вормат файла "Строка, чтобы положить в дерево" \t "json значение для ноды" \t частота встречаемости
    df = pd.read_csv(filename)
    PrefixTree = prefix_tree()
    for i in df.iterrows():
        PrefixTree.add(i[1]["title"], i[1]["raiting"], i[1]["json"])
    return PrefixTree

p_t = init_prefix_tree('Exampleoffile.csv')

@app.route("/get_sudgest/<string>", methods=['GET', 'POST'])
def return_sudgest(string):
    #TODO по запросу string вернуть json, c топ-10 саджестами, и значениями из нод
    sudgest = p_t.tops(string)
    t_sudgest = {}
    for i in sudgest:
        st = "рейтинг=" + str(i[0]) + "; json=" + str(i[2])
        t_sudgest[i[1]] = st
    return t_sudgest

@app.route("/")
def hello():
    #TODO должна возвращатьс инструкция по работе с сервером
    print("Hi)")
    return

if __name__ == "__main__":
    app.run()
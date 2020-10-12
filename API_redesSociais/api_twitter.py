import tweepy
import numpy as np
import pandas as pd 
from datetime import date
import utils


  


def login_api():

    consumer_key = 'NtXvTwTigLmN5heto1m2leNON'
    consumer_secret = 'aK1pW7BbWPzljGlUIV8M7Ybap9banhXBZ5cigGpkaMwYrufqNi'
    access_token = '198314809-yu0eym1WTSmKSEFQL6udvWFPbRjQaLtRoH6zGIcL'
    access_token_secret = 'xb5JCOJ4EIEFOUNqZ5iSXDomqkQZwJ7zefUn4xBTFUYO0'   


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    return api 



def obter_twitters(api, qtd_twittes, strings_busca, data):
    """
    qtd_twittes: qtd máxima de twittes por busca
    strings_busca: palavras a serem pesquisada nos twitters
    data: data de inicio da busca no formato: "ano-mes-dia"

    """
    

    dados = []
    i = 0
    for string_busca in strings_busca:

      
      for tweet in tweepy.Cursor(api.search,q=string_busca, count=280, since=data, tweet_mode='extended', lang='pt-br').items():
          
          texto = tweet.full_text
          nome = tweet.author.name
          conta = tweet.author.screen_name
          cod_user = tweet.author.id
          palavra_chave = string_busca
          
          
          dados.append([cod_user, nome, conta, texto, palavra_chave])
          if i == qtd_twittes:
              break
          else:
              i = i+1
    
    return dados 


def validar_texto(twitter):
    palavras= utils.palavras_censuradas()
    return any(item in palavras for item in twitter) 


def selecionar_twitter(palavras_chaves, local):
    data = date.today()
    qtd_twittes = 200
    api = login_api()
    twitters = obter_twitters(api, qtd_twittes, palavras_chaves, data)

    if len(twitters) < 1:
        return list(), list()

    dados_twitter = pd.DataFrame(twitters, columns=['ID', 'Nome', 'Conta', 'Texto', 'palavra_chave'])

    twitters_selected = []
    users_selected = []
    id_selected = []
    
    i = 0
    while(i < 5):
        select = np.random.randint(0, len(dados_twitter))
        
        if select not in id_selected:
            id_selected.append(select)
            twitter_selected = dados_twitter['Texto'][select].decode("utf-8")
            user_selected =  dados_twitter['Conta'][select]
            

            texto_invalido = validar_texto(twitter_selected.split(" "))

            if texto_invalido == False:
                twitters_selected.append(twitter_selected)
                users_selected.append(user_selected)
                i+=1
    

    return twitters_selected, users_selected



if __name__ == "__main__":
    palavras = ['comida', 'bolo']
    twt_selected,  user_selected = selecionar_twitter(palavras, 'null')
    print(twt_selected)
    print(user_selected)
    
    







  


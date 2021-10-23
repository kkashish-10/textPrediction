from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings

from tensorflow.keras.models import load_model
model=load_model("Model\model.h5")

#libraries for initialization_routine
import numpy
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

raw_data=open(r"main\wonderland.txt",encoding='utf-8').read()
raw_data=raw_data.lower().split('\n')
    
kToken=Tokenizer()
kToken.fit_on_texts(raw_data)
vocab_size=len(kToken.word_index)+1
inp_seq=[]
for line in raw_data:
    token_list=kToken.texts_to_sequences([line])[0]
    for i in range(1,len(token_list)):
        inp_seq.append(token_list[:i+1])
    
max_seq_len=max([len(x) for x in inp_seq])
inp_seq=numpy.array(pad_sequences(inp_seq,maxlen=max_seq_len,padding='pre'))
predictors,labels=inp_seq[:,:-1],inp_seq[:,-1]
labels=to_categorical(labels,num_classes=vocab_size)

    
   

def home(request):
    return render(request,'home.html')


#def textbox(request):
  # return render(request, 'home.html')


# rework this function here

def generate_text(seed_text, next_words, model, max_sequence_len):
    for _ in range(next_words):
        token_list=kToken.texts_to_sequences([seed_text])[0]
        print('token_list ',token_list[:10])
        token_list=pad_sequences([token_list],maxlen=max_sequence_len-1,padding='pre')
        predicted=model.predict(token_list,verbose=1)
        prediction=numpy.argmax(predicted,axis=1)
        output_word=""
        for word,index in kToken.word_index.items():
            if(numpy.any(index==prediction)):
                output_word=word
                break
        seed_text+=" "+output_word
        print(seed_text)
    return seed_text

def generate(request):
    text=request.GET.get('id_content')
    print('seed text=',text)
    output= generate_text(text, 10, model,max_seq_len)
    print('output text',output)
    return JsonResponse({'result': output})
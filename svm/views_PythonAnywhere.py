from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from .forms import SeqForm

import os, sys

sys.path.append('./AMPSVM/code')
import descripGen_12, predictSVC


def seq(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SeqForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            seq = form.cleaned_data['seq']
            if seq is not None:
                f = open('seqs.txt', 'w+')
                f.write('     1 ')
                f.write(seq)
                f.close()
            # redirect to a new URL:
            if len(seq) >= 8 and len(seq) <= 100:
                return redirect('/result/')
            else:
                return redirect('/fail/')
                
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SeqForm()

    return render(request, 'svm/seq.html', {'form': form})

def result(request):
    
    os.chdir('./AMPSVM/code')
    
    descripGen_12.main('./aaindex','../../seqs.txt',1,1)
    predictSVC.main('descriptors.csv','Z_score_mean_std__intersect_noflip.csv','svc.pkl')
    
    with open('descriptors_PREDICTIONS.csv','r') as fin:
        line = fin.readline()
        headers = line.strip().split(',')
        line = fin.readline()
        data = line.strip().split(',')
        seqIndex = data[0]
        prediction = data[1]
        distToMargin = data[2]
        P_neg1 = data[3]
        P_plus1 = data[4]
        
    os.chdir('../..')
    
    distToMargin = '%6.2f' % (float(distToMargin))
    P_neg1 = '%6.2f' % (float(P_neg1))
    P_plus1 = '%6.2f' % (float(P_plus1))
    
    return render(request, 'svm/result.html', {'seqIndex' : seqIndex, 'prediction' : prediction, 'distToMargin' : distToMargin, 'P_neg1' : P_neg1, 'P_plus1' : P_plus1})

def fail(request):
    
    return render(request, 'svm/fail.html')
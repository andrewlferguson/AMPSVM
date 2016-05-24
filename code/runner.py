import descripGen_12, predictSVC

descripGen_12.main('./aaindex','seqs.txt',1,1)
predictSVC.main('descriptors.csv','Z_score_mean_std__intersect_noflip.csv','svc.pkl')
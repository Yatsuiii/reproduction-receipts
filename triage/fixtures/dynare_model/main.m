modelName = 'nk';
dynare nk noclearall
modelResult = load([modelName, '_results.mat']);
plot(modelResult.oo_.irfs.y_e);

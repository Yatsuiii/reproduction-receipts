dynare optpol noclearall
load result.mat;
rates = oo_.irfs;
save('rates', 'rates');

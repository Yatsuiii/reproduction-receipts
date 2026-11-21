var y pi;
varexo e;
model;
y = y(+1) - pi(+1) + e;
pi = 0.99*pi(+1) + 0.1*y;
end;
stoch_simul(order=1);
resultFileName = 'result.mat';
save(resultFileName, 'oo_');

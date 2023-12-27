function DrawActivationFuncs()
% matlab/octave function to draw 3 activation functions and their derivatives
% sigmoid, tanh, and relu
% Daniel Zhang
% Dec 2023
%

s = 0.001;
x = -5:s:5;
x = [x(1)-s,x,x(end)+s];


sx = sig(x);
dsx = (sx(2:end)-sx(1:end-1))/s;
sx = sx(2:end-1);
dsx = dsx(2:end);

tx = tax(x);
dtx = (tx(2:end)-tx(1:end-1))/s;
tx = tx(2:end-1);
dtx = dtx(2:end);

rx = relu(x);
drx = (rx(2:end)-rx(1:end-1))/s;
rx = rx(2:end-1);
drx = drx(2:end);

lx = lelu(x);
dlx = (lx(2:end)-lx(1:end-1))/s;
lx = lx(2:end-1);
dlx = dlx(2:end);

ex = elu(x);
dex = (ex(2:end)-ex(1:end-1))/s;
ex = ex(2:end-1);
dex = dex(2:end);


x = x(2:end-1);

% plot 
close all;

figure,hold on;
grid minor;

plot(x,sx,'r-','LineWidth',3);
plot(x,tx,'b-','LineWidth',3);
plot(x,rx,'g-','LineWidth',3);
plot(x,lx,'k-','LineWidth',3);
plot(x,ex,'m-','LineWidth',3);

title('Activation Functions');
ylim([-2,2]);
legend('S(sigmoid)','T(tanh)','R(ReLU)','L(LeakyReLU)','E(Exponential LU)','Location','northwest');

figure,hold on;
grid minor;

plot(x,dsx,'r-.','LineWidth',3);
plot(x,dtx,'b-.','LineWidth',3);
plot(x,drx,'g-.','LineWidth',3);
plot(x,dlx,'k-','LineWidth',3);
plot(x,dex,'m-','LineWidth',3);

title('Derivatives of Activation Functions');
ylim([-1.1,1.1]);
legend('S''','T''','R''','L''','E''','Location','northwest');

end

function out = sig(x)
out = 1./(1 + exp(-x));
end

function out = tax(x)
out = tanh(x);
end

function out = relu(x)
out = x;
out(out<0) = 0;
end

function out = lelu(x)
a = 0.01;
out = x;
out(out<0) = a*out(out<0);
end

function out = elu(x)
alpha = 1;
out = x;
out(out<0) = alpha*(exp(out(out<0))-1);
end


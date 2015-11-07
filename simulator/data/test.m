close all;
clc
clear
% load 'data.mat'
% figure()
% plot(probe_loss_set, probe_rel_err, '-r')
% hold on
% plot(distance_loss_set, distance_rel_err, '-b')
D = 9;
m = 25;
R = 100;
lambda = 0.1;
N = 2018;
tau1 = 10:40;
tau2 = tau1 + 5;
P = 0:0.1:0.9;

phi1_1 = (P' * ((tau1 - D) .* exp(-lambda * (tau1 - D))) + (1-P)' * ((tau1 - D-m) .* exp(-lambda * (tau1 - m - D)))) * lambda ^ 2;
phi1_2 = (1 - P)' * lambda^2 * ((tau1 - D - m).*exp(-lambda * (tau1 - D -m)));

phi2_1 = (P' * ((tau2 - D) .* exp(-lambda * (tau2 - D))) + (1-P)' * ((tau2 - D-m) .* exp(-lambda * (tau2 - m - D)))) * lambda ^ 2;
phi2_2 = (1 - P)' * lambda^2 * ((tau2 - D - m).*exp(-lambda * (tau2 - D -m)));

PF1 = lambda * P' * ((tau1 - D + 1/lambda) .* exp(-lambda * (tau1 - D))) + lambda * (1-P)' * ((tau1 - D - m + 1/lambda) .* exp(-lambda * (tau1 - m - D)));
PF2 = lambda * P' * ((tau2 - D + 1/lambda) .* exp(-lambda * (tau2 - D))) + lambda * (1-P)' * ((tau2 - D - m + 1/lambda) .* exp(-lambda * (tau2 - m - D)));


coeff1 = N ./ (1 - PF1) ./ PF1;
coeff2 = N ./ (1 - PF2) ./ PF2;

J_11 = coeff1 .* phi1_1 .* phi1_1 + coeff2 .* phi2_1 .* phi2_1;
J_22 = coeff1 .* phi1_2 .* phi1_2 + coeff2 .* phi2_2 .* phi2_2;
J_21 = coeff1 .* phi1_2 .* phi1_1 + coeff2 .* phi2_2 .* phi2_1;
J_12 = J_21;

[p_num, tau_num] = size(J_11);

CRB = ones(p_num, tau_num);

for i = 1: p_num
    for j = 1:tau_num
        J = [J_11(i, j), J_12(i, j); J_21(i, j), J_22(i, j)];
        tmp = inv(J);
        CRB(i, j) = tmp(1, 1);
    end
end
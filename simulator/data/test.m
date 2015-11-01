close all;
clc
load 'data.mat'
figure()
plot(probe_loss_set, probe_rel_err, '-r')
hold on
plot(distance_loss_set, distance_rel_err, '-b')
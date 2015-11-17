clear;
close all;
clc;

load 'data.mat';
plot(distance_loss_set, distance_rel_err);
hold on;
plot(probe_loss_set, probe_rel_err);
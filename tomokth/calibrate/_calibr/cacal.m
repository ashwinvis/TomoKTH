function [par,pos,iter,res,er,C]=cacal(name,data1,data2,data3,data4,data5,data6)
%CACAL Calibration routine for computing the camera parameters. The
%initial values are solved by using the DLT method and the final parameter
%values are obtained iteratively.      
%
%Usage:
%   [par,pos,iter,res,er,C]=cacal(name,data1,data2,data3,data4,data5,data6)
%
%where
%   name = string that is specific to the camera and the framegrabber.
%          This string must be defined in configc.m
%   data1...data6 = matrices that contain the 3-D coordinates of the
%          control points (in fixed right-handed frame), corresponding
%          image observations (in image frame, origo in the upper left
%          corner), and normal vectors of the object surface. 
%          dimensions: (n x 8) matrices, row format: [wx wy wz ix iy nx ny nz],
%          units: mm for control points, pixels for image points,
%          min. number of images = 1 (requires 3-D control point structure)
%          max. number of images = 6
%   par  = camera intrinsic parameters
%   pos  = camera position and orientation for each image (n x 6 matrix)
%   iter = number of iterations used
%   res  = residual (sum of squared errors)
%   er   = remaining error for each point
%   C    = error covariance matrix of the estimated parameters

%   Version 3.0  10-17-00
%   Janne Heikkila, University of Oulu, Finland

num=nargin-1;
if ~isstr(name)
  error('The first argument should be the camera type');
end
sys=configc(name);

data=[]; obs=[]; sdata=[]; snorm=[]; ipos=[]; tic;

f0=sys(5); u0=sys(1)/2; v0=sys(2)/2; s0=1;
for i=1:num
  dt=eval(['data' num2str(i)]);
  if size(dt,2)~=8
    error('Data matrix should contain the surface normal');
  end
  data=[data;dt(:,1:3)]; obs=[obs;dt(:,4:5)]; snorm=[snorm;dt(:,6:8)];
  sdata=[sdata;size(dt,1)];
  ip=extinit(sys,dt(:,1:5));
  ipos=[ipos ip(:)];
end

nbr=sdata'; n=sum(sdata);
iparam=[s0 f0 u0 v0 0 0 0 0 ipos(:)'];
Bs=cinit(sys,data,snorm);
[param,iter,res,er,J,success]=lmoptc(sys,Bs,obs,nbr,iparam,1);
C=full(inv(J'*J))*var(er);
par=param(1:8);
pos=reshape(param(9:length(param)),6,num);
if success
  disp('Calibration was successfully completed. Here are the results:');
  disp(sprintf('\nCamera parameters (%s):',sys(10:length(sys))));
  disp('==================');
  disp(sprintf('Scale factor: %.4f   Effective focal length: %.4f mm',...
  par(1),par(2)));
  disp(sprintf('Principal point: (%.4f,%.4f)',par(3),par(4)));
  disp(sprintf('Radial distortion:     K1 = %e  K2 = %e',par(5),par(6)));
  disp(sprintf('Tangential distortion: T1 = %e  T2 = %e',par(7),par(8)));
  disp(sprintf('\nOther information:'));
  disp('==================');
  disp(sprintf('Standard error in pixels: %f',std(er(:))));
  disp(sprintf('Standard deviation of the estimated intrinsic parameters:'));
  disp(sprintf('%.2e ',sqrt(diag(C(1:8,1:8))')));
  disp(sprintf('Number of iterations: %d',iter));
  disp(sprintf('Elapsed time: %.1f sec.',toc));
else
  disp('Sorry, calibration failed');
end

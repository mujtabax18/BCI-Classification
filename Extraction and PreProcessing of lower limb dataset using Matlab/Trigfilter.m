function [dsdata] = Trigfilter(data,filterOrder,filterType,fs)
% HP and LP Filtering
% 2nd order (0.05-5Hz)
order   = filterOrder;
[bb,aa] = butter(order,100*2/fs,filterType);  % Calculate high pass filter coefficients
dsdata = filtfilt(bb,aa,data);
function [dsdata] = BPfilter(data,filterOrder,epochType,fs)
%fs      = fs;                             % Sampling frequency
% HP and LP Filtering
order   = filterOrder;
switch epochType
    case 0
        [b, a]  = butter(order,30*2/fs,'low');      % Calculate low pass filter coefficients - Feature extraction
    otherwise
        [b, a]  = butter(order,10*2/fs,'low');      % Calculate low pass filter coefficients - Morphology analysis
end
[bb,aa] = butter(order,0.1*2/fs,'high');  % Calculate high pass filter coefficients

% Perform filtering twice to obtain a fourth order filter
dsdata  = zeros(size(data));               % Preallocate matrix
for w = 1:size(data,1)                     % Start filtering
    dsdata(w,:) = filtfilt(b,a,data(w,:));
    dsdata(w,:) = filtfilt(b,a,dsdata(w,:));
    dsdata(w,:) = filtfilt(bb,aa,dsdata(w,:));
    dsdata(w,:) = filtfilt(bb,aa,dsdata(w,:));
end

end
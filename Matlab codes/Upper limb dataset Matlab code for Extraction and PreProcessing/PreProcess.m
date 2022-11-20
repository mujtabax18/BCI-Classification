function [dsdata] = PreProcess(data)
fs      = 512;                             % Sampling frequency
% HP and LP Filtering
% 2nd order (0.05-45Hz)
order   = 4;
[b, a]  = butter(order,5*2/fs,'low');     % Calculate low pass filter coefficients
[bb,aa] = butter(order,0.05*2/fs,'high');  % Calculate high pass filter coefficients

% Notch Filter                
Wn      = [49 51]/fs*2;                    % Cutoff frequencies
[bn,an] = butter(order,Wn,'stop');         % Calculate filter coefficients
dsdata  = zeros(size(data));               % Preallocate matrix
for w = 1:size(data,1)                     % Start filtering
    dsdata(w,:) = filtfilt(bn,an,data(w,:));
    dsdata(w,:) = filtfilt(b,a,dsdata(w,:));
    dsdata(w,:) = filtfilt(bb,aa,dsdata(w,:));    
end

end

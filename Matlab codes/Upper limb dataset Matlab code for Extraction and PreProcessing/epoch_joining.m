function [epoch] = epoch_joining(ch1,ch2,ch3)
    epoch={};
    hit=min([height(ch1) height(ch2) height(ch3)]);
    for mo=1:hit
        epoch{mo}=[ch1(mo,:);ch2(mo,:);ch3(mo,:)];
    end
end
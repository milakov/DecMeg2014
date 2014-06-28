data= load('../additional_files/NeuroMagSensorsDeviceSpace.mat');
    position = data.pos;
    orientation = data.ori;
    label = data.lab;
    sensor_type = data.typ;

    %Normalize orientation for visualization purpose:
    total=orientation.*orientation;
    orientation = orientation ./ repmat(sqrt(sum(total,2)),1,3);
    position_rearranged = reshape(position', 9, [])';
    orientation_rearranged = reshape(orientation', 9, [])';
    quiver3(position_rearranged(:,1), position_rearranged(:,2), position_rearranged(:,3), orientation_rearranged(:,1), orientation_rearranged(:,2), orientation_rearranged(:,3), 'color', [1,0,0]);
    hold on
    quiver3(position_rearranged(:,4), position_rearranged(:,5), position_rearranged(:,6), orientation_rearranged(:,4), orientation_rearranged(:,5), orientation_rearranged(:,6), 'color', [0,1,0]);
    hold on
    quiver3(position_rearranged(:,7), position_rearranged(:,8), position_rearranged(:,9), orientation_rearranged(:,7), orientation_rearranged(:,8), orientation_rearranged(:,9), 'color', [0,0,1]);
    hold on
    

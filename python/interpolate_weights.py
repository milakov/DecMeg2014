import numpy as np
from matplotlib import mlab

if __name__ == '__main__':

    image_width = 25
    image_height = 25
    output_image_border = 0.1
    layout_filename = '../additional_files/Vectorview-all.lout'
    interpolation_filename = '../additional_files/interpolation_weights.txt'

    print "Loading channel IDs and locations ..."
    channel_info = np.loadtxt(layout_filename, skiprows=1, usecols=(0, 1, 2), delimiter='\t')
    channel_info.shape = (-1, 9)

    channel_info = np.column_stack((np.floor(channel_info[:,0] / 10), (channel_info[:,1] + channel_info[:,4] + channel_info[:,7]) / 3, (channel_info[:,2] + channel_info[:,5] + channel_info[:,8]) / 3))

    # Normalize coordinate system
    def normalize(data):
    	data_min = data.min();
    	data_max = data.max();
        data_min_adjusted = data_min - (data_max - data_min) * output_image_border
        data_max_adjusted = data_max + (data_max - data_min) * output_image_border
        return (data - data_min_adjusted) / (data_max_adjusted - data_min_adjusted)

    channel_info[:,1] = normalize(channel_info[:,1])
    channel_info[:,2] = normalize(channel_info[:,2])

    channel_info = np.vstack((channel_info, [[-1, -0.001, -0.001], [-1, -0.001, 1.001], [-1, 1.001, -0.001], [-1, 1.001, 1.001]]))

    xi = np.linspace(0, 1, image_width)
    yi = np.linspace(0, 1, image_height)
    xi, yi = np.meshgrid(xi, yi)

    z = np.zeros((channel_info.shape[0]))

    print "Generating weights ..."
    total_weight_sum = 0
    with open(interpolation_filename, 'w') as the_file:
        the_file.write('sensor_id\tx\ty\tweight\n')
        for x in range(z.shape[0]):
            z[x] = 1.0
            # Interpolate using delaunay triangulation
            zi = mlab.griddata(channel_info[:,1], channel_info[:,2], z, xi, yi)
            nz = np.nonzero(zi)
            for t in range(0,len(nz[0])):
                the_file.write("%d\t%d\t%d\t%f\n" % (int(channel_info[x,0]), nz[1][t], nz[0][t], zi[nz[0][t], nz[1][t]]))
                total_weight_sum = total_weight_sum + zi[nz[0][t], nz[1][t]]
            z[x] = 0.0
    print "total_weight_sum per elem = %f" % (total_weight_sum / (image_width * image_height))
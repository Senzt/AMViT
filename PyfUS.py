# -*- coding: utf-8 -*-
"""

@author: Senzt
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from ipywidgets import interact, widgets

class io:
    
    def read_doppler(self, file_patch):
        
        ####################################
        
        self.mat = sio.loadmat(file_patch)
        
        sorted(self.mat.keys()) 
        #print(self.mat.keys())
        # Fix this
        self.data = self.mat['b0']        
        
        ####################################
        
        self.bloodflow = []        
        calibration_factor = 0.01        
        
        for t in range(self.data.shape[2]):
        
            # Select the image at time t
            image_t = self.data[:, :, t]
        
            # Extract the ROI from the image
            #roi = image_t[roi_top:roi_bottom, roi_left:roi_right]
            roi = image_t
        
            # Compute the mean pixel intensity in the ROI
            mean_intensity = np.mean(roi)
        
            # Convert the mean pixel intensity to blood flow using the calibration factor
            flow = mean_intensity * calibration_factor
        
            # Append the calculated blood flow to the list
            self.bloodflow.append(flow)
            
        self.bloodflow = np.array(self.bloodflow)
        
        ##################################

        print("Loading successful.")
        
    def plot_bloodflow(self):
        # Plot the blood flow over time
        plt.plot(self.bloodflow)
        plt.xlabel('Time point')
        plt.ylabel('Blood flow')
        plt.show()
        
        ##################################
        
    def plot_s(self):
        
        n = self.data.shape[2]  # the number of subplots

        fig, axs = plt.subplots(nrows=n, ncols=1, figsize=(15,100))
        
        for i in range(n):
            axs[i].imshow(self.data[:,:,i])
            axs[i].set_title('the blood flow')
        
        plt.show()
        
        
    def browse_images(self):
        n = self.data.shape[2]
        def view_image(i):
            plt.imshow(self.data[:,:,i], interpolation='nearest')
            plt.title(f'Time step: {i}')
            plt.show()
        interact(view_image, i=(0,n-1))

        
def epochs(PD, start, stop):
    print("epoch test")
    
    # Assuming PD.bloodflow is your y-values
    y = PD.bloodflow
    
    # Generate x-values, from 0 to the length of y
    x = np.arange(len(y))
    
    fig, ax = plt.subplots()
    
    ax.plot(x, y)
    ax.fill_between(x, y, where=(y > start) & (y < stop), color='gray', alpha=0.5)
    ax.axvline(x=start, color='r', linestyle='--')
    ax.axvline(x=stop, color='r', linestyle='--')

    plt.xlabel('Time point')
    plt.ylabel('Blood flow')
    plt.show()
    
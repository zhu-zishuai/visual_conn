# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 09:51:32 2021

@author: zzs

email: zzs.zhu@foxmail.com

"""

def visual_conn(conn_pos, conn_neg, title = 'visual_conn'):
    import pandas as pd
    import numpy as np
    from bokeh.plotting import figure, show
    from bokeh.models import Range1d
    from bokeh.core.properties import value
    from bokeh.io import export_png
    from bokeh.io.export import get_screenshot_as_png
    
    # read node order
    node_info = pd.read_excel('AAL_info.xlsx', 'my_node_order')
    node_l = np.array(node_info['L-order'])
    node_r = np.array(node_info['R-order'])
    node_all = np.concatenate([node_l, node_r], axis = 0)
        
    node_name = pd.read_excel('AAL_info.xlsx', 'aal_order')
    node_name = node_name['name']
    parcel_name = ['Prefrontal', 'MotorStrip', 'Insula', 'Parietal','Temporal',
                   'Occipital', 'Limbic', 'Cerebellum', 'Subcortical']
    parcel_color = ['red', 'orange', 'yellow', 'green', 'blue', 
                    'purple', 'cyan', 'brown', 'gray']

    parcel_end = [10, 13, 14, 21, 28, 34, 40, 53, 57]
    parcel_end1 = [x+1 for x in parcel_end]
    num_nodes = 116
    
    # coordinates of nodes from left hemisphere
    theta_left = np.linspace(np.pi/2, np.pi*3/2, num_nodes//2)
    x_left = np.cos(theta_left) - 0.05
    y_left = np.sin(theta_left)
    
    # coordinates of nodes from right hemisphere
    theta_right = np.linspace(np.pi/2, -np.pi/2, num_nodes//2)
    x_right = np.cos(theta_right) + 0.05
    y_right = np.sin(theta_right)

    # concat theta, x and y of both hemispheres
    theta_all = np.concatenate([theta_left, theta_right], axis = 0)
    x_all = np.concatenate([x_left, x_right], axis = 0)
    y_all = np.concatenate([y_left, y_right], axis = 0)
    

    # create plot
    tools = 'pan,box_zoom,wheel_zoom,tap,save,reset,help'
    p = figure(tools = tools) #, height = 1200, width = 1200
    p.text(x = [0], y = [1.3], text = [title], 
           text_align='center', text_baseline = 'middle', # align is horizontal, baseline is vertical
           text_font_size = '25px', text_font = value('times'), text_font_style = 'bold')
    p.toolbar.logo = None
    p.toolbar_location = None

    # plot nodes and hemispheres in different color
    p.text([-1.3, 1.3], [0, 0], ['L', 'R'], text_align='center', text_baseline = 'middle',
           text_font_size = '20px', text_font = value('times'), text_font_style = 'bold')
    parcel_theta1_l, parcel_theta2_l = theta_left[0], theta_left[0]
    parcel_theta1_r, parcel_theta2_r = theta_right[0], theta_right[0]
    for i_parcel in range(len(parcel_name)):
        if i_parcel == 0:
            start = 0
        else:
            start = parcel_end1[i_parcel-1]
        # nodes    
        parcel_x_l = x_left[start:parcel_end1[i_parcel]]
        parcel_y_l = y_left[start:parcel_end1[i_parcel]]
        parcel_x_r = x_right[start:parcel_end1[i_parcel]]
        parcel_y_r = y_right[start:+parcel_end1[i_parcel]]
        p.circle(parcel_x_l, parcel_y_l, 
                 fill_color = parcel_color[i_parcel],
                 line_color = None)
        p.circle(parcel_x_r, parcel_y_r, 
                 fill_color = parcel_color[i_parcel],
                 line_color = None)
        
        # hemispheres
        if i_parcel == len(parcel_name) - 1:
            parcel_theta1_l = parcel_theta2_l
            parcel_theta2_l = theta_left[parcel_end[i_parcel]]
            parcel_theta1_r = parcel_theta2_r
            parcel_theta2_r = theta_right[parcel_end[i_parcel]]
        else:
            parcel_theta1_l = parcel_theta2_l
            parcel_theta2_l = (theta_left[parcel_end[i_parcel]] + theta_left[parcel_end[i_parcel]+1]) / 2
            parcel_theta1_r = parcel_theta2_r
            parcel_theta2_r = (theta_right[parcel_end[i_parcel]] + theta_right[parcel_end[i_parcel]+1]) / 2
        
        parcel_theta_l = np.linspace(parcel_theta1_l, parcel_theta2_l, 10)
        parcel_theta_r = np.linspace(parcel_theta1_r, parcel_theta2_r, 10)
        p.line(1.1 * np.cos(parcel_theta_l) - 0.05, 1.1 * np.sin(parcel_theta_l), 
               line_width = 10, line_color = parcel_color[i_parcel])
        p.line(1.1 * np.cos(parcel_theta_r) + 0.05, 1.1 * np.sin(parcel_theta_r),
               line_width = 10, line_color = parcel_color[i_parcel])   
    
    # set x_range and y_range, remove grids, axes and frame
    sqaure = 1.5
    p.x_range = Range1d(start = -sqaure, end = sqaure)
    p.y_range = Range1d(start = -sqaure, end = sqaure)
    p.axis.visible = False
    p.grid.visible = False
    p.outline_line_color = None
    
    
    # annotation for lobes
    parcel_annot_x = [-1.0, -0.2, 0.6, -1.0, -0.2, 0.6, -1.0, -0.2, 0.6]
    parcel_annot_x1 = [x+0.05 for x in parcel_annot_x]
    parcel_annot_y = [-1.25, -1.25, -1.25, -1.35, -1.35, -1.35, -1.45, -1.45, -1.45]
    p.circle(parcel_annot_x, parcel_annot_y, size = 15,
             line_color = None, fill_color = parcel_color)
    p.text(x = parcel_annot_x1, y = parcel_annot_y,
           text = parcel_name, text_font = value('times'),
           text_baseline = 'middle')
        
    
    # add annotation to each node
#    for node0 in range(1, num_nodes+1):   
#        node0_idx = np.argwhere(node_all == node0)
#        x0, y0 = x_all[node0_idx], y_all[node0_idx]
#        angle = theta_all[node0_idx]
# 
#        p.text(x = [x0 * 1.2], y = [y0 * 1.2], 
#               text = [node_name[node0-1]], angle = [angle],
#               text_font_size = '10px', text_font = value('times'),
#               text_baseline = 'middle')



    # plot
    for node1 in range(1, num_nodes): # 1,2,...,115
        for node2 in range(node1+1, num_nodes+1): # 2,3,...,116
            node1_idx = np.argwhere(node_all == node1)
            node2_idx = np.argwhere(node_all == node2)
            
            x1, x2 = x_all[node1_idx], x_all[node2_idx]
            y1, y2 = y_all[node1_idx], y_all[node2_idx]
            ratio = 1/2
            xm1, ym1 = x1 * ratio, y1 * ratio
            xm2, ym2 = x2 * ratio, y2 * ratio

            if conn_pos[node1-1, node2-1] == 1: # positive connectivity exists
                p.bezier(x0 = [x1], y0 = [y1],
                        x1 = [x2], y1 = [y2],
                        cx0 = [xm1], cy0 = [ym1],
                        cx1 = [xm2], cy1 = [ym2],
                        line_color = '#ff5a00')
                
            if conn_neg[node1-1, node2-1] == 1: # negative connectivity exists
                p.bezier(x0 = [x1], y0 = [y1],
                        x1 = [x2], y1 = [y2],
                        cx0 = [xm1], cy0 = [ym1],
                        cx1 = [xm2], cy1 = [ym2],
                        line_color = '#7069f6')                         
    # display and export figures  
#    show(p)
    export_png(p, filename = title + '.png')
    
#    connmap = get_screenshot_as_png(p)
#    return connmap
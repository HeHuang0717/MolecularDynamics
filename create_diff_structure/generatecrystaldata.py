# -*- coding: utf-8 -*-
"""
Created on Mon May 23 10:47:05 2016

@author: magicdietz
"""
import numpy as np


def make_3d_grid(x_space, y_space, z_space):
    "creates 3d_Grid in given xyz-space"
    return np.vstack(np.meshgrid(x_space, y_space, z_space)).reshape(3, -1).T

def fill_volume_bcc(x_limit, y_limit, z_limit, a):
    "fill given volume with BCC structure"
    calibration_factor = a * 2./np.sqrt(3)
    x_space = np.arange(0, 2*x_limit, 1.)
    y_space = np.arange(0, 2*y_limit, 1.)
    z_space = np.arange(0, 2*z_limit, 1.)
    first_grid = make_3d_grid(x_space, y_space, z_space)
    second_grid = np.copy(first_grid)
    second_grid += 1./2.
    crystal = np.vstack((first_grid, second_grid)) * calibration_factor
    condition = ((crystal[:, 0] <= x_limit)&
                 (crystal[:, 1] <= y_limit)&
                 (crystal[:, 2] <= z_limit))
    return crystal[condition]

def fill_volume_fcc(x_limit, y_limit, z_limit, a):
    "fill given volume with BCC structure"
    calibration_factor = a * 2./np.sqrt(2)
    x_space = np.arange(0, 2*x_limit, 1.)
    y_space = np.arange(0, 2*y_limit, 1.)
    z_space = np.arange(0, 2*z_limit, 1.)
    first_grid = make_3d_grid(x_space, y_space, z_space)
    second_grid = np.copy(first_grid)
    third_grid = np.copy(first_grid)
    fourth_grid = np.copy(first_grid)
    second_grid[:, 0:2] += 1./2.
    third_grid[:, 0] += 1./2.
    third_grid[:, 2] += 1./2.
    fourth_grid[:, 1:] += 1./2.
    crystal = np.vstack((first_grid,
                         second_grid,
                         third_grid,
                         fourth_grid)) * calibration_factor
    condition = ((crystal[:, 0] <= x_limit)&
                 (crystal[:, 1] <= y_limit)&
                 (crystal[:, 2] <= z_limit))
    return crystal[condition]

def add_hcp_line(x_vec, y_coord, z_coord):
    "create atom line along x-axis with space 1"
    crystal_line = np.zeros((len(x_vec), 3))
    crystal_line[:, 0] = x_vec
    crystal_line[:, 1] = y_coord
    crystal_line[:, 2] = z_coord
    return crystal_line

def add_hcp_layer(noa_x, noa_y, z_coord):
    "creates HCP Layer"
    x_vec = np.arange(0, int(round(noa_x)))
    crystal_volume = np.empty((0, 3))
    for y_coord in np.arange(0, noa_y, 2*np.sin(np.pi / 3.)):
        first_line = add_hcp_line(x_vec, y_coord, z_coord)
        second_line = add_hcp_line(x_vec + 1./2.,
                                   y_coord + np.sin(np.pi / 3.), z_coord)
        crystal_volume = np.vstack((crystal_volume, first_line))
        crystal_volume = np.vstack((crystal_volume, second_line))
    return crystal_volume

def fill_volume_hcp(x_space, y_space, z_space, a):
    "fill given volume with HCP structure"
    lattice_correct = np.sqrt(8/3)
    noa_x = int(round(x_space))
    noa_y = int(round(y_space / (np.sin(np.pi / 3.))))
    noa_z = int(round(z_space / (lattice_correct/2.)))
    crystal = np.empty((0, 3))
    unshifted_layer = True
    for z_coord in np.arange(0, noa_z+1, lattice_correct/2.):
        if unshifted_layer:
            cur_crystal = add_hcp_layer(noa_x + 1, noa_y + 1, z_coord)
            unshifted_layer = False
        else:
            cur_crystal = add_hcp_layer(noa_x + 1, noa_y + 1, z_coord)
            cur_crystal[:, 0] += 1./2.
            cur_crystal[:, 1] += 1./(2*np.sqrt(3))
            unshifted_layer = True
        crystal = np.vstack((crystal, cur_crystal * a))
        condition = ((crystal[:, 0] <= x_space)&
                     (crystal[:, 1] <= y_space)&
                     (crystal[:, 2] <= z_space))
    return crystal[condition]

fd=fill_volume_bcc(3, 3, 3, 0.5)\
fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(331, projection='3d') 
ax.scatter(fd[0], fd1], fd[2], c='r')

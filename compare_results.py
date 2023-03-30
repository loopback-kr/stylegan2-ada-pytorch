# Python Built-in libraries
import os, sys, json, csv, re, random, numpy as np
from os.path import join, basename, exists, splitext, dirname, isdir
from shutil import copy, copytree, rmtree
from glob import glob, iglob
from tqdm import tqdm, trange
from tqdm.contrib import tzip
from ast import literal_eval
import matplotlib.pyplot as plt
import matplotlib.image as img
import cv2 as cv


OUTPUT_DIR = 'outputs/benign_nomask/00000-benign_nomask-auto4-kimg25000-ada-bgc_norotate'
LOG_PATH = join(OUTPUT_DIR, 'log.txt')

with open(LOG_PATH, 'rt') as f:
    log = f.readlines()
with open(LOG_PATH, 'rt') as f:
    num_metrics = f.read().count('Evaluating metrics...')

os.makedirs(f'visualize/{OUTPUT_DIR.split("/")[-1]}', exist_ok=True)

for fake_idx in range(0, 10, 1):
    plt.figure(figsize=(10, 3), dpi=150)
    count = 0
    for i, l in enumerate(log):
        if 'Evaluating metrics...' in l:
            count += 1
            tick = int(log[i-1].split(' ')[1])
            kimg = int(float(log[i-1].split('kimg')[1].split(' ')[1]))
            metrics = literal_eval(log[i+1])
            fid = round(metrics['results']['fid50k_full'], 1)

            fakes_path = join(OUTPUT_DIR, f'fakes{kimg:06d}.png')
            fakes = img.imread(fakes_path)
            fake = fakes[0+(256*fake_idx):256+(256*fake_idx), 0+(256*fake_idx):256+(256*fake_idx)]
            
            ax = plt.subplot(1, num_metrics, count)
            ax.tick_params(left=False, bottom=False)
            ax.set(yticklabels=[])
            ax.set(ylabel=None)
            ax.set(xticklabels=[])
            ax.set(xlabel=None)
            plt.imshow(fake, cmap='gray')
            plt.xlabel(f'EP:{tick}, FID:{fid}')
    plt.tight_layout()
    plt.savefig(f'visualize/{OUTPUT_DIR.split("/")[-1]}/fake{fake_idx:03d}.png')
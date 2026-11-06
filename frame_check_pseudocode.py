# Frame displacement checker — pseudocode / reference only
# Requires: opencv-python, numpy
# NOT executed; provided as inspection guide

"""
import cv2
import numpy as np

def estimate_displacement(frame_a, frame_b):
    """Rough centroid shift of brightest region (placeholder heuristic)."""
    gray_a = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)
    # Threshold to isolate subject on neutral background
    _, mask_a = cv2.threshold(gray_a, 200, 255, cv2.THRESH_BINARY_INV)
    _, mask_b = cv2.threshold(gray_b, 200, 255, cv2.THRESH_BINARY_INV)
    m_a = cv2.moments(mask_a)
    m_b = cv2.moments(mask_b)
    cx_a = m_a['m10'] / (m_a['m00'] + 1e-6)
    cy_a = m_a['m01'] / (m_a['m00'] + 1e-6)
    cx_b = m_b['m10'] / (m_b['m00'] + 1e-6)
    cy_b = m_b['m01'] / (m_b['m00'] + 1e-6)
    return np.sqrt((cx_b - cx_a)**2 + (cy_b - cy_a)**2)

def check_flicker(frames, sample_stride=4):
    """Mean luminance per sampled frame; large jumps = flicker candidate."""
    luminances = []
    for i in range(0, len(frames), sample_stride):
        gray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
        luminances.append(gray.mean())
    return luminances

# Usage sketch:
# cap = cv2.VideoCapture('condition_b_fast.mp4')
# frames = []
# while True:
#     ret, f = cap.read()
#     if not ret: break
#     frames.append(f)
# displacements = [estimate_displacement(frames[i], frames[i+1])
#                  for i in range(len(frames)-1)]
# print('Mean disp:', np.mean(displacements), 'Std:', np.std(displacements))
# print('Flicker luminances:', check_flicker(frames))
"""

# Key discriminating metric:
# std(displacements) / mean(displacements) — coefficient of variation.
# CV < 0.2: uniform motion (smooth apparent motion)
# CV > 0.5: inconsistent displacement (apparent stutter or smear)
# -*- coding: utf-8 -*-
"""
Image Quality Checker - Detect blur and inconsistency issues
"""

import cv2
import numpy as np
import os
import json

INPUT_BASE = r'E:\sites\666-hotpot\public\images\cleaned'
REPORT_FILE = r'E:\sites\666-hotpot\quality_report.json'

def detect_blur(img):
    """Detect blur using Laplacian variance"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return variance

def analyze_image(filepath):
    """Analyze image quality"""
    img = cv2.imread(filepath)
    if img is None:
        return None
    
    h, w = img.shape[:2]
    
    # Overall blur score
    blur_score = detect_blur(img)
    
    # Check different regions
    regions = {
        'top_left': img[0:h//2, 0:w//2],
        'top_right': img[0:h//2, w//2:w],
        'bottom_left': img[h//2:h, 0:w//2],
        'bottom_right': img[h//2:h, w//2:w],
    }
    
    region_scores = {}
    for name, region in regions.items():
        region_scores[name] = detect_blur(region)
    
    # Check for inconsistency (some regions sharp, some blurry)
    scores = list(region_scores.values())
    max_score = max(scores)
    min_score = min(scores)
    
    # If ratio > 3, there's significant inconsistency
    ratio = max_score / max(min_score, 1)
    
    # Detect faces (for blur check)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    face_regions = []
    for (x, y, fw, fh) in faces:
        face_img = img[y:y+fh, x:x+fw]
        if face_img.size > 0:
            face_regions.append(detect_blur(face_img))
    
    return {
        'width': w,
        'height': h,
        'overall_blur': round(blur_score, 2),
        'region_scores': {k: round(v, 2) for k, v in region_scores.items()},
        'inconsistency_ratio': round(ratio, 2),
        'has_inconsistency': ratio > 3,
        'face_count': len(faces),
        'face_blur_scores': [round(s, 2) for s in face_regions] if face_regions else [],
        'is_problematic': blur_score < 100 or ratio > 3,  # Low blur score or inconsistent
    }

def main():
    print("=" * 60)
    print("Image Quality Checker - 666 Hot Pot Spicy Slices")
    print("=" * 60)
    
    results = {
        'total': 0,
        'problematic': 0,
        'by_folder': {},
        'issues': []
    }
    
    for folder in ['products', 'promo', 'users', 'assets', 'old']:
        folder_path = os.path.join(INPUT_BASE, folder)
        if not os.path.exists(folder_path):
            continue
        
        print(f"\n[FOLDER] {folder}")
        
        folder_results = {
            'total': 0,
            'problematic': 0,
            'issues': []
        }
        
        for f in os.listdir(folder_path):
            if not f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                continue
            
            results['total'] += 1
            folder_results['total'] += 1
            
            filepath = os.path.join(folder_path, f)
            analysis = analyze_image(filepath)
            
            if analysis and analysis['is_problematic']:
                results['problematic'] += 1
                folder_results['problematic'] += 1
                
                issue = {
                    'folder': folder,
                    'file': f,
                    'analysis': analysis
                }
                results['issues'].append(issue)
                folder_results['issues'].append(issue)
                
                print(f"  [ISSUE] {f}")
                print(f"    Blur: {analysis['overall_blur']} | Inconsistency: {analysis['inconsistency_ratio']}")
        
        results['by_folder'][folder] = folder_results
        print(f"  {folder_results['problematic']}/{folder_results['total']} problematic")
    
    # Save report
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print(f"Total: {results['total']} images")
    print(f"Problematic: {results['problematic']} images ({results['problematic']*100//max(results['total'],1)}%)")
    print(f"Report saved: {REPORT_FILE}")
    print("=" * 60)

if __name__ == '__main__':
    main()
